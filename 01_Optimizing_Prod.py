import pulp as pl

def optimize_beverage_production():
    production = pl.LpProblem("Оптимізація Виробництва напоїв", pl.LpMaximize)

    lemonade = pl.LpVariable("Lemonade", lowBound=0, cat='Integer')     # визначення першоїзмінної
    fruit_juice = pl.LpVariable("Fruit_Juice", lowBound=0, cat='Integer') # визначення другої змінної

    # Функція цілі - максимізуємо прибуток: emonade(L) + fruit_juice(J) -> maximize
    production += pl.lpSum([lemonade, fruit_juice]), "Total_Production"

    # Додаємо всі обмеження з умов
    production += 2 * lemonade + 1 * fruit_juice <= 100, "Обмеження Води"
    production += 1 * lemonade <= 50, "Обмеження по цукру"
    production += 1 * lemonade <= 30, "Обмеження Лимонного соку"
    production += 2 * fruit_juice <= 40, "Обмеження Фруктового пюре"

    production.solve()

    print(f"Статус рішення: {pl.LpStatus[production.status]}")
    print(f"Лимонад (од.): {pl.value(lemonade)}")
    print(f"Фруктовий сік (од.): {pl.value(fruit_juice)}")
    print(f"Всього продуктів: {pl.value(production.objective)}")

if __name__ == "__main__":
    optimize_beverage_production()