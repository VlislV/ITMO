import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import matplotlib


k_obj = 1
k_wall = 1

WIDTH, HEIGHT = 10.0, 8.0

DT = 0.005           # dt
SIMULATION_SPEED = 2.0
STEPS_PER_FRAME = 4

# ПЕРВЫЙ ОБЬЕКТ
m1, r1 = 1.0, 0.5
x1, y1 = 2.0, 2.0
vx1, vy1 = 1, 1

# ВТОРОЙ ОБЬЕКТ
m2, r2 = 2.0, 0.7
x2, y2 = 4.0, 2.0
vx2, vy2 = -1, 0

def check_wall_collision(x, y, vx, vy, r):
    # Левая/правая стенки
    if x - r < 0:
        x = r
        vx = -k_wall * vx
    elif x + r > WIDTH:
        x = WIDTH - r
        vx = -k_wall * vx

    # Нижняя/верхняя стенки
    if y - r < 0:
        y = r
        vy = -k_wall * vy
    elif y + r > HEIGHT:
        y = HEIGHT - r
        vy = -k_wall * vy

    return x, y, vx, vy


def process_object_collision(x1, y1, vx1, vy1, m1, r1,
                              x2, y2, vx2, vy2, m2, r2):
    dx = x2 - x1
    dy = y2 - y1
    dist = np.hypot(dx, dy)

    if dist == 0 or dist >= r1 + r2:
        return vx1, vy1, vx2, vy2  # нет столкновения

    # Нормаль в точке контакта (от 1 к 2)
    nx = dx / dist
    ny = dy / dist

    # Относительная скорость
    dvx = vx1 - vx2
    dvy = vy1 - vy2
    vn = dvx * nx + dvy * ny  # проекция на нормаль

    if vn <= 0:
        return vx1, vy1, vx2, vy2  # тела удаляются

    # Импульс (с учётом k_obj)
    impulse = (1 + k_obj) * vn / (1/m1 + 1/m2)

    vx1_new = vx1 - impulse * nx / m1
    vy1_new = vy1 - impulse * ny / m1
    vx2_new = vx2 + impulse * nx / m2
    vy2_new = vy2 + impulse * ny / m2

    return vx1_new, vy1_new, vx2_new, vy2_new


def resolve_positions(x1, y1, r1, x2, y2, r2):
    dx = x2 - x1
    dy = y2 - y1
    dist = np.hypot(dx, dy)
    if dist == 0 or dist >= r1 + r2:
        return x1, y1, x2, y2

    overlap = (r1 + r2 - dist) / 2
    nx = dx / dist
    ny = dy / dist

    x1 -= overlap * nx
    y1 -= overlap * ny
    x2 += overlap * nx
    y2 += overlap * ny

    x1 = np.clip(x1, r1, WIDTH - r1)
    y1 = np.clip(y1, r1, HEIGHT - r1)
    x2 = np.clip(x2, r2, WIDTH - r2)
    y2 = np.clip(y2, r2, HEIGHT - r2)

    return x1, y1, x2, y2


def update_physics(state):
    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = state

    x1 += vx1 * DT
    y1 += vy1 * DT
    x2 += vx2 * DT
    y2 += vy2 * DT

    x1, y1, vx1, vy1 = check_wall_collision(x1, y1, vx1, vy1, r1)
    x2, y2, vx2, vy2 = check_wall_collision(x2, y2, vx2, vy2, r2)

    vx1_new, vy1_new, vx2_new, vy2_new = process_object_collision(
        x1, y1, vx1, vy1, m1, r1,
        x2, y2, vx2, vy2, m2, r2
    )

    if (vx1_new != vx1 or vy1_new != vy1 or
        vx2_new != vx2 or vy2_new != vy2):
        vx1, vy1 = vx1_new, vy1_new
        vx2, vy2 = vx2_new, vy2_new
        x1, y1, x2, y2 = resolve_positions(x1, y1, r1, x2, y2, r2)

    return [x1, y1, vx1, vy1, x2, y2, vx2, vy2]


state = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]

color1 = '#FF6B6B'
color2 = '#4ECDC4'

trail_length = 100
trail1_x, trail1_y = [], []
trail2_x, trail2_y = [], []

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
ax.set_aspect('equal')
ax.set_facecolor("#3b3b5a")
fig.patch.set_facecolor('#1a1a2e')
ax.grid(True, alpha=0.1)

border = plt.Rectangle((0, 0), WIDTH, HEIGHT, fill=False,
                        color='white', linewidth=2, alpha=0.5)
ax.add_patch(border)

body1 = Circle((x1, y1), r1, color=color1, alpha=0.8, zorder=5)
body2 = Circle((x2, y2), r2, color=color2, alpha=0.8, zorder=5)
ax.add_patch(body1)
ax.add_patch(body2)

trail_line1, = ax.plot([], [], '-', color=color1, lw=1.5, alpha=0.4)
trail_line2, = ax.plot([], [], '-', color=color2, lw=1.5, alpha=0.4)

info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                     color='white', fontfamily='monospace',
                     fontsize=9, verticalalignment='top')
frame_counter = 0

def animate(frame):
    global state, frame_counter, trail1_x, trail1_y, trail2_x, trail2_y

    for _ in range(STEPS_PER_FRAME):
        state = update_physics(state)
        frame_counter += 1

    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = state

    trail1_x.append(x1)
    trail1_y.append(y1)
    trail2_x.append(x2)
    trail2_y.append(y2)
    if len(trail1_x) > trail_length:
        trail1_x.pop(0); trail1_y.pop(0)
        trail2_x.pop(0); trail2_y.pop(0)

    body1.center = (x1, y1)
    body2.center = (x2, y2)
    trail_line1.set_data(trail1_x, trail1_y)
    trail_line2.set_data(trail2_x, trail2_y)

    v1 = np.hypot(vx1, vy1)
    v2 = np.hypot(vx2, vy2)
    E1 = 0.5 * m1 * v1**2
    E2 = 0.5 * m2 * v2**2
    E_total = E1 + E2

    info_text.set_text(
        f'Время: {frame_counter * DT:.2f} с\n'
        f'Тело 1: v={v1:.2f} E={E1:.2f}\n'
        f'Тело 2: v={v2:.2f} E={E2:.2f}\n'
        f'Сумм. энергия: {E_total:.2f}\n'
    )

    return body1, body2, trail_line1, trail_line2, info_text


ani = FuncAnimation(fig, animate, interval=20, blit=True, cache_frame_data=False)

plt.tight_layout()
plt.show()