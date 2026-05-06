#!/usr/bin/env python3
# Модульные тесты для Expense Chart

import unittest
import tempfile
import os
import sys

# Добавляем src в путь для импортов
sys.path.insert(0, 'src')

from models.expense import Expense
from models.category import Category
from utils.validators import Validator
from services.json_storage import JSONStorage
from controllers.expense_controller import ExpenseController

class TestExpense(unittest.TestCase):
    """Тесты модели Expense"""
    
    def test_create_expense(self):
        # Позитивный тест: создание расхода
        expense = Expense(1, 100.50, Category.FOOD, "2024-01-15", "Обед")
        self.assertEqual(expense.amount, 100.50)
        self.assertEqual(expense.category, Category.FOOD)
    
    def test_to_dict(self):
        # Позитивный тест: преобразование в словарь
        expense = Expense(1, 50.00, Category.TRANSPORT, "2024-01-15")
        data = expense.to_dict()
        self.assertEqual(data["amount"], 50.00)
        self.assertEqual(data["category"], "Транспорт")
    
    def test_from_dict(self):
        # Позитивный тест: создание из словаря
        data = {"id": 2, "amount": 200, "category": "Еда", "date": "2024-01-20", "description": ""}
        expense = Expense.from_dict(data)
        self.assertEqual(expense.amount, 200)
        self.assertEqual(expense.category, Category.FOOD)


class TestValidator(unittest.TestCase):
    """Тесты валидации"""
    
    # Позитивные тесты
    def test_valid_amount(self):
        valid, result = Validator.amount("100")
        self.assertTrue(valid)
        self.assertEqual(result, 100)
    
    def test_valid_date(self):
        valid, result = Validator.date("2024-01-15")
        self.assertTrue(valid)
    
    def test_empty_date(self):
        # Пустая дата = сегодня
        valid, result = Validator.date("")
        self.assertTrue(valid)
    
    # Негативные тесты
    def test_negative_amount(self):
        valid, result = Validator.amount("-50")
        self.assertFalse(valid)
        self.assertEqual(result, "Сумма должна быть больше 0")
    
    def test_zero_amount(self):
        valid, _ = Validator.amount("0")
        self.assertFalse(valid)
    
    def test_invalid_amount_text(self):
        valid, _ = Validator.amount("abc")
        self.assertFalse(valid)
    
    def test_invalid_date_format(self):
        valid, _ = Validator.date("15-01-2024")
        self.assertFalse(valid)
    
    def test_future_date(self):
        valid, _ = Validator.date("2099-12-31")
        self.assertFalse(valid)
    
    def test_invalid_id(self):
        valid, _ = Validator.expense_id("abc")
        self.assertFalse(valid)
    
    # Граничные тесты
    def test_min_amount(self):
        valid, result = Validator.amount("0.01")
        self.assertTrue(valid)
        self.assertEqual(result, 0.01)
    
    def test_max_amount(self):
        valid, result = Validator.amount("1000000")
        self.assertTrue(valid)
        self.assertEqual(result, 1000000)
    
    def test_exceed_max(self):
        valid, _ = Validator.amount("1000001")
        self.assertFalse(valid)
    
    def test_date_range_valid(self):
        valid, _, _ = Validator.period("2024-01-01", "2024-12-31")
        self.assertTrue(valid)
    
    def test_date_range_invalid(self):
        valid, result, _ = Validator.period("2024-12-31", "2024-01-01")
        self.assertFalse(valid)
        self.assertEqual(result, "Начальная дата не может быть позже конечной")


class TestStorage(unittest.TestCase):
    """Тесты JSON хранилища"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.storage = JSONStorage(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_save_and_load(self):
        # Позитивный тест: сохранение и загрузка
        expenses = [Expense(1, 100, Category.FOOD, "2024-01-15")]
        self.storage.save(expenses)
        loaded = self.storage.load()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].amount, 100)
    
    def test_load_empty(self):
        # Граничный тест: пустой файл
        loaded = self.storage.load()
        self.assertEqual(loaded, [])


class TestController(unittest.TestCase):
    """Тесты контроллера"""
    
    def setUp(self):
        self.controller = ExpenseController()
        # Очищаем данные для чистоты теста
        self.controller.expenses.clear()
        self.controller._next_id = 1
    
    def test_add_expense(self):
        # Позитивный тест: добавление расхода
        expense = self.controller.add(50, Category.FOOD, "2024-01-15")
        self.assertEqual(len(self.controller.expenses), 1)
        self.assertEqual(expense.amount, 50)
    
    def test_delete_expense(self):
        # Позитивный тест: удаление расхода
        expense = self.controller.add(50, Category.FOOD, "2024-01-15")
        self.assertTrue(self.controller.delete(expense.id))
        self.assertEqual(len(self.controller.expenses), 0)
    
    def test_delete_nonexistent(self):
        # Негативный тест: удаление несуществующего
        self.assertFalse(self.controller.delete(999))
    
    def test_filter_by_category(self):
        # Позитивный тест: фильтрация по категории
        self.controller.add(50, Category.FOOD, "2024-01-15")
        self.controller.add(30, Category.TRANSPORT, "2024-01-16")
        
        food = self.controller.filter_by_category(Category.FOOD)
        self.assertEqual(len(food), 1)
    
    def test_filter_by_period(self):
        # Позитивный тест: фильтрация по периоду
        self.controller.add(50, Category.FOOD, "2024-01-15")
        self.controller.add(30, Category.TRANSPORT, "2024-02-01")
        
        filtered = self.controller.filter_by_period("2024-01-01", "2024-01-31")
        self.assertEqual(len(filtered), 1)
    
    def test_get_total(self):
        # Позитивный тест: подсчёт суммы за период
        self.controller.add(50, Category.FOOD, "2024-01-15")
        self.controller.add(30, Category.TRANSPORT, "2024-01-16")
        
        total = self.controller.get_total("2024-01-01", "2024-01-31")
        self.assertEqual(total, 80)
    
    def test_empty_category_totals(self):
        # Граничный тест: пустые суммы по категориям
        totals = self.controller.get_category_totals()
        self.assertEqual(totals, {})
    
    def test_find_by_id(self):
        # Позитивный тест: поиск по ID
        expense = self.controller.add(100, Category.FOOD, "2024-01-15")
        found = self.controller.find_by_id(expense.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.amount, 100)
    
    def test_find_by_id_not_found(self):
        # Негативный тест: поиск несуществующего ID
        found = self.controller.find_by_id(999)
        self.assertIsNone(found)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("ЗАПУСК ТЕСТОВ")
    print("=" * 50)
    unittest.main(verbosity=2)
