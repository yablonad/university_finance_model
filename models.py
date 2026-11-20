from sqlalchemy import Column, String, Float, Integer, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FinancialOperation(Base):
    __tablename__ = 'financial_operations'
    
    operation_id = Column(String, primary_key=True)
    group_id = Column(String)
    period_id = Column(String)
    operation_type = Column(String)
    amount = Column(Float)
    contingent_type = Column(String)
    
    is_linked_to_state = Column(Boolean, default=False)
    depends_on_students = Column(Boolean, default=False)
    depends_on_pps = Column(Boolean, default=False)
    has_other_drivers = Column(Boolean, default=False)
    is_fixed_amount = Column(Boolean, default=False)

class StudentCohort(Base):
    __tablename__ = 'student_cohorts'
    
    group_id = Column(String, primary_key=True)
    period_id = Column(String, primary_key=True)
    contingent_type = Column(String)
    student_count = Column(Integer)

class HistoricalMetrics(Base):
    __tablename__ = 'historical_metrics'
    
    period_id = Column(String, primary_key=True)
    group_id = Column(String, primary_key=True)
    avg_profit_per_student_all = Column(Float)
    prev_profit_per_student = Column(Float)

class CalculationResult(Base):
    __tablename__ = 'calculation_results'
    
    calculation_id = Column(String, primary_key=True)
    group_id = Column(String)
    period_id = Column(String)
    
    income_g1 = Column(Float, default=0.0)
    income_g2 = Column(Float, default=0.0)
    expense_g1 = Column(Float, default=0.0)
    expense_g2 = Column(Float, default=0.0)
    total_profit = Column(Float, default=0.0)
    
    income_per_student = Column(Float, default=0.0)
    profit_per_student = Column(Float, default=0.0)
    
    is_anomaly = Column(Boolean, default=False)
    calculation_status = Column(String, default="SUCCESS")
    error_message = Column(String, nullable=True)
