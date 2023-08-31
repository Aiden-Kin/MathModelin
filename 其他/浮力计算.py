import math
import sympy as sp
from sympy import symbols,Eq,solve

#  = (pou*g*(1/3*Pi*math.pow(r,3)+Pi *math.pow(r,3)(h-hs)))/((mo + mi)*g)


mo = 4866
mi = 2433
r = 1
hs = 0.8
pou = 1025
g = 9.8
h = symbols('h')
Pi = math.pi

# 定义等式
eq1 = Eq(pou*g*((1/3)*Pi*math.pow(r,2)*hs+Pi*math.pow(r,2)*(h-hs)),(mo + mi)*g)
print(eq1)

# 求解
solutions = solve(eq1, h)

print("求解得到的变量值:", solutions)


