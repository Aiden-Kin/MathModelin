import pandas as pd

# 读取Excel文件中的数据
excel_file = "C:\\Users\\23166\\OneDrive\\大学文件\\A数学建模\\A数学建模实战\\代码与资源\\大气透射率.xlsx"  # 替换为你的Excel文件路径
df = pd.read_excel(excel_file)

# 计算大气透射率并保存到第三列
def calculate_transmittance(row):
    dHR = row['dHR_values']  # 假设Excel文件中的列名是'dHR'
    transmittance = 0.99321 - 0.0001176 * dHR + 1.97e-8 * dHR
    return transmittance

df['Atm'] = df.apply(calculate_transmittance, axis=1)

# 将结果保存到原Excel文件中的第三列
output_excel_file = 'C:\\Users\\23166\\OneDrive\\大学文件\\A数学建模\\A数学建模实战\\代码与资源\\大气透射率.xlsx'  # 替换为输出的Excel文件路径
df.to_excel(output_excel_file, index=False)