from abc import ABC, abstractmethod
from typing import Callable, Tuple, List, Optional
import numpy as np
import pandas as pd
from tabulate import tabulate
from typing import Callable, Tuple, List, Optional, Union, Dict
import sympy as sp
import math
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib import cm

# ИНТЕРФЕЙСЫ

class OptimizableFunction(ABC):
    @abstractmethod
    def __call__(self, x: np.ndarray) -> float:
        pass

    @abstractmethod
    def gradient(self, x: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def hessian(self, x: np.ndarray) -> np.ndarray:
        pass


class LineSearchMethod(ABC):
    @abstractmethod
    def search(self, f: Callable[[float], float], a: float, b: float, eps: float) -> float:
        pass


class OptimizationMethod(ABC):
    def __init__(self, func: OptimizableFunction, eps: float = 1e-4):
        self.func = func
        self.eps = eps
        self._history: List[np.ndarray] = []
        self._values: List[float] = []

    @abstractmethod
    def step(self, x: np.ndarray) -> np.ndarray:
        pass

    def minimize(self, x0: np.ndarray, max_iter: int = 1000) -> Tuple[np.ndarray, List[np.ndarray], List[float]]:
        x_curr = x0.copy()
        self._history = [x_curr.copy()]
        self._values = [self.func(x_curr)]

        for _ in range(max_iter):
            x_prev = x_curr.copy()
            x_curr = self.step(x_curr)
            self._history.append(x_curr.copy())
            self._values.append(self.func(x_curr))

            if np.linalg.norm(x_curr - x_prev) < self.eps:
                break

        return x_curr, self._history, self._values

    def get_history(self) -> List[np.ndarray]:
        return self._history

    def get_values(self) -> List[float]:
        return self._values

#РЕАЛИЗАЦИИ ИНТЕРФЕЙСОВ

class HalfDivisionSearch(LineSearchMethod):
    def search(self, f: Callable[[float], float], a: float, b: float, eps: float = 1e-6) -> float:
        delta = eps / 2
        while (b - a) > eps * 2:
            x_mid = (a + b) / 2
            x1 = max(a, x_mid - delta)
            x2 = min(b, x_mid + delta)
            f1, f2 = f(x1), f(x2)
            if f1 < f2:
                b = x2
            else:
                a = x1
        return (a + b) / 2


class Function2D(OptimizableFunction):
    def __init__(self, f_expr: str, var_names: Tuple[str, str] = ("x1", "x2")):
        self.var_names = var_names
        self.x1 = sp.Symbol(var_names[0])
        self.x2 = sp.Symbol(var_names[1])

        self.f_expr = sp.sympify(f_expr)

        self.f_x1_expr = sp.diff(self.f_expr, self.x1)
        self.f_x2_expr = sp.diff(self.f_expr, self.x2)

        self.f_x1x1_expr = sp.diff(self.f_x1_expr, self.x1)
        self.f_x1x2_expr = sp.diff(self.f_x1_expr, self.x2)
        self.f_x2x2_expr = sp.diff(self.f_x2_expr, self.x2)

        self.f = sp.lambdify((self.x1, self.x2), self.f_expr, modules=["numpy", "math"])
        self.grad_x1 = sp.lambdify((self.x1, self.x2), self.f_x1_expr, modules=["numpy", "math"])
        self.grad_x2 = sp.lambdify((self.x1, self.x2), self.f_x2_expr, modules=["numpy", "math"])
        self.hess_x1x1 = sp.lambdify((self.x1, self.x2), self.f_x1x1_expr, modules=["numpy", "math"])
        self.hess_x1x2 = sp.lambdify((self.x1, self.x2), self.f_x1x2_expr, modules=["numpy", "math"])
        self.hess_x2x2 = sp.lambdify((self.x1, self.x2), self.f_x2x2_expr, modules=["numpy", "math"])

    def __call__(self, x: np.ndarray) -> float:
        return float(self.f(x[0], x[1]))

    def gradient(self, x: np.ndarray) -> np.ndarray:
        return np.array([
            float(self.grad_x1(x[0], x[1])),
            float(self.grad_x2(x[0], x[1]))
        ])

    def hessian(self, x: np.ndarray) -> np.ndarray:
        return np.array([
            [float(self.hess_x1x1(x[0], x[1])), float(self.hess_x1x2(x[0], x[1]))],
            [float(self.hess_x1x2(x[0], x[1])), float(self.hess_x2x2(x[0], x[1]))]
        ])

#КОНКРЕТНЫЕ МЕТОДЫ ОПТИМИЗАЦИИ

class CoordinateDescent(OptimizationMethod):
    def __init__(self, func: OptimizableFunction, eps: float = 1e-4,
                 line_search: LineSearchMethod = None, bounds: Tuple[float, float] = (-100, 100)):
        super().__init__(func, eps)
        self.bounds = bounds
        self.line_search = line_search if line_search else HalfDivisionSearch()

    def step(self, x: np.ndarray) -> np.ndarray:
        x_new = x.copy()

        g1 = lambda t: self.func(np.array([t, x_new[1]]))
        x_new[0] = self.line_search.search(g1, self.bounds[0], self.bounds[1], self.eps / 10)

        g2 = lambda t: self.func(np.array([x_new[0], t]))
        x_new[1] = self.line_search.search(g2, self.bounds[0], self.bounds[1], self.eps / 10)

        return x_new


class GradientDescent(OptimizationMethod):
    def __init__(self, func: OptimizableFunction, eps: float = 1e-4, learning_rate: float = 0.1):
        super().__init__(func, eps)
        self.learning_rate = learning_rate

    def step(self, x: np.ndarray) -> np.ndarray:
        grad = self.func.gradient(x)
        return x - self.learning_rate * grad


class SteepestDescent(OptimizationMethod):
    def __init__(self, func: OptimizableFunction, eps: float = 1e-4,
                 line_search: LineSearchMethod = None, bounds: Tuple[float, float] = (0, 10)):
        super().__init__(func, eps)
        self.bounds = bounds
        self.line_search = line_search if line_search else HalfDivisionSearch()

    def step(self, x: np.ndarray) -> np.ndarray:
        grad = self.func.gradient(x)
        grad_norm = np.linalg.norm(grad)

        if grad_norm < self.eps:
            return x

        direction = -grad / grad_norm
        g = lambda eta: self.func(x + eta * direction)
        eta_opt = self.line_search.search(g, self.bounds[0], self.bounds[1], self.eps / 10)

        return x + eta_opt * direction

#КЛАССЫ ДЛЯ ВИЗУАЛИЗАЦИИ

class OptimizationVisualizer:
    def __init__(self, func: OptimizableFunction):
        self.func = func

    def plot_history(self, title: str, history: List[np.ndarray], bounds: Optional[Tuple] = None):
        points = np.array(history)
        values = [self.func(p) for p in points]

        if bounds is None:
            x_min, x_max = points[:, 0].min(), points[:, 0].max()
            y_min, y_max = points[:, 1].min(), points[:, 1].max()
            pad_x = max(0.5, (x_max - x_min) * 0.2)
            pad_y = max(0.5, (y_max - y_min) * 0.2)
            bounds = (x_min - pad_x, x_max + pad_x, y_min - pad_y, y_max + pad_y)

        x_min, x_max, y_min, y_max = bounds
        x = np.linspace(x_min, x_max, 200)
        y = np.linspace(y_min, y_max, 200)
        X, Y = np.meshgrid(x, y)

        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = self.func([X[i, j], Y[i, j]])

        fig, ax = plt.subplots(figsize=(12, 9))

        levels = sorted(set(values))
        if len(levels) >= 2:
            contour = ax.contour(X, Y, Z, levels=levels, cmap='viridis', alpha=0.7, linewidths=1.5)
            ax.clabel(contour, inline=True, fontsize=9, fmt='%.2f')

        ax.plot(points[:, 0], points[:, 1], 'r.-', linewidth=2, markersize=6, label='Траектория')

        for i, (x, y) in enumerate(points):
            ax.annotate(str(i), (x, y), xytext=(8, 8), textcoords='offset points',
                       fontsize=9, fontweight='bold', color='darkblue',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

        ax.set_xlabel('x₁', fontsize=12)
        ax.set_ylabel('x₂', fontsize=12)
        ax.set_title(f'{title}\nИтераций: {len(points)-1} | f(x*) = {values[-1]:.6f}', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

class ResultComparator:
    @staticmethod
    def compare(methods: dict, x0: np.ndarray) -> pd.DataFrame:
        results = []
        for name, method in methods.items():
            x_opt, history, values = method.minimize(x0)
            results.append({
                'Метод': name,
                'x*': f"({x_opt[0]:.6f}, {x_opt[1]:.6f})",
                'f(x*)': f"{values[-1]:.6f}",
                'Итераций': len(history) - 1,
                'Норма градиента': f"{np.linalg.norm(method.func.gradient(x_opt)):.2e}"
            })
        return pd.DataFrame(results)

def main():
    func_expr = "x1**3 - 3*x1 + x2**3 + x2**2 - x2 - 3"
    x0 = np.array([0.5, 0.5])

    f = Function2D(func_expr)

    methods = {
        "Покоординатный спуск": CoordinateDescent(f, eps=0.0001),
        "Градиентный спуск": GradientDescent(f, eps=0.0001, learning_rate=0.1),
        "Наискорейший спуск": SteepestDescent(f, eps=0.0001),
    }

    visualizer = OptimizationVisualizer(f)

    for name, method in methods.items():
        x_opt, history, values = method.minimize(x0)
        print(f"\n{name}:")
        print(f"  x* = ({x_opt[0]:.6f}, {x_opt[1]:.6f})")
        print(f"  f(x*) = {values[-1]:.6f}")
        print(f"  Итераций: {len(history)-1}")
        visualizer.plot_history(name, history)

    print("\n" + "=" * 50)
    print("СРАВНЕНИЕ МЕТОДОВ")
    print("=" * 50)
    print(ResultComparator.compare(methods, x0).to_string(index=False))


if __name__ == "__main__":
    main()