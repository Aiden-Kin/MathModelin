import pandas as pd
import numpy as np
import math

# Read the Excel file
df = pd.read_excel(r"E:\Code\Python\MathEveroment\2023年数学建模实战\表格数据\solar_altitude_angles.xlsx")

# Given parameters for DNI formula
G0 = 1361  # Solar constant in W/m^2
a = 0.75  # example parameter
b = 0.25  # example parameter
c = 0.1   # example parameter

# Calculate DNI for each solar altitude angle
for column in df.columns[1:]:  # Skipping the first column which is the 'Time' or 'Index'
    df[f"{column}_DNI"] = 1.366*(0.34981+0.5783875* np.exp(-0.275745 / np.sin(np.radians(df[column]))))

# Save the updated DataFrame back to Excel
df.to_excel("solar_altitude_and_DNI.xlsx", index=False)
