# Работа с JSON файлом (сохранение и загрузка)
import json
import os
from typing import List
from models.expense import Expense

class JSONStorage:
    """Хранилище данных в JSON файле"""
    
    def __init__(self, filename: str = "expenses.json"):
        self.filename = filename
    
    def save(self, expenses: List[Expense]) -> bool:
        """Сохраняет расходы в файл"""
        try:
            data = [e.to_dict() for e in expenses]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def load(self) -> List[Expense]:
        """Загружает расходы из файла"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [Expense.from_dict(item) for item in data]
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return []
