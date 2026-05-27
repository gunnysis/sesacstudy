# a+b=1
# 5a+b=3

from sympy import solve, Symbol

a = Symbol('a')
b = Symbol('b')
ex1 = a + b - 1
ex2 = 5*a + b - 3
print(solve([ex1, ex2]))