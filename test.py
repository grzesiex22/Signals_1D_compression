import math
import time

def spinning_donut():
    A = 0
    B = 0
    while True:
        z = [0] * 1760
        b = [' '] * 1760
        for j in range(0, 628, 7):
            for i in range(0, 628, 2):
                c = math.sin(i / 100.0)
                d = math.cos(j / 100.0)
                e = math.sin(A)
                f = math.sin(j / 100.0)
                g = math.cos(A)
                h = d + 2
                D = 1 / (c * h * e + f * g + 5)
                l = math.cos(i / 100.0)
                m = math.cos(B)
                n = math.sin(B)
                t = c * h * g - f * e
                x = int(40 + 30 * D * (l * h * m - t * n))
                y = int(12 + 15 * D * (l * h * n + t * m))
                o = int(x + 80 * y)
                N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
                if 22 > y and y > 0 and x > 0 and 80 > x and D > z[o]:
                    z[o] = D
                    b[o] = ".,-~:;=!*#$@"[N if N > 0 else 0]
        print('\x1b[2J')
        for k in range(1760):
            print(b[k], end='')
            if k % 80 == 79:
                print()
        A += 0.04
        B += 0.02
        time.sleep(0.03)

def main():
    spinning_donut()

if __name__ == '__main__':
    main()