import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件到 DataFrame
# df = pd.read_excel("data.xlsx")

# 假设这是从 Excel 文件中读取的数据
file_path = '问题1.2数据.xlsx'
df = pd.read_excel(file_path)

# 计算相对位移和相对速度
df['相对位移 (m)'] = df['浮子 (m)'] - df['振子 (m)']
df['相对速度 (m/s)'] = df['浮子 (m/s)'] - df['振子 (m/s)']

# Set the font properties for UTF-8 characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei is a commonly used font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # This is to display the minus sign properly


# 绘制图表
plt.figure(figsize=(12, 6))

# 相对位移图
plt.subplot(1, 2, 1)
plt.plot(df['时间'], df['相对位移 (m)'], label='相对位移 (m)')
plt.xlabel('时间 (s)')
plt.ylabel('相对位移 (m)')
plt.title('相对位移 vs 时间')
plt.grid(True)
plt.legend()

# 相对速度图
plt.subplot(1, 2, 2)
plt.plot(df['时间'], df['相对速度 (m/s)'], label='相对速度 (m/s)', color='r')
plt.xlabel('时间 (s)')
plt.ylabel('相对速度 (m/s)')
plt.title('相对速度 vs 时间')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
