import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Загрузка данных из CSV файла
@st.cache
def load_data(file):
    data = pd.read_csv(file)
    return data

# Отображение загруженных данных
def display_data(data):
    st.write("Статистика:", data)

# Проверка гипотез
def hypothesis_testing(data, age_threshold, work_days_threshold):
    # Разделение данных на группы по возрасту и полу
    older_employees = data[(data['Возраст'] > age_threshold) & (data['Количество больничных дней'] > work_days_threshold)]
    younger_employees = data[data['Возраст'] <= age_threshold & (data['Количество больничных дней'] > work_days_threshold)]
    male_employees = data[(data['Количество больничных дней'] == 'М') & (data['Количество больничных дней'] > work_days_threshold)]
    female_employees = data[(data['Количество больничных дней'] == 'Ж') & (data['Количество больничных дней'] > work_days_threshold)]

    # Проверка первой гипотезы
    _, pvalue_gender = ttest_ind(male_employees['Количество больничных дней'], female_employees['Количество больничных дней'])
    gender_hypothesis_result = "Мужчины пропускают значимо больше рабочих дней" if pvalue_gender < 0.05 else "Нет значимой разницы между мужчинами и женщинами"

    # Проверка второй гипотезы
    _, pvalue_age = ttest_ind(older_employees['Количество больничных дней'], younger_employees['Количество больничных дней'])
    age_hypothesis_result = "Старшие сотрудники пропускают значимо больше рабочих дней" if pvalue_age < 0.05 else "Нет значимой разницы между старшими и молодыми сотрудниками"

    return gender_hypothesis_result, age_hypothesis_result

# Отображение результатов проверки гипотез
def display_results(gender_result, age_result):
    st.write("Результаты проверки гипотез:")
    st.write("1) Мужчины пропускают в течение года более 2 рабочих дней по болезни:")
    st.write(gender_result)
    st.write("2) Работники старше 35 лет пропускают в течение года более 2 рабочих дней по болезни:")
    st.write(age_result)

# Загрузка данных
data_file = st.file_uploader("Выберите файл CSV", type="csv")
if data_file is not None:
    data = load_data(data_file)
    display_data(data)

    # Настройка параметров
    age_threshold = st.number_input("Порог возраста")
    work_days_threshold = st.number_input("Порог рабочих дней", value=2)

    # Проверка гипотез
    gender_result, age_result = hypothesis_testing(data, age_threshold, work_days_threshold)

    # Отображение результатов
    display_results(gender_result, age_result)