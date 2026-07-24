import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================
# ПАРАМЕТРЫ
# ============================================
T0 = 0.1
h = 0.01
c = np.sqrt(T0 / h)  # скорость волны (100 м/с)


L = 1.0                 # длина струны, м
N_modes = 50            # количество мод Фурье
Nx = 500                # точек по координате
t_max = 10             # время моделирования, с
fps = 10000                # кадров в секунду

# ============================================
# КООРДИНАТЫ
# ============================================
x = np.linspace(0, L, Nx)
t_vals = np.linspace(0, t_max, int(t_max * fps))

# ============================================
# НАЧАЛЬНЫЕ УСЛОВИЯ (треугольник как в struna_1.py)
# ============================================
peak_x = 0.7
peak_y = 0.05

def f(x):  # начальная форма
    result = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi <= peak_x:
            result[i] = peak_y * xi / peak_x
        else:
            result[i] = peak_y * (L - xi) / (L - peak_x)
    return result

def g(x):  # начальная скорость (ноль)
    return np.zeros_like(x)

# ============================================
# ВЫЧИСЛЕНИЕ КОЭФФИЦИЕНТОВ ФУРЬЕ
# ============================================
def fourier_coefficients(f, g, L, c, N_modes, Nx):
    """
    Вычисляет коэффициенты A_n и B_n для метода Фурье
    """
    x_int = np.linspace(0, L, Nx)
    dx = L / (Nx - 1)
    
    A = np.zeros(N_modes)
    B = np.zeros(N_modes)
    
    f_values = f(x_int)
    g_values = g(x_int)
    
    for n in range(1, N_modes + 1):
        n_idx = n - 1  # индекс в массиве
        
        # Интегрируем методом трапеций
        sin_n = np.sin(n * np.pi * x_int / L)
        
        # A_n = (2/L) * ∫ f(x) sin(nπx/L) dx
        A[n_idx] = (2.0 / L) * np.trapz(f_values * sin_n, dx=dx)
        
        # B_n = (2/(nπc)) * ∫ g(x) sin(nπx/L) dx
        B[n_idx] = (2.0 / (n * np.pi * c)) * np.trapz(g_values * sin_n, dx=dx)
    
    return A, B

# ============================================
# ФУНКЦИЯ ДЛЯ ВЫЧИСЛЕНИЯ СМЕЩЕНИЯ
# ============================================
def u_fourier(x, t, A, B, L, c, N_modes):
    """
    Вычисляет смещение в момент времени t
    """
    u = np.zeros_like(x)
    
    for n in range(1, N_modes + 1):
        n_idx = n - 1
        omega = n * np.pi * c / L
        sin_n = np.sin(n * np.pi * x / L)
        
        u += (A[n_idx] * np.cos(omega * t) + B[n_idx] * np.sin(omega * t)) * sin_n
    
    return u

# ============================================
# ВЫЧИСЛЯЕМ КОЭФФИЦИЕНТЫ
# ============================================
print("Вычисление коэффициентов Фурье...")
A, B = fourier_coefficients(f, g, L, c, N_modes, Nx)

print(f"Первые 5 коэффициентов A_n: {A[:5]}")
print(f"Первые 5 коэффициентов B_n: {B[:5]}")

# ============================================
# АНИМАЦИЯ
# ============================================
fig, ax = plt.subplots(figsize=(12, 6))

ax.set_xlim(0, L)
ax.set_ylim(-peak_y * 1.2, peak_y * 1.2)
ax.set_xlabel("x, м", fontsize=12)
ax.set_ylabel("u, м", fontsize=12)
ax.set_title("Колебания струны — решение методом Фурье", fontsize=14)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color="black", linewidth=0.5)

line, = ax.plot([], [], "b-", linewidth=2, label="Струна")
initial_line, = ax.plot(x, f(x), "r--", alpha=0.5, linewidth=1, label="Начальное положение")

ax.legend()
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=12)

def init():
    line.set_data([], [])
    time_text.set_text("")
    return line, time_text

def animate(frame):
    t = t_vals[frame]
    y = u_fourier(x, t, A, B, L, c, N_modes)
    line.set_data(x, y)
    time_text.set_text(f"Время: {t:.3f} с")
    return line, time_text

print(f"Запуск анимации... (t_max={t_max} с, {len(t_vals)} кадров)")

ani = FuncAnimation(fig, animate, init_func=init, frames=len(t_vals), interval=1000/fps, blit=True)

plt.tight_layout()
plt.show()

# ============================================
# ДОПОЛНИТЕЛЬНО: ВИЗУАЛИЗАЦИЯ МОД
# ============================================
fig2, axes = plt.subplots(2, 3, figsize=(12, 6))
axes = axes.flatten()

for n in range(1, 7):  # первые 6 мод
    ax2 = axes[n-1]
    y_mod = np.sin(n * np.pi * x / L)
    ax2.plot(x, y_mod, "b-")
    ax2.axhline(y=0, color="black", linewidth=0.5)
    ax2.set_title(f"Мода n = {n}, частота = {n*c/(2*L):.1f} Гц")
    ax2.set_xlabel("x, м")
    ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\nМетод Фурье — полный успех!")
print(f"Энергия струны содержится в {N_modes} модах колебаний.")