# test_logic.py - Юнит-тесты для блоков 4, 6, 8, 10

import pytest
from logic import classify_operation, calc_income_per_student, calc_financial_result, calc_profit_per_student
from errors import PeriodMismatchError, DataNotReadyError

# ==========================================
# Тесты для Блока 4 (Классификация)
# ==========================================
class MockOperation:
    """Имитация объекта FinancialOperation для тестов"""
    def __init__(self, **kwargs):
        self.is_linked_to_state = kwargs.get('is_linked_to_state', False)
        self.depends_on_students = kwargs.get('depends_on_students', False)
        self.depends_on_pps = kwargs.get('depends_on_pps', False)
        self.has_other_drivers = kwargs.get('has_other_drivers', False)
        self.is_fixed_amount = kwargs.get('is_fixed_amount', False)

def test_block_4_fixed_income_is_group_1():
    """Тест: Фиксированная сумма без зависимостей -> Группа 1"""
    operation = MockOperation(is_linked_to_state=False, depends_on_students=False,
                              depends_on_pps=False, has_other_drivers=False, is_fixed_amount=True)
    assert classify_operation(operation) == "Группа 1"

def test_block_4_student_dependent_is_group_2():
    """Тест: Зависит от студентов -> Группа 2"""
    operation = MockOperation(depends_on_students=True, is_fixed_amount=False)
    assert classify_operation(operation) == "Группа 2"

def test_block_4_unknown_goes_to_manual():
    """Тест: Все зависимости False и сумма не фиксирована -> Ручная проверка"""
    operation = MockOperation(is_linked_to_state=False, depends_on_students=False,
                              depends_on_pps=False, has_other_drivers=False, is_fixed_amount=False)
    assert classify_operation(operation) == "Ручная проверка"


# ==========================================
# Тесты для Блока 6 (Доход на 1 студента)
# ==========================================
def test_block_6_normal_calculation():
    """Тест: Успешный расчет"""
    result = calc_income_per_student(income=1000000, students=200, period_inc="Q1", period_stud="Q1")
    assert result == 5000.0

def test_block_6_zero_students_raises_error():
    """Тест: Защита от деления на ноль"""
    with pytest.raises(ZeroDivisionError):
        calc_income_per_student(income=1000000, students=0, period_inc="Q1", period_stud="Q1")

def test_block_6_period_mismatch_raises_error():
    """Тест: Смешение периодов"""
    with pytest.raises(PeriodMismatchError):
        calc_income_per_student(income=1000000, students=200, period_inc="Q1", period_stud="Q2")


# ==========================================
# Тесты для Блока 8 (Доходы - Расходы)
# ==========================================
def test_block_8_financial_result_calculation():
    """Тест: Расчет финрезультата по группам"""
    result = calc_financial_result(income_g1=100, expense_g1=40, income_g2=200, expense_g2=50)
    assert result.profit_g1 == 60
    assert result.profit_g2 == 150
    assert result.total_profit == 210

def test_block_8_missing_data_raises_error():
    """Тест: Если данные не получены (None)"""
    with pytest.raises(DataNotReadyError):
        calc_financial_result(income_g1=None, expense_g1=40, income_g2=200, expense_g2=50)


# ==========================================
# Тесты для Блока 10 (Прибыль на 1 студента)
# ==========================================
def test_block_10_profit_calculation():
    """Тест: Базовый расчет прибыли на студента"""
    result = calc_profit_per_student(total_profit=100000, students=100, avg_prev=900)
    assert result.profit_per_student == 1000.0
    assert result.is_anomaly == False

def test_block_10_anomaly_detection():
    """Тест: Выявление аномалии (отклонение > 200%)"""
    # Средняя прибыль 1000, а у нас 3000 (отклонение 300%)
    result = calc_profit_per_student(total_profit=300000, students=100, avg_prev=1000)
    assert result.is_anomaly == True

def test_block_10_negative_profit_flag():
    """Тест: Убыточная группа"""
    result = calc_profit_per_student(total_profit=-50000, students=100, avg_prev=1000)
    assert result.profit_per_student == -500.0
    assert result.status == "LOSS"