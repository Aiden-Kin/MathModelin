import sympy as sp

# 定义符号变量
x = sp.symbols('h')

# 定义等式
equation = (pou*g*(1/3*Pi*math.pow(r,3)+Pi *math.pow(r,3)(h-hs)))/((mo + mi)*g)

# 求解
solutions = sp.solve(equation, x)

print("求解得到的变量值:", solutions)