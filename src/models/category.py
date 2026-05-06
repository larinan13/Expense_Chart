# Модель категорий расходов (перечисление)
from enum import Enum

class Category(Enum):
    """Категории расходов"""
    FOOD = "Еда"
    TRANSPORT = "Транспорт"
    ENTERTAINMENT = "Развлечения"
    SHOPPING = "Покупки"
    BILLS = "Счета"
    OTHER = "Прочее"
    
    @classmethod
    def get_all(cls):
        """Возвращает список всех категорий"""
        return list(cls)
    
    @classmethod
    def from_string(cls, value: str):
        """Преобразует строку в категорию"""
        for cat in cls:
            if cat.value.lower() == value.lower():
                return cat
        raise ValueError(f"Неверная категория. Выберите из: {', '.join([c.value for c in cls])}")
