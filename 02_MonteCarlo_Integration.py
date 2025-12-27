import numpy as np
import scipy.integrate as sci
import matplotlib.pyplot as plt

# Визначення функції
def f(x):
    return x**2

a = 0  # Нижня межа інтегрування
b = 2  # Верхня межа інтегрування

def monte_carlo_integral(f, a, b, num_samples=10000):
    # 1. Визначаємо межі прямокутника
    # Для x: від a до b
    # Для y: від 0 до максимального значення функції на цьому відрізку
    # (беремо з запасом невелику кількість точок для визначення максимуму)
    x_range = np.linspace(a, b, 1000)
    y_max = max(f(x_range))
    
    # 2. Генеруємо випадкові точки
    x_random = np.random.uniform(a, b, num_samples)
    y_random = np.random.uniform(0, y_max, num_samples)

    # 3. Перевіряємо, які точки потрапили під криву
    under_curve = y_random <= f(x_random)
    points_under_curve = np.sum(under_curve)

    # 4. Обчислюємо площу
    rectangle_area = (b - a) * y_max
    area_ratio = points_under_curve / num_samples
    integral_estimate = rectangle_area * area_ratio

    return integral_estimate, x_random, y_random, under_curve

if __name__ == "__main__":
    # 1. Аналітичне обчислення (SciPy)
    result_quad, error_quad = sci.quad(f, a, b)
    print(f"Аналітичне значення (quad): {result_quad:.5f}")

    # 2. Метод Монте-Карло
    N = 1000  # Кількість точок для візуалізації (менше, щоб не засмічувати графік)
    mc_result, x_rnd, y_rnd, under_curve = monte_carlo_integral(f, a, b, num_samples=N)
    
    # Обчислення похибки
    absolute_error = abs(mc_result - result_quad)
    relative_error = (absolute_error / result_quad) * 100

    print(f"Monte Carlo ({N} точок): {mc_result:.5f}")
    print(f"Похибка: {absolute_error:.5f} ({relative_error:.2f}%)")

    # 3. Побудова графіка
    fig, ax = plt.subplots(figsize=(10, 6))

    # Малювання функції
    x = np.linspace(a - 0.5, b + 0.5, 400)
    y = f(x)
    ax.plot(x, y, "r", linewidth=2, label=f"f(x) = x^2")

    # Малювання випадкових точок
    # Точки під кривою - зелені
    ax.scatter(x_rnd[under_curve], y_rnd[under_curve], color='green', s=10, alpha=0.5, label="Points under curve")
    # Точки над кривою - сині
    ax.scatter(x_rnd[~under_curve], y_rnd[~under_curve], color='blue', s=10, alpha=0.5, label="Points above curve")

    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.5])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=a, color="gray", linestyle="--")
    ax.axvline(x=b, color="gray", linestyle="--")
    
    ax.set_title(f"Метод Монте-Карло: N={N}, Error={relative_error:.2f}%")
    ax.legend()
    plt.grid()
    plt.show()