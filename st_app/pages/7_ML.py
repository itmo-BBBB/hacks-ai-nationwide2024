import streamlit as st
import pandas as pd
import plotly.graph_objects as go
st.write("# ML Results")
age, gender = st.columns(2)
age.write("## Модель, считающая возраст")
gender.write("## Модель, определяющая пол")
age.write(pd.read_csv('help/age_feature.csv'))
gender.write(pd.read_csv('help/gender_feature.csv'))

stats_cont = pd.read_csv('help/v2_stats_cont.csv')
stats_not_cont = pd.read_csv('help/v2_stats_not_cont.csv')

stats_not_cont['numeric_group'] = range(1, len(stats_not_cont) + 1)
stats_cont['numeric_group'] = range(1, len(stats_cont) + 1)

bar = go.Bar(
    x=stats_not_cont['numeric_group'],
    y=stats_not_cont['final_score'],
    opacity=0.75,
    name='Дискретная метрика'
)

line = go.Scatter(
    x=stats_cont['numeric_group'],
    y=stats_cont['final_score'],
    mode='lines+markers',
    name='Кумулятивная метрика'

)

fig = go.Figure(data=[bar, line])

fig.update_layout(
    xaxis_title='Количество просмотренных видео',
    yaxis_title='Итоговая оценка',
    barmode='overlay',
)

new_x_values = [i for i in range(1, 190, 10)]
fig.update_traces(x=new_x_values)
st.write("### Зависимость оценки от количества просмотренных пользователем видео")
st.plotly_chart(fig)
