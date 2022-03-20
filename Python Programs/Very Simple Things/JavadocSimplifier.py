from bs4 import BeautifulSoup as BS
import requests


def safeguard(func):
    from functools import wraps

    @wraps(func)
    def wrapper(self):
        try:
            func(self)
        except AttributeError:
            field = func.__name__.replace('find_', '')
            self.__setattr__(field, '')
    return wrapper


class HTML:
    DD = 'dd'
    DL = 'dl'
    DT = 'dt'
    LI = 'li'
    UL = 'ul'
    CODE = 'code'
    DIV = 'div'
    SPAN = 'span'
    SECTION = 'section'


class CSS:
    BLOCK = 'block'
    CLASS = 'class'
    DETAIL = 'detail'
    ARGUMENTS = 'arguments'
    MODIFIERS = 'modifiers'
    BLOCK_LIST = 'blockList'
    MEMBER_NAME = 'memberName'
    PARAM_LABEL = 'paramLabel'
    RETURN_TYPE = 'returnType'
    RETURN_LABEL = 'returnLabel'
    THROWS_LABEL = 'throwsLabel'
    METHOD_DETAILS = 'methodDetails'
    MEMBER_SIGNATURE = 'memberSignature'
    CONSTRUCTOR_DETAILS = 'constructorDetails'
    OVERRIDE_SPECIFY_LABEL = 'overrideSpecifyLabel'


class Method:
    def __init__(self, method):
        self.method = method
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
    def find_signature(self):
        self.signature = self.method.find(HTML.DIV, {CSS.CLASS: CSS.MEMBER_SIGNATURE}).text

    @safeguard
    def find_modifiers(self):
        self.modifiers = self.method.find(HTML.SPAN, {CSS.CLASS: CSS.MODIFIERS}).text

    @safeguard
    def find_name(self):
        self.name = self.method.find(HTML.SPAN, {CSS.CLASS: CSS.MEMBER_NAME}).text

    @safeguard
    def find_return_type(self):
        self.return_type = self.method.find(HTML.SPAN, {CSS.CLASS: CSS.RETURN_TYPE}).text
        self.return_type = self.return_type.replace('java.lang.', '').lower().strip()

    @safeguard
    def find_params(self):
        self.params = self.method.find(HTML.SPAN, {CSS.CLASS: CSS.ARGUMENTS}).text
        self.params = self.params.replace('java.lang.', '').replace(')', '')
        self.params = ', '.join(map(lambda p: p.strip(), self.params.split(',')))

    @safeguard
    def find_description(self):
        self.description = self.method.find(HTML.DIV, {CSS.CLASS: CSS.BLOCK}).text
        self.description = self.description.replace('\r', '').replace('\n ', '\n').strip()
        self.description = self.description.split('\n')

    @safeguard
    def find_params_description(self):
        if not (self.method.find(HTML.SPAN, {CSS.CLASS: CSS.PARAM_LABEL})):
            raise AttributeError
        self.params_description = []
        dl = self.method.find(HTML.DL)
        start = False
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
    def find_return_description(self):
        if not (_ := self.method.find(HTML.SPAN, {CSS.CLASS: CSS.RETURN_LABEL})):
            raise AttributeError
        description = f'\n * {" " * 7}'.join(map(lambda x: x.strip(), _.next.next.next.text.strip().split('\r')))
        self.return_description = f"@return {description}"

    @safeguard
    def find_throws_description(self):
        if not (self.method.find(HTML.SPAN, {CSS.CLASS: CSS.THROWS_LABEL})):
            raise AttributeError
        self.throws_description = []
        dl = self.method.find(HTML.DL)
        start = False
        for i in dl.children:
            if i.name == 'dt' and i.find(HTML.SPAN, {CSS.CLASS: CSS.THROWS_LABEL}):
                start = True
            elif i.name == 'dt' and start:
                break
            elif i.name == 'dd' and start:
                description = f'\n * {" " * 7}'.join(map(lambda x: x.strip(), i.text.strip().split('\r')))
                self.throws_description.append(f'@throws {description}\n')
            else:
                continue

    @safeguard
    def find_override(self):
        if not (_ := self.method.find(HTML.SPAN, {CSS.CLASS: CSS.OVERRIDE_SPECIFY_LABEL})):
            raise AttributeError
        self.override = '@Override\n'

    @safeguard
    def generate_comments(self):
        self.comment = '/**\n'
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
    def generate_stub(self):
        self.stub = f'{self.comment}\n{self.override}{self.signature} {{\n\n}}'
        print(self.stub)

    def __str__(self):
        return self.stub

    def __repr__(self):
        return str(self)


def get_source(url):
    with requests.get(url) as response:
        assert response.ok
        return response.text


def get_soup(source, parser):
    return BS(source, parser)


def get_methods(container):
    for _ in container.find_all(HTML.LI, {CSS.CLASS: CSS.BLOCK_LIST}):
        yield _.find(HTML.SECTION, {CSS.CLASS: CSS.DETAIL})


def run(soup, method_type):
    method_container = soup.find(
        HTML.SECTION,
        {
            CSS.CLASS: method_type,
        }
    ).find(
        HTML.UL,
        {
            CSS.CLASS: CSS.BLOCK_LIST,
        }
    )
    methods = get_methods(method_container)
    for method in methods:
        _ = Method(method)
        print(_.stub)
        print()


def generate(url, parser):
    source = get_source(url).replace('&nbsp;', ' ').replace('&#8203;', '')
    soup = get_soup(source, parser)
    run(soup, CSS.CONSTRUCTOR_DETAILS)
    run(soup, CSS.METHOD_DETAILS)


if __name__ == '__main__':
    URLS = [
        'https://cs300-www.cs.wisc.edu/wp/wp-content/uploads/2020/12/spring22/p5/doc/TreasureHunt.html',
        'https://cs300-www.cs.wisc.edu/wp/wp-content/uploads/2020/12/spring22/p5/doc/InteractiveObject.html',
    ]
    PARSER = 'lxml'
    for url in URLS:
        print(f'From: {url}')
        generate(url, PARSER)
