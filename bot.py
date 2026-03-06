import json
import os
from datetime import datetime

# Назва файлу для збереження даних
DATA_FILE = 'finance_data.json'

def load_data():
    """Зчитує дані з файлу при запуску програми[cite: 27]."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    # Якщо файлу немає, повертаємо початкову структуру
    return {"budget": 0.0, "expenses": []}

def save_data(data):
    """Автоматично оновлює дані у файлі після кожної зміни[cite: 28]."""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def set_budget(data):
    """Встановлює суму бюджету[cite: 29]."""
    try:
        amount = float(input("Введіть суму бюджету: "))
        data["budget"] = amount
        save_data(data)
        print(f"✅ Бюджет успішно встановлено: {amount} грн.")
    except ValueError:
        print("❌ Помилка: введіть числове значення.")

def check_budget(data):     
    """Обчислює залишок та виводить попередження про перевищення[cite: 38, 39, 40, 41]."""
    total_spent = sum(item["amount"] for item in data["expenses"])
    balance = data["budget"] - total_spent
    print(f"💰 Ваш залишок: {balance:.2f} грн.")
    
    if balance < 0:
        print("!!! ПОПЕРЕДЖЕННЯ: Ви перевищили встановлений бюджет! !!!")

def add_expense(data):
    """Додає нову витрату[cite: 30]."""
    try:
        amount = float(input("Сума витрати: "))
        category = input("Категорія: ")
        date_input = input("Дата (РРРР-ММ-ДД) або натисніть Enter для сьогоднішньої: ")
        
        if not date_input:
            date_input = datetime.now().strftime("%Y-%m-%d")
            
        comment = input("Короткий коментар (за бажанням): ")

        expense = {
            "amount": amount,
            "category": category,
            "date": date_input,
            "comment": comment
        }
        
        data["expenses"].append(expense)
        save_data(data)
        print("✅ Витрату успішно додано!")
        
        # Перевірка на перевищення бюджету після додавання
        check_budget(data)
    except ValueError:
        print("❌ Помилка: невірна сума. Спробуйте ще раз.")

def show_expenses(expenses_list):
    """Виводить список переданих витрат[cite: 35]."""
    if not expenses_list:
        print("📭 Витрат не знайдено.")
        return
        
    print("\n--- Список витрат ---")
    for idx, item in enumerate(expenses_list, 1):
        print(f"{idx}. [{item['date']}] {item['category']}: {item['amount']} грн. ({item['comment']})")
    print("---------------------\n")

def filter_expenses(data):
    """Фільтрація витрат за різними критеріями[cite: 35, 36, 37]."""
    print("\nОберіть тип фільтру:")
    print("1. За конкретну дату")
    print("2. За період (між двома датами)")
    print("3. За категорією")
    
    choice = input("Ваш вибір (1/2/3): ")
    
    if choice == '1':
        date = input("Введіть дату (РРРР-ММ-ДД): ")
        filtered = [e for e in data["expenses"] if e["date"] == date]
        show_expenses(filtered)
    elif choice == '2':
        start_date = input("Початкова дата (РРРР-ММ-ДД): ")
        end_date = input("Кінцева дата (РРРР-ММ-ДД): ")
        filtered = [e for e in data["expenses"] if start_date <= e["date"] <= end_date]
        show_expenses(filtered)
    elif choice == '3':
        category = input("Введіть категорію: ").lower()
        filtered = [e for e in data["expenses"] if e["category"].lower() == category]
        show_expenses(filtered)
    else:
        print("❌ Невідомий вибір.")

def category_report(data):
    """Підрахунок загальної суми витрат по кожній категорії[cite: 42]."""
    report = {}
    for item in data["expenses"]:
        cat = item["category"]
        report[cat] = report.get(cat, 0) + item["amount"]
    
    print("\n--- Звіт за категоріями ---")
    if not report:
        print("Витрат ще немає.")
    for cat, total in report.items():
        print(f"🔹 {cat}: {total:.2f} грн.")
    print("---------------------------\n")

def show_help():
    """Виводить список доступних команд[cite: 29]."""
    commands = """
    Доступні команди:
    - допомога: показати це меню
    - встановити бюджет: задати новий ліміт
    - додати витрату: внести нову витрату 
    - показати витрати: вивести всі витрати 
    - фільтр: пошук за датою, періодом або категорією 
    - залишок: перевірити баланс 
    - звіт за категоріями: суми по категоріях 
    - вийти: завершити програму 
    """
    print(commands)

def main():
    """Головна функція програми."""
    data = load_data()
    print("\n👋 Вітаємо! Це ваш 'Фінансовий трекер студента'.")
    show_help()

    while True:
        # Вхідні дані вводяться користувачем 
        command = input("Введіть команду: ").strip().lower()
        
        if command == "встановити бюджет":
            set_budget(data)
        elif command == "додати витрату":
            add_expense(data)
        elif command == "показати витрати":
            show_expenses(data["expenses"])
        elif command == "фільтр":
            filter_expenses(data)
        elif command == "залишок":
            check_budget(data)
        elif command == "звіт за категоріями":
            category_report(data)
        elif command == "допомога":
            show_help()
        elif command == "вийти":
            print("Бувайте! Ваші дані збережено. Завершення роботи програми.")
            break
        else:
            print("❌ Невідома команда. Введіть 'допомога' для списку команд.")

if __name__ == "__main__":
    main()