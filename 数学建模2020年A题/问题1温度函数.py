import pandas as pd
import matplotlib.pyplot as plt


file_path = 'C:\\Users\\23166\\OneDrive\\大学文件\\A数学建模\\历年真题\\2020建模赛题\\A\\附件.xlsx'
df = pd.read_excel(file_path)

# Set the font properties for UTF-8 characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei is a commonly used font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # This is to display the minus sign properly

x_data = df.iloc[:, 0]
y_data = df.iloc[:, 1]

# 创建一个新的绘图窗口
fig = plt.figure(figsize=(12, 6))

# 绘制曲线图
plt.plot(x_data, y_data, linestyle='-', color='orange',linewidth=2, label='温度')

# 添加标题和标签
plt.title('温度曲线')
plt.xlabel('时间（s）')
plt.ylabel('温度(℃)')

# 添加图例
plt.legend()

# 显示网格线
plt.grid(True)
plt.savefig('图片/2.svg', format='svg')
# 显示图表
plt.show()