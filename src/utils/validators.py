# Валидация пользовательского ввода
from datetime import datetime

class Validator:
    """Проверка корректности ввода"""
    
    @staticmethod
    def amount(value: str) -> tuple:
        """Проверка суммы (положительное число, не больше 1 млн)"""
        try:
            amount = float(value)
            if amount <= 0:
                return False, "Сумма должна быть больше 0"
            if amount > 1_000_000:
                return False, "Сумма не может превышать 1 000 000 ₽"
            return True, amount
        except ValueError:
            return False, "Введите корректное число"
    
    @staticmethod
    def date(value: str) -> tuple:
        """Проверка даты (формат ГГГГ-ММ-ДД, не в будущем)"""
        if not value:  # Пустая строка = сегодня
            value = datetime.now().strftime("%Y-%m-%d")
            return True, value
        
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
            if date_obj > datetime.now():
                return False, "Дата не может быть в будущем"
            return True, value
        except ValueError:
            return False, "Неверный формат. Используйте ГГГГ-ММ-ДД"
    
    @staticmethod
    def expense_id(value: str) -> tuple:
        """Проверка ID расхода"""
        try:
            id_val = int(value)
            if id_val <= 0:
                return False, "ID должен быть положительным числом"
            return True, id_val
        except ValueError:
            return False, "Введите число"
    
    @staticmethod
    def period(start: str, end: str) -> tuple:
        """Проверка диапазона дат"""
        valid1, start_date = Validator.date(start)
        if not valid1:
            return False, start_date
        
        valid2, end_date = Validator.date(end)
        if not valid2:
            return False, end_date
        
        start_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_obj = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start_obj > end_obj:
            return False, "Начальная дата не может быть позже конечной"
        
        return True, start_date, end_date
