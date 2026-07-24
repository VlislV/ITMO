import numpy as np
import matplotlib.pyplot as plt

rows, cols =  50, 70
top_L, bottom_L = 0.0, 0.0
top_R, bottom_R = 10.0, 20.0

T = np.full((rows, cols), (bottom_R + top_R) / 2)
T[0, :] = np.linspace(top_L, top_R, cols)
T[-1, :] = np.linspace(bottom_L, bottom_R, cols)
T[:, 0] = np.linspace(top_L, bottom_L, rows)
T[:, -1] = np.linspace(top_R, bottom_R, rows)

for _ in range(100):
    T_new = T.copy()
    T_new[1:-1, 1:-1] = (T[:-2, 1:-1] + T[2:, 1:-1] + T[1:-1, :-2] + T[1:-1, 2:]) / 4
    if np.abs(T_new - T).max() < 1e-4:
        T = T_new
        break
    T = T_new

print(np.round(T, 1))

fig, ax = plt.subplots(figsize=(10, 6))
img = ax.imshow(T, cmap='coolwarm', interpolation='bilinear')
cbar = fig.colorbar(img, ax=ax, orientation='horizontal', pad=0.1, label='Температура')
bg = dict(facecolor='white', alpha=0.6, edgecolor='none', pad=2)
ax.text(0, 0, f'{top_L}°C', ha='center', va='center', fontweight='bold', bbox=bg)
ax.text(0, rows-1, f'{bottom_L}°C', ha='center', va='center', fontweight='bold', bbox=bg)
ax.text(cols-1, 0, f'{top_R}°C', ha='center', va='center', fontweight='bold', bbox=bg)
ax.text(cols-1, rows-1, f'{bottom_R}°C', ha='center', va='center', fontweight='bold', bbox=bg)
plt.tight_layout()
plt.show()