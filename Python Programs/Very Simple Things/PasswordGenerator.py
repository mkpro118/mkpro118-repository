import string
import random

l = list(string.printable)
b = [l[i] for i in range(62, 74)] + [l[i] for i in range(75, 88)] + [l[i] for i in range(89, 100)]
for i in b:
    l.remove(i)


def generate(n):
    k = []
    for _ in range(n):
        k.append(random.choice(l))
    print(''.join(k))


if __name__ == '__main__':
    generate(16)
