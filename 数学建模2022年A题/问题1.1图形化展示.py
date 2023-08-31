import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file into a DataFrame
file_path = 'E:\\Code\\Python\\MathEveroment\\数学建模2022年A题\\问题1.1数据.xlsx'
df = pd.read_excel(file_path)

# Set the font properties for UTF-8 characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei is a commonly used font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # This is to display the minus sign properly

# Create a figure and a set of subplots (two subplots)
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Plotting the velocity data
axes[0].plot(df['时间'], df['浮子 (m/s)'], label='浮子速度 (m/s)', color='b')
axes[0].plot(df['时间'], df['振子 (m/s)'], label='振子速度 (m/s)', color='r')
axes[0].set_title('速度随时间的变化')
axes[0].set_xlabel('时间 (s)')
axes[0].set_ylabel('速度 (m/s)')
axes[0].legend()
axes[0].grid(True)

# Plotting the position data
axes[1].plot(df['时间'], df['浮子 (m)'], label='浮子位移 (m)', color='b')
axes[1].plot(df['时间'], df['振子 (m)'], label='振子位移 (m)', color='r')
axes[1].set_title('位移随时间的变化')
axes[1].set_xlabel('时间 (s)')
axes[1].set_ylabel('位置 (m)')
axes[1].legend()
axes[1].grid(True)

# Show the plots
plt.tight_layout()
plt.show()
