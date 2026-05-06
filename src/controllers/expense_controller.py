# Контроллер - бизнес-логика приложения
from typing import List, Optional
from models.expense import Expense
from models.category import Category
from services.json_storage import JSONStorage

class ExpenseController:
    """Управление расходами"""
    
    def __init__(self):
        self.storage = JSONStorage()
        self.expenses = self.storage.load()
        self._next_id = max([e.id for e in self.expenses], default=0) + 1
    
    def add(self, amount: float, category: Category, date: str, desc: str = "") -> Expense:
        """Добавляет новый расход"""
        expense = Expense(self._next_id, amount, category, date, desc)
        self.expenses.append(expense)
        self._next_id += 1
        self.storage.save(self.expenses)
        return expense
    
    def delete(self, expense_id: int) -> bool:
        """Удаляет расход по ID"""
        for i, e in enumerate(self.expenses):
            if e.id == expense_id:
                self.expenses.pop(i)
                self.storage.save(self.expenses)
                return True
        return False
    
    def get_all(self) -> List[Expense]:
        """Возвращает все расходы, сортированные по дате (новые сверху)"""
        return sorted(self.expenses, key=lambda x: x.date, reverse=True)
    
    def filter_by_category(self, category: Category) -> List[Expense]:
        """Фильтр по категории"""
        return [e for e in self.expenses if e.category == category]
    
    def filter_by_period(self, start: str, end: str) -> List[Expense]:
        """Фильтр по диапазону дат"""
        return [e for e in self.expenses if start <= e.date <= end]
    
    def get_total(self, start: str, end: str) -> float:
        """Сумма расходов за период"""
        return sum(e.amount for e in self.filter_by_period(start, end))
    
    def get_category_totals(self, start: str = None, end: str = None) -> dict:
        """Суммы расходов по категориям за период"""
        if start and end:
            expenses = self.filter_by_period(start, end)
        else:
            expenses = self.expenses
        
        totals = {}
        for cat in Category.get_all():
            total = sum(e.amount for e in expenses if e.category == cat)
            if total > 0:
                totals[cat.value] = total
        return totals
    
    def find_by_id(self, expense_id: int) -> Optional[Expense]:
        """Находит расход по ID"""
        for e in self.expenses:
            if e.id == expense_id:
                return e
        return None
