#!/usr/bin/env python3

import sys
from controllers.expense_controller import ExpenseController
from views.console_view import ConsoleView
from services.chart_generator import ChartGenerator
from utils.validators import Validator
from models.category import Category

class ExpenseApp:
    """Главный класс приложения"""
    
    def __init__(self):
        self.controller = ExpenseController()
        self.view = ConsoleView()
        self.chart = ChartGenerator()
        self.running = True
    
    def run(self):
        """Запуск главного цикла"""
        self.view.success("Expense Chart запущен!")
        
        while self.running:
            self.view.show_menu()
            choice = input("\nВаш выбор: ").strip()
            self._handle_choice(choice)
            if choice != "9":
                self.view.wait()
                self.view.clear()
    
    def _handle_choice(self, choice: str):
        """Обработка выбора пользователя"""
        handlers = {
            "1": self._add_expense,
            "2": self._show_all,
            "3": self._delete_expense,
            "4": self._filter_by_category,
            "5": self._filter_by_period,
            "6": self._total_for_period,
            "7": self._bar_chart,
            "8": self._pie_chart,
            "9": self._exit,
        }
        
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            self.view.error("Неверный выбор")
    
    def _add_expense(self):
        """Добавление расхода"""
        # Ввод суммы
        amount_str = self.view.get_amount()
        valid, result = Validator.amount(amount_str)
        if not valid:
            self.view.error(result)
            return
        amount = result
        
        # Ввод категории
        cat_input = self.view.get_category()
        try:
            if cat_input.isdigit():
                idx = int(cat_input) - 1
                categories = Category.get_all()
                if 0 <= idx < len(categories):
                    category = categories[idx]
                else:
                    raise ValueError
            else:
                category = Category.from_string(cat_input)
        except:
            self.view.error("Неверная категория")
            return
        
        # Ввод даты
        date_str = self.view.get_date()
        valid, result = Validator.date(date_str)
        if not valid:
            self.view.error(result)
            return
        date = result
        
        # Ввод описания
        desc = self.view.get_description()
        
        expense = self.controller.add(amount, category, date, desc)
        self.view.success(f"Расход {expense.amount:.2f} ₽ добавлен (ID: {expense.id})")
    
    def _show_all(self):
        """Показать все расходы"""
        expenses = self.controller.get_all()
        self.view.show_expenses(expenses)
    
    def _delete_expense(self):
        """Удалить расход"""
        id_str = self.view.get_expense_id()
        valid, expense_id = Validator.expense_id(id_str)
        if not valid:
            self.view.error(expense_id)
            return
        
        expense = self.controller.find_by_id(expense_id)
        if not expense:
            self.view.error(f"Расход с ID {expense_id} не найден")
            return
        
        self.view.show_expenses([expense], "Расход для удаления")
        if self.view.get_yes_no("Удалить этот расход?"):
            if self.controller.delete(expense_id):
                self.view.success(f"Расход {expense_id} удалён")
    
    def _filter_by_category(self):
        """Фильтр по категории"""
        cat_input = self.view.get_category()
        try:
            if cat_input.isdigit():
                idx = int(cat_input) - 1
                category = Category.get_all()[idx]
            else:
                category = Category.from_string(cat_input)
        except:
            self.view.error("Неверная категория")
            return
        
        expenses = self.controller.filter_by_category(category)
        self.view.show_expenses(expenses, f"Категория: {category.value}")
        totals = {category.value: sum(e.amount for e in expenses)}
        self.view.show_category_totals(totals)
    
    def _filter_by_period(self):
        """Фильтр по периоду"""
        start, end = self.view.get_period()
        
        if not start or not end:
            self.view.error("Введите обе даты")
            return
        
        valid, start_date, end_date = Validator.period(start, end)
        if not valid:
            self.view.error(start_date)
            return
        
        expenses = self.controller.filter_by_period(start_date, end_date)
        self.view.show_expenses(expenses, f"Период: {start_date} - {end_date}")
    
    def _total_for_period(self):
        """Сумма расходов за период"""
        start, end = self.view.get_period()
        
        if not start or not end:
            self.view.error("Введите обе даты")
            return
        
        valid, start_date, end_date = Validator.period(start, end)
        if not valid:
            self.view.error(start_date)
            return
        
        total = self.controller.get_total(start_date, end_date)
        totals = self.controller.get_category_totals(start_date, end_date)
        
        print(f"\n Сумма расходов за период {start_date} - {end_date}: {total:.2f} ₽")
        self.view.show_category_totals(totals)
    
    def _bar_chart(self):
        """Показать столбчатую диаграмму"""
        if self.view.get_yes_no("За период?"):
            start, end = self.view.get_period()
            if start and end:
                valid, start_date, end_date = Validator.period(start, end)
                if valid:
                    totals = self.controller.get_category_totals(start_date, end_date)
                    title = f"Расходы по категориям ({start_date} - {end_date})"
                else:
                    self.view.error(start_date)
                    return
            else:
                totals = self.controller.get_category_totals()
                title = "Все расходы по категориям"
        else:
            totals = self.controller.get_category_totals()
            title = "Все расходы по категориям"
        
        self.chart.bar_chart(totals, title)
    
    def _pie_chart(self):
        """Показать круговую диаграмму"""
        totals = self.controller.get_category_totals()
        self.chart.pie_chart(totals, "Распределение расходов")
    
    def _exit(self):
        """Выход из приложения"""
        self.view.success("Данные сохранены. До свидания!")
        self.running = False

def main():
    """Точка входа"""
    try:
        app = ExpenseApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nДо свидания!")
        sys.exit(0)
    except Exception as e:
        print(f"\n Непредвиденная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
