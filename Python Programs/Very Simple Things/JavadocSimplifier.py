from bs4 import BeautifulSoup as BS
import requests


def safeguard(func: callable) -> callable:
    from functools import wraps

    @wraps(func)
    def wrapper(self: object, *args: tuple, **kwargs: dict) -> object:
        try:
            return func(self, *args, **kwargs)
        except AttributeError:
            if 'find' in func.__name__:
                field = func.__name__.replace('find_', '')
                self.__setattr__(field, '')
    return wrapper


class HTML:
    DD: str = 'dd'
    DL: str = 'dl'
    DT: str = 'dt'
    LI: str = 'li'
    UL: str = 'ul'
    CODE: str = 'code'
    DIV: str = 'div'
    SPAN: str = 'span'
    SECTION: str = 'section'


class CSS:
    BLOCK: str = 'block'
    CLASS: str = 'class'
    DETAIL: str = 'detail'
    ARGUMENTS: str = 'arguments'
    MODIFIERS: str = 'modifiers'
    BLOCK_LIST: str = 'blockList'
    MEMBER_NAME: str = 'memberName'
    PARAM_LABEL: str = 'paramLabel'
    RETURN_TYPE: str = 'returnType'
    RETURN_LABEL: str = 'returnLabel'
    THROWS_LABEL: str = 'throwsLabel'
    FIELD_DETAILS: str = 'fieldDetails'
    METHOD_DETAILS: str = 'methodDetails'
    MEMBER_SIGNATURE: str = 'memberSignature'
    CONSTRUCTOR_DETAILS: str = 'constructorDetails'
    OVERRIDE_SPECIFY_LABEL: str = 'overrideSpecifyLabel'


class Field:
    def __init__(self, field: BS):
        self.field: BS = field
        self.find_modifiers()
        self.find_name()
        self.find_return_type()
        self.find_params()
        self.find_signature()
        self.find_description()
        if self.params:
            self.find_params_description()
        else:
            self.params_description = ''
        if self.return_type and self.return_type != 'void':
            self.find_return_description()
        else:
            self.return_description = ''
        self.find_throws_description()
        self.find_override()
        self.generate_comments()
        self.generate_stub()

    @safeguard
    def find_signature(self) -> None:
        self.signature: str = self.field.find(HTML.DIV, {CSS.CLASS: CSS.MEMBER_SIGNATURE}).text
        self.signature = ', '.join(map(lambda p: p.strip(), self.signature.split(',')))

    @safeguard
    def find_modifiers(self) -> None:
        self.modifiers: str = self.field.find(HTML.SPAN, {CSS.CLASS: CSS.MODIFIERS}).text

    @safeguard
    def find_name(self) -> None:
        self.name: str = self.field.find(HTML.SPAN, {CSS.CLASS: CSS.MEMBER_NAME}).text

    @safeguard
    def find_return_type(self) -> None:
        self.return_type: str = self.field.find(HTML.SPAN, {CSS.CLASS: CSS.RETURN_TYPE}).text
        self.return_type = self.return_type.replace('java.lang.', '').strip()

    @safeguard
    def find_params(self) -> None:
        self.params: str = self.field.find(HTML.SPAN, {CSS.CLASS: CSS.ARGUMENTS}).text
        self.params = self.params.replace('java.lang.', '').replace(')', '')
        self.params = ', '.join(map(lambda p: p.strip(), self.params.split(',')))

    @safeguard
    def find_description(self) -> None:
        self.description: str = self.field.find(HTML.DIV, {CSS.CLASS: CSS.BLOCK}).text
        self.description = self.description.replace('\r', '').replace('\n ', '\n').strip()
        self.description: list = self.description.split('\n')

    @safeguard
    def find_params_description(self) -> None:
        if not (self.field.find(HTML.SPAN, {CSS.CLASS: CSS.PARAM_LABEL})):
            raise AttributeError
        self.params_description: list = []
        dl: BS = self.field.find(HTML.DL)
        start: bool = False
        for i in dl.children:
            if i.name == 'dt' and i.find(HTML.SPAN, {CSS.CLASS: CSS.PARAM_LABEL}):
                start = True
            elif i.name == 'dt' and start:
                break
            elif i.name == 'dd' and start:
                description = f'\n * {" " * 7}'.join(map(lambda x: x.strip(), i.text.strip().split('\r')))
                self.params_description.append(f'@param {description}')
            else:
                continue

    @safeguard
    def find_return_description(self) -> None:
        if not (_ := self.field.find(HTML.SPAN, {CSS.CLASS: CSS.RETURN_LABEL})):
            raise AttributeError
        description: str = f'\n * {" " * 7}'.join(map(lambda x: x.strip(), _.next.next.next.text.strip().split('\r')))
        self.return_description: str = f"@return {description}"

    @safeguard
    def find_throws_description(self) -> None:
        if not (self.field.find(HTML.SPAN, {CSS.CLASS: CSS.THROWS_LABEL})):
            raise AttributeError
        self.throws_description: list = []
        dl: BS = self.field.find(HTML.DL)
        start: bool = False
        for i in dl.children:
            if i.name == 'dt' and i.find(HTML.SPAN, {CSS.CLASS: CSS.THROWS_LABEL}):
                start = True
            elif i.name == 'dt' and start:
                break
            elif i.name == 'dd' and start:
                description: str = f'\n * {" " * 7}'.join(map(lambda x: x.strip(), i.text.strip().split('\r')))
                self.throws_description.append(f'@throws {description}\n')
            else:
                continue

    @safeguard
    def find_override(self) -> None:
        if not (_ := self.field.find(HTML.SPAN, {CSS.CLASS: CSS.OVERRIDE_SPECIFY_LABEL})):
            raise AttributeError
        self.override: str = '@Override\n'

    @safeguard
    def generate_comments(self) -> None:
        self.comment: str = '/**\n'
        for line in self.description:
            self.comment += f' * {line}\n'
        if self.params_description:
            self.comment += ' * \n'
        for line in self.params_description:
            self.comment += f' * {line}\n'
        if self.return_description:
            self.comment += ' *\n'
            self.comment += f' * {self.return_description}\n'
        if self.throws_description:
            self.comment += ' *\n'
        for line in self.throws_description:
            self.comment += f' * {line}\n'
        self.comment += ' */'

    @safeguard
    def generate_stub(self) -> None:
        self.stub: str = f'{self.comment}\n{self.override}{self.signature} {{\n  {self.default_return()}\n}}'
        self.stub = self.stub.replace('java.lang.', '')

    @safeguard
    def default_return(self) -> str:
        if self.return_type in ['void', '']:
            return ''
        elif self.return_type in ['byte', 'short', 'int', 'long', 'float', 'double', ]:
            return 'return 0;'
        elif self.return_type == 'boolean':
            return 'return false;'
        elif self.return_type == 'char':
            return "return '\\u0000';"
        else:
            return 'return null;'

    def __str__(self) -> str:
        return self.stub

    def __repr__(self) -> str:
        return str(self)


def get_source(url: str) -> str:
    with requests.get(url) as response:
        assert response.ok
        return response.text


def get_soup(source: str, parser: str) -> BS:
    return BS(source, parser)


def get_fields(container: BS) -> BS:
    for _ in container.find_all(HTML.LI, {CSS.CLASS: CSS.BLOCK_LIST}):
        yield _.find(HTML.SECTION, {CSS.CLASS: CSS.DETAIL})


@safeguard
def run(soup: BS, field_type: str) -> None:
    field_container = soup.find(
        HTML.SECTION,
        {
            CSS.CLASS: field_type,
        }
    ).find(
        HTML.UL,
        {
            CSS.CLASS: CSS.BLOCK_LIST,
        }
    )
    fields = get_fields(field_container)
    for field in fields:
        _ = Field(field)
        if field_type is CSS.FIELD_DETAILS:
            description = '\n// '.join(_.description).strip()
            description = f'// {description}' if description else description
            print(f'{_.modifiers} {_.return_type} {_.name}; {description}')
        else:
            print(_.stub)
        print()


def generate(url: str, parser: str) -> None:
    source = get_source(url).replace('&nbsp;', ' ').replace('&#8203;', '')
    soup = get_soup(source, parser)
    run(soup, CSS.FIELD_DETAILS)
    run(soup, CSS.CONSTRUCTOR_DETAILS)
    run(soup, CSS.METHOD_DETAILS)


if __name__ == '__main__':
    URLS = [
        'https://cs300-www.cs.wisc.edu/wp/wp-content/uploads/2020/12/spring22/p5/doc/TreasureHunt.html',
    ]
    PARSER = 'lxml'
    for url in URLS:
        print(f'From: {url}')
        print('-' * 150)
        generate(url, PARSER)
        print('-' * 150)
