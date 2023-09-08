import matplotlib.pyplot as plt
import pandas as pd

# 读取Excel文件
excel_file = "C:\\Users\\23166\\OneDrive\\大学文件\\A数学建模\\A数学建模实战\\题目\\A题\\附件.xlsx" # 将'your_excel_file.xlsx'替换为实际的Excel文件路径
df = pd.read_excel(excel_file)

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei is a commonly used font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # This is to display the minus sign properly
# 提取x和y坐标数据
# 提取x和y坐标数据
x = df['x坐标 (m)']
y = df['y坐标 (m)']

# 创建二维点图
plt.figure(figsize=(10, 10))  # 可选：设置图形大小
plt.scatter(x, y, marker='.', color='orange', label='定日镜')  # 创建散点图
plt.xlabel('x坐标 (m)')
plt.ylabel('y坐标 (m)')
plt.title('定日镜位置')
plt.grid(True)

plt.legend()
plt.show()