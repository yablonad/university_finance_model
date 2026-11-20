# errors.py - Наши собственные ошибки

class PeriodMismatchError(Exception):
    """Периоды дохода и контингента не совпадают"""
    pass

class ContingentMixingError(Exception):
    """Смешение бюджетных и платных студентов"""
    pass

class DuplicateOperationError(Exception):
    """Найден двойной учёт операций"""
    pass

class ClassificationPendingError(Exception):
    """Данные не классифицированы (нужен Блок 4)"""
    pass

class DataNotReadyError(Exception):
    """Не выполнены предварительные блоки (8 перед 10)"""
    pass
