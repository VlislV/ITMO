import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return 0.01 * (8*x**2 + 2*x*y + 27*x + 6*y + 9)

x = np.linspace(-20, 20, 500)
y = np.linspace(-50, 50, 500)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

plt.figure(figsize=(10, 8))
contour = plt.contour(X, Y, Z, levels=30, cmap='viridis', alpha=0.8)
plt.clabel(contour, inline=True, fontsize=8, fmt='%0.1f')
plt.plot(-3, 10.5, 'ro', markersize=8, label='Седловая точка')
plt.plot(73/16, -50, 'go', markersize=12, label='Глобальный минимум')
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(-20, 20)
plt.ylim(-50, 50)
plt.title('Линии уровня функции $f(x,y)$')
plt.legend()
plt.grid(alpha=0.3)
plt.colorbar(contour, label='$f(x,y)$')
plt.show()