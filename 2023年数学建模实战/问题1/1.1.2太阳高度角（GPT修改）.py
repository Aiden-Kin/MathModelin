import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import pandas as pd

mpl.rcParams['font.sans-serif'] = ['SimHei']

# Given parameters
phi = 39.4  # Latitude (degrees), north is positive
H = 3  # Altitude (km)
D_values = [307, 337, 1, 32, 63, 93, 124, 154, 185, 215, 246, 276]  # Days since vernal equinox for each month
ST_values = np.arange(9, 15, 0.1)  # 给定时间

# Create an empty DataFrame to store results
df = pd.DataFrame(index=ST_values)

plt.figure(figsize=(8, 6))
plt.title("太阳的高度角和各月21号的时间关系")
plt.xlabel("时间")
plt.ylabel("高度角")
plt.grid(True)

# Set x-axis ticks for better readability
plt.xticks(np.arange(min(ST_values), max(ST_values)+1, 0.5))

# Possible line styles for better distinction
line_styles = ['-', '--', '-.', ':']

# Different colors for better distinction
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Calculate solar declination angle delta for each month
delta_values = np.arcsin(np.sin(2 * np.pi * np.array(D_values) / 365) * np.sin(np.radians(23.45)))

# Calculate solar altitude angle alpha_s and azimuth angle gamma_s for each month and time point
alpha_s_values = {}
for D, delta in zip(D_values, delta_values):
    month = D_values.index(D) + 1
    alpha_s_values[month] = []
    for omega in [np.pi / 12 * (ST - 12) for ST in ST_values]:
        alpha_s = np.arcsin(np.cos(delta) * np.cos(np.radians(phi)) * np.cos(omega) + np.sin(delta) * np.sin(np.radians(phi)))
        alpha_s_values[month].append(np.degrees(alpha_s))

    df[f"月份_{month}"] = alpha_s_values[month]  # Save to DataFrame

    # Choose line style and color from the list
    chosen_style = line_styles[(month - 1) % len(line_styles)]
    chosen_color = colors[(month - 1) % len(colors)]
    plt.plot(ST_values, alpha_s_values[month], label=f"月份={month}", linestyle=chosen_style, color=chosen_color)

plt.legend(loc='upper right', fontsize=6)
plt.savefig(r'E:\Code\Python\MathEveroment\2023年数学建模实战\图片\太阳高度角.jpg', format='jpg')
plt.show()
