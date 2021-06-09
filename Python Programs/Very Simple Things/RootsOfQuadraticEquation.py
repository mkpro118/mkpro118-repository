from math import sqrt


class Quadratic_Roots:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.d = b**2 - 4 * a * c
        self.x = list()
        self.Error = False
        self.error_msg = 'Some Error Occured!'

    def check_possible(self):
        try:
            if self.a == 0:
                print('Not a Quadratic Equation!')
                self.Error = True
            else:
                return
        except Exception:
            self.Error = True
            print(self.error_msg)

    def check_nature(self):
        try:
            if self.d < 0:
                return "imaginary"
            else:
                return "real"
        except Exception:
            self.Error = True
            print(self.error_msg)

    def solve_real(self):
        try:
            val1 = round((-self.b + sqrt(self.d)) / (2 * self.a), 5)
            val2 = round((-self.b - sqrt(self.d)) / (2 * self.a), 5)
            self.x = [val1, val2]
            return self.x
        except Exception:
            print(self.error_msg)

    def solve_imaginary(self):
        try:
            val_real = round(-self.b / 2 * self.a, 5)
            val_imag = round(sqrt(-self.d) / 2 * self.a, 5)
            self.x = [complex(val_real, val_imag), complex(val_real, -val_imag)]
            return self.x
        except Exception:
            print(self.error_msg)
            raise

    def find_roots(self):
        try:
            self.check_possible()
            nature = self.check_nature()
            if nature == 'real':
                if not self.Error:
                    for i in self.solve_real():
                        print(f'x = {i}')
            elif nature == 'imaginary':
                if not self.Error:
                    for i in self.solve_imaginary():
                        print(f'x = {i}')
        except Exception:
            self.Error = True
            print(self.error_msg)


# Driver Code
if __name__ == '__main__':
    try:
        # a = float(input('Enter coefficient of second degree variable\n'))
        # b = float(input('Enter coefficient of first degree variable\n'))
        # c = float(input('Enter constant term\n'))
        a, b, c = 1, 1, 1
        roots = Quadratic_Roots(a, b, c)
        roots.find_roots()
    except Exception:
        print('Some Error Occured!')
