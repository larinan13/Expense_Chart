# Генерация графиков с помощью matplotlib
import matplotlib.pyplot as plt

class ChartGenerator:
    """Генератор графиков"""
    
    @staticmethod
    def _setup_font():
        """Настройка шрифта для русского текста"""
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
    
    @staticmethod
    def bar_chart(category_totals: dict, title: str = "Расходы по категориям"):
        """Создаёт столбчатую диаграмму"""
        if not category_totals:
            print("Нет данных для отображения")
            return
        
        ChartGenerator._setup_font()
        
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, amounts, color='steelblue', edgecolor='black')
        
        # Подписи значений на столбцах
        for bar, amount in zip(bars, amounts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(amounts)*0.01,
                    f'{amount:.2f} ₽', ha='center', va='bottom')
        
        plt.xlabel('Категория', fontsize=12)
        plt.ylabel('Сумма (₽)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def pie_chart(category_totals: dict, title: str = "Распределение расходов"):
        """Создаёт круговую диаграмму"""
        if not category_totals:
            print("Нет данных для отображения")
            return
        
        ChartGenerator._setup_font()
        
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.show()
