class ThingTuple(tuple):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.current = kwargs.get('current', None)

    def __new__(self, *args, **kwargs):
        return super().__new__(ThingTuple, *args, **kwargs)

    def __getattr__(self, attr):
        if attr == 'current':
            return object.__getattribute__(self, attr)
        if attr == 'each':
            return self
        elif attr in ['being_the', 'and_the']:
            self.current = 'property'
            p = []
            for i in self:
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)
        if self.current == 'property':
            self.current = 'property_value'
            p = []
            for i in self:
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)
        elif self.current == 'property_value':
            p = []
            for i in self:
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)
        elif self.current == 'having':
            p = []
            for i in self:
                i.has(self.count)
                p.append(i.__getattr__(attr))
            return ThingTuple(p, current=self.current)

    def having(self, num):
        self.count = num
        self.current = 'having'
        return self


class Thing(object):
    def __init__(self, name):
        self.name = name
        self.current = None

    def __getattr__(self, attr):
        if attr == 'is_a':
            self.current = '+bool'
            return self
        elif attr == 'is_not_a':
            self.current = '-bool'
            return self
        elif attr in ['is_the', 'being_the', 'and_the']:
            self.current = 'property'
            return self
        elif attr == 'can':
            self.current = 'verb'
            return self
        elif attr == 'verb':
            return object.__getattribute__(self, attr)

        if self.current == '+bool':
            self.__setattr__(f'is_a_{attr}', True)
        elif self.current == '-bool':
            self.__setattr__(f'is_a_{attr}', False)
        elif self.current == 'property':
            self.property_name = attr
            self.current = 'property_value'
        elif self.current == 'property_value':
            self.__setattr__(self.property_name, attr)
        elif self.current == 'has':
            n = f'{attr}' if not f'{attr}'.endswith('s') else f'{attr}'[:-1]
            if self.count == 1:
                self.__setattr__(attr, Thing(n))
            else:
                self.__setattr__(attr, ThingTuple([Thing(n) for _ in range(self.count)]))
            return self.__dict__[attr]
        elif self.current == 'verb':
            self.verb_name = attr
            return self.verb
        return self

    def verb(self, func, past=None):
        if past:
            func = self.past(func, self.name)
            self.__setattr__(past, func.results)
        func.__globals__['name'] = self.name
        self.__setattr__(self.verb_name, func)

    @staticmethod
    def past(func, name):

        def wrapper(*args, **kwargs):
            wrapper.results.append(func(*args, **kwargs))
            return wrapper.results[-1]

        wrapper.results = []
        return wrapper

    def __setattr__(self, attr, val):
        self.__dict__[attr] = val

    def has(self, num):
        self.count = num
        self.current = 'has'
        return self

    def having(self, num):
        return self.has(num)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    mk = Thing('MK')
    mk.is_a.person
    mk.is_a.programmer
    mk.is_not_a.biologist
    mk.has(1).head.having(2).eyes.each.being_the.color.black.having(1).pupil.being_the.color.black
    mk.can.talk(lambda phrase: phrase, past="talked")
    print(f'mk.is_a_person: {mk.is_a_person}')
    print(f'mk.is_a_programmer: {mk.is_a_programmer}')
    print(f'mk.is_a_biologist: {mk.is_a_biologist}')
    print(f'mk.head.eyes[0].color: {mk.head.eyes[0].color}')
    print(f'mk.head.eyes[0].pupil.color: {mk.head.eyes[0].pupil.color}')
    print(f'mk.head.eyes[1].color: {mk.head.eyes[1].color}')
    print(f'mk.head.eyes[1].pupil.color: {mk.head.eyes[1].pupil.color}')
    print(mk.talk('Hello!'))
    print(mk.talk("My name's %s" % (name)))
    print(mk.talk("What's yours?"))
    # print(*mk.talked,sep='n')
