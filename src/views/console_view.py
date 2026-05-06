# Представление - работа с консолью (ввод/вывод)
import os
from typing import List
from models.expense import Expense
from models.category import Category

class ConsoleView:
    """Отображение интерфейса в консоли"""
    
    @staticmethod
    def clear():
        """Очищает экран"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def show_menu():
        """Показывает главное меню"""
        print("\n" + "=" * 50)
        print("        EXPENSE CHART - Финансовый трекер")
        print("=" * 50)
        print("1.  Добавить расход")
        print("2.  Все расходы")
        print("3.  Удалить расход")
        print("4.  Фильтр по категории")
        print("5.  Фильтр по периоду")
        print("6.  Сумма за период")
        print("7.  Столбчатая диаграмма")
        print("8.  Круговая диаграмма")
        print("9.  Выход")
        print("=" * 50)
    
    @staticmethod
    def show_expenses(expenses: List[Expense], title: str = "Расходы"):
        """Показывает список расходов в таблице"""
        print(f"\n {title}:")
        if not expenses:
            print("   Расходов нет")
            return
        
        print("-" * 70)
        print(f"{'ID':<4} {'Дата':<12} {'Сумма':<12} {'Категория':<15} Описание")
        print("-" * 70)
        for e in expenses:
            print(f"{e.id:<4} {e.date:<12} {e.amount:>10.2f} ₽  {e.category.value:<12} {e.description[:35]}")
        print("-" * 70)
        total = sum(e.amount for e in expenses)
        print(f"Итого: {total:.2f} ₽  ({len(expenses)} записей)")
    
    @staticmethod
    def show_category_totals(totals: dict):
        """Показывает суммы по категориям"""
        print("\n Суммы по категориям:")
        print("-" * 35)
        for cat, amount in totals.items():
            print(f"   {cat:<12}: {amount:>10.2f} ₽")
        print("-" * 35)
        print(f"   {'ВСЕГО':<12}: {sum(totals.values()):>10.2f} ₽")
    
    # Методы для ввода данных
    @staticmethod
    def get_amount() -> str:
        return input("Сумма (₽): ").strip()
    
    @staticmethod
    def get_category() -> str:
        print("\nКатегории:")
        for i, cat in enumerate(Category.get_all(), 1):
            print(f"   {i}. {cat.value}")
        return input("Выберите (номер или название): ").strip()
    
    @staticmethod
    def get_date() -> str:
        return input("Дата (ГГГГ-ММ-ДД, Enter - сегодня): ").strip()
    
    @staticmethod
    def get_description() -> str:
        return input("Описание (необязательно): ").strip()
    
    @staticmethod
    def get_expense_id() -> str:
        return input("ID расхода: ").strip()
    
    @staticmethod
    def get_period() -> tuple:
        start = input("Начальная дата (ГГГГ-ММ-ДД): ").strip()
        end = input("Конечная дата (ГГГГ-ММ-ДД): ").strip()
        return start, end
    
    @staticmethod
    def get_yes_no(prompt: str) -> bool:
        response = input(f"{prompt} (y/n): ").strip().lower()
        return response == 'y'
    
    # Сообщения
    @staticmethod
    def success(msg: str):
        print(f"\n {msg}")
    
    @staticmethod
    def error(msg: str):
        print(f"\n Ошибка: {msg}")
    
    @staticmethod
    def wait():
        input("\nНажмите Enter для продолжения...")
