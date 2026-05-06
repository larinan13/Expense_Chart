# Модель расхода
from dataclasses import dataclass
from .category import Category

@dataclass
class Expense:
    """Класс representing расход"""
    id: int
    amount: float          # Сумма в рублях
    category: Category     # Категория расхода
    date: str              # Дата в формате ГГГГ-ММ-ДД
    description: str = ""  # Описание (необязательно)
    
    def to_dict(self) -> dict:
        """Преобразует расход в словарь для JSON"""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category.value,
            "date": self.date,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт расход из словаря JSON"""
        category = Category.from_string(data["category"])
        return cls(
            id=data["id"],
            amount=data["amount"],
            category=category,
            date=data["date"],
            description=data.get("description", "")
        )
