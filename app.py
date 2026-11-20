# app.py - Веб-интерфейс для модели эффективности университета

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from logic import classify_operation, calc_income_per_student, calc_financial_result, calc_profit_per_student

# ==========================================
# Настройка страницы
# ==========================================
st.set_page_config(page_title="Модель эффективности университета", layout="wide")
st.title(" Модель эффективности финансирования университета")
st.markdown("---")

# ==========================================
# Боковая панель: ввод параметров
# ==========================================
st.sidebar.header(" Параметры моделирования")

# Ввод количества студентов
num_students = st.sidebar.slider(
    "Количество студентов в группе:",
    min_value=5,
    max_value=50,
    value=25,
    step=1
)

# Ввод типа группы
group_type = st.sidebar.selectbox(
    "Тип группы:",
    ["Бюджетная", "Платная", "Смешанная"]
)

# Ввод стоимости обучения (для платных)
tuition_fee = st.sidebar.number_input(
    "Стоимость обучения (руб/год):",
    min_value=0,
    value=300000,
    step=50000
)

# Ввод госбюджета на студента
state_budget = st.sidebar.number_input(
    "Госбюджет на 1 студента (руб/год):",
    min_value=0,
    value=150000,
    step=10000
)

# Ввод расходов
expenses = st.sidebar.number_input(
    "Расходы на группу (руб/год):",
    min_value=0,
    value=2000000,
    step=100000
)

st.sidebar.markdown("---")
st.sidebar.info(" Меняйте параметры слева, чтобы увидеть результат справа")

# ==========================================
# Основной экран: расчет и отображение
# ==========================================
st.header(" Расчет финансовой эффективности")

# Кнопка расчета
if st.button(" Рассчитать"):
    
    # Расчет доходов
    if group_type == "Бюджетная":
        total_income = state_budget * num_students
    elif group_type == "Платная":
        total_income = tuition_fee * num_students
    else:  # Смешанная
        budget_students = num_students // 2
        paid_students = num_students - budget_students
        total_income = (state_budget * budget_students) + (tuition_fee * paid_students)
    
    # Расчет прибыли
    total_profit = total_income - expenses
    
    # Расчет на одного студента
    income_per_student = total_income / num_students if num_students > 0 else 0
    profit_per_student = total_profit / num_students if num_students > 0 else 0
    
    # Отображение результатов в метриках
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Общий доход", f"{total_income:,.0f} руб")
    with col2:
        st.metric("Общие расходы", f"{expenses:,.0f} руб")
    with col3:
        st.metric("Прибыль группы", f"{total_profit:,.0f} руб", 
                  delta=f"{profit_per_student:,.0f} руб/студ")
    with col4:
        st.metric("Доход на студента", f"{income_per_student:,.0f} руб")
    
    st.markdown("---")
    
    # ==========================================
    # Графики
    # ==========================================
    st.header(" Визуализация результатов")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Структура доходов и расходов")
        
        # Круговая диаграмма
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Доходы', 'Расходы'],
            values=[total_income, expenses],
            marker=dict(colors=['#00CC96', '#EF553B'])
        )])
        fig_pie.update_layout(title="Доходы vs Расходы")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_chart2:
        st.subheader("Прибыль на одного студента")
        
        # Столбчатая диаграмма
        fig_bar = go.Figure(data=[go.Bar(
            x=['Прибыль на студента'],
            y=[profit_per_student],
            marker=dict(color=['#636EFA' if profit_per_student >= 0 else '#EF553B'])
        )])
        fig_bar.update_layout(
            title="Финансовый результат",
            yaxis_title="Рубли"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # ==========================================
    # Таблица с детализацией
    # ==========================================
    st.markdown("---")
    st.header("📋 Детализация расчета")
    
    # Создаем DataFrame для таблицы
    df = pd.DataFrame({
        'Показатель': [
            'Количество студентов',
            'Тип группы',
            'Общий доход',
            'Общие расходы',
            'Прибыль группы',
            'Доход на 1 студента',
            'Прибыль на 1 студента'
        ],
        'Значение': [
            f"{num_students} чел",
            group_type,
            f"{total_income:,.0f} руб",
            f"{expenses:,.0f} руб",
            f"{total_profit:,.0f} руб",
            f"{income_per_student:,.0f} руб",
            f"{profit_per_student:,.0f} руб"
        ]
    })
    
    st.dataframe(df, use_container_width=True)
    
    # ==========================================
    # Анализ эффективности
    # ==========================================
    st.markdown("---")
    st.header(" Анализ эффективности")
    
    if total_profit > 0:
        st.success(f"Группа эффективна! Прибыль составляет {total_profit:,.0f} руб")
        st.info(f" Каждый студент приносит {profit_per_student:,.0f} руб прибыли")
    else:
        st.error(f" Группа убыточна! Убыток составляет {abs(total_profit):,.0f} руб")
        st.warning(f" Каждый студент убыточен на {abs(profit_per_student):,.0f} руб")
        
        # Рекомендация по минимальному количеству студентов
        if expenses > 0 and (group_type == "Платная" or group_type == "Смешанная"):
            min_students = int(expenses / tuition_fee) + 1
            st.info(f" Для безубыточности нужно минимум **{min_students} студентов** по {tuition_fee:,.0f} руб")

else:
    st.info(" Настройте параметры слева и нажмите кнопку 'Рассчитать'")

# ==========================================
# Подвал
# ==========================================
st.markdown("---")
st.caption("Модель эффективности финансирования университета | 2026")