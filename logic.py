# logic.py - Бизнес-логика блоков 4, 6, 8, 10

from errors import PeriodMismatchError, DataNotReadyError

# ==========================================
# БЛОК 4: Классификация дохода
# ==========================================
def classify_operation(operation):
    """
    Определяет группу дохода по правилам из ТЗ.
    Возвращает: "Группа 1", "Группа 2" или "Ручная проверка"
    """
    # Если зависит от студентов, ППС или других драйверов -> Группа 2
    if operation.depends_on_students or operation.depends_on_pps or operation.has_other_drivers:
        return "Группа 2"
    
    # Если сумма фиксирована -> Группа 1
    if operation.is_fixed_amount:
        return "Группа 1"
    
    # Иначе -> Ручная проверка
    return "Ручная проверка"


# ==========================================
# БЛОК 6: Доход на одного студента
# ==========================================
def calc_income_per_student(income, students, period_inc, period_stud):
    """
    Считает доход на одного студента.
    Проверяет: деление на ноль и совпадение периодов.
    """
    # Проверка 1: студентов должно быть больше 0
    if students <= 0:
        raise ZeroDivisionError("Количество студентов должно быть больше 0")
    
    # Проверка 2: периоды должны совпадать
    if period_inc != period_stud:
        raise PeriodMismatchError(f"Периоды не совпадают: доход={period_inc}, контингент={period_stud}")
    
    # Расчет
    return income / students


# ==========================================
# БЛОК 8: Расчет финрезультата (Доходы - Расходы)
# ==========================================
class FinancialResult:
    """Хранит результаты расчета по группам"""
    def __init__(self, profit_g1, profit_g2, total_profit):
        self.profit_g1 = profit_g1
        self.profit_g2 = profit_g2
        self.total_profit = total_profit

def calc_financial_result(income_g1, expense_g1, income_g2, expense_g2):
    """
    Считает финансовый результат по группам.
    """
    # Проверка: все данные должны быть получены (не None)
    if income_g1 is None or expense_g1 is None or income_g2 is None or expense_g2 is None:
        raise DataNotReadyError("Не все данные получены для расчета")
    
    profit_g1 = income_g1 - expense_g1
    profit_g2 = income_g2 - expense_g2
    total_profit = profit_g1 + profit_g2
    
    return FinancialResult(profit_g1, profit_g2, total_profit)


# ==========================================
# БЛОК 10: Прибыль на одного студента
# ==========================================
class ProfitResult:
    """Хранит результат расчета прибыли на студента"""
    def __init__(self, profit_per_student, is_anomaly, status):
        self.profit_per_student = profit_per_student
        self.is_anomaly = is_anomaly
        self.status = status

def calc_profit_per_student(total_profit, students, avg_prev):
    """
    Считает прибыль на одного студента и проверяет на аномалии.
    Аномалия = отклонение от среднего больше 200%
    """
    # Проверка: студентов должно быть больше 0
    if students <= 0:
        raise ZeroDivisionError("Количество студентов должно быть больше 0")
    
    profit_per_student = total_profit / students
    
    # Проверка на аномалию (отклонение > 200% от среднего)
    is_anomaly = False
    if avg_prev != 0:
        deviation = abs(profit_per_student - avg_prev) / abs(avg_prev)
        if deviation >= 2.0:  # 200%
            is_anomaly = True
    
    # Определяем статус
    if profit_per_student < 0:
        status = "LOSS"
    else:
        status = "PROFIT"
    
    return ProfitResult(profit_per_student, is_anomaly, status)
