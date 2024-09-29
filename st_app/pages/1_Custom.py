import streamlit as st
import pandas as pd
import utilities
import plotly.express as px
@st.cache_data
def filter_dataset(data, gender=None, category=None, age=None, device=None,
                   client_type=None, os=None, browser=None, region=None,
                   min_duration=None, max_duration=None,
                   min_watchtime=None, max_watchtime=None, min_videos_per_day=None,
                   max_videos_per_day=None, min_videos=None, max_videos=None):
    # Start with the full dataset
    filtered_data = data.copy()

    # Apply filters
    if gender:
        filtered_data = filtered_data[filtered_data['sex'].isin(gender)]
    if category:
        filtered_data = filtered_data[filtered_data['category'].isin(category)]
    if age:
        filtered_data = filtered_data[filtered_data['age_class'].isin(age)]
    if device:
        filtered_data = filtered_data[filtered_data['ua_device_type'].isin(device)]
    if client_type:
        filtered_data = filtered_data[filtered_data['ua_client_type'].isin(client_type)]
    if os:
        filtered_data = filtered_data[filtered_data['ua_os'].isin(os)]
    if browser:
        filtered_data = filtered_data[filtered_data['ua_client_name'].isin(browser)]
    if region:
        filtered_data = filtered_data[filtered_data['region'].isin(region)]

    # Apply duration filter if provided
    if min_duration is not None:
        filtered_data = filtered_data[filtered_data['duration'] >= min_duration]
    if max_duration is not None:
        filtered_data = filtered_data[filtered_data['duration'] <= max_duration]

    # Apply watchtime filter if provided
    if min_watchtime is not None:
        filtered_data = filtered_data[filtered_data['total_watchtime'] >= min_watchtime]
    if max_watchtime is not None:
        filtered_data = filtered_data[filtered_data['total_watchtime'] <= max_watchtime]

    if min_videos is not None:
        filtered_data = filtered_data[filtered_data['video_count'] >= min_videos]
    if max_videos is not None:
        filtered_data = filtered_data[filtered_data['video_count'] <= max_videos]

    # Apply watchtime filter if provided
    if min_videos_per_day is not None:
        filtered_data = filtered_data[filtered_data['videos_per_day'] >= min_videos_per_day]
    if max_videos_per_day is not None:
        filtered_data = filtered_data[filtered_data['videos_per_day'] <= max_videos_per_day]


    return filtered_data


data = st.session_state['dataset']


st.write("## Применить фильтры к датасету")
left, middle, right = st.columns(3)

# Filters
gender = left.multiselect("Включить в датасет пол", data.sex.unique())
category = middle.multiselect("Включить в датасет категории", data.category.unique())
age = right.multiselect("Включить в датасет возрастные группы", data.age_class.unique())
device = left.multiselect("Включить в датасет девайсы", data.ua_device_type.unique())
client_type = middle.multiselect("Включить в датасет клиенты", data.ua_client_type.unique())
os = right.multiselect("Включить в датасет OС", data.ua_os.unique())
browser = left.multiselect("Включить в датасет браузеры", data.ua_client_name.unique())
region = middle.multiselect("Включить в датасет регионы", data.region.unique())


st.divider()
one, two, three, four = st.columns(4)
min_duration = one.number_input("Мин длина видео (сек)", min_value=data.duration.min())
max_duration = two.number_input("Макс длина видео (сек)",value=data.duration.max())
min_watchtime = three.number_input("Мин длина просмотра (сек)",min_value=data.total_watchtime.min())
max_watchtime = four.number_input("Макс длина просмотра (сек)",value=data.total_watchtime.max())
min_videos_per_day = one.number_input("Мин кол-во видео в день", min_value=data.videos_per_day.min())
max_videos_per_day = two.number_input("Макс кол-во видео в день", value=data.videos_per_day.max())
min_videos = three.number_input("Мин просмотернных видео", min_value=data.video_count.min())
max_videos = four.number_input("Макс просмотренных видео", value=data.video_count.max())


if st.button("Применить фильтры"):
    st.session_state['data'] = filter_dataset(
        data,
        gender,
        category,
        age,
        device,
        client_type,
        os,
        browser,
        region,
        min_duration,
        max_duration,
        min_watchtime,
        max_watchtime,
        min_videos_per_day,
        max_videos_per_day,
        min_videos,
        max_videos
    )
    data = st.session_state['data']

    with st.expander("Просмотреть ифнормацию о датасете"):
        st.write(f"Number of rows after filtering: {data.shape[0]}")

        if data.empty:
            st.write("Отфильтрованный датасет пуст. Попробуйте изменить фильтры.")
        else:
            st.dataframe(data.describe())
            utilities.show_data_info()
first, second, last = st.columns(3)
x=first.selectbox("Ось X для ScatterPlot", ["age","total_watchtime","duration", "videos_per_day","video_count"])
y=second.selectbox("Ось Y для ScatterPlot", ["age","total_watchtime","duration", "videos_per_day","video_count"])
sep = last.selectbox("Разделять данные Гистограммы и ScatterPlot по", ["region", "ua_device_type", "ua_client_type","ua_os","ua_client_name","authorized","category","age_class", "sex"])


def plot_stacked_bar_chart(data, y_column, group_column):
    # Ensure 'event_date' is in datetime format if it's not already
    if not pd.api.types.is_datetime64_any_dtype(data['event_date']):
        data['event_date'] = pd.to_datetime(data['event_date'])

    # Group by 'event_date' and the grouping column, and count the occurrences
    grouped_data = data.groupby(['event_date', group_column])[y_column].count().reset_index()

    # Create a stacked bar chart using Plotly Express
    fig = px.bar(
        grouped_data,
        x='event_date',
        y=y_column,
        color=group_column,
        labels={'event_date': 'Date', y_column: 'Number of Entries'},
        title=f"Stacked Bar Chart for {y_column} Grouped by {group_column}"
    )

    # Update layout to show only relevant days on x-axis
    fig.update_layout(barmode='stack', xaxis={'type': 'category'})

    # Display the plot in Streamlit
    st.plotly_chart(fig)
def plot_scatter_chart(data, x_column, y_column, group_column):
    # Ensure 'event_date' is in datetime format if it's being used as the x_column
    if x_column == 'event_date' and not pd.api.types.is_datetime64_any_dtype(data[x_column]):
        data[x_column] = pd.to_datetime(data[x_column])

    # Create a scatter plot using Plotly Express
    fig = px.scatter(
        data,
        x=x_column,
        y=y_column,
        color=group_column,
        opacity=0.6,
        labels={x_column: x_column.capitalize(), y_column: y_column.capitalize(), group_column: group_column.capitalize()},
        title=f"Scatter Plot for {y_column} vs {x_column} Grouped by {group_column}"
    )

    # Update layout for the chart
    fig.update_layout(legend_title=group_column.capitalize())

    # Display the plot in Streamlit
    st.plotly_chart(fig)
plot_scatter_chart(data, x, y, sep)
plot_stacked_bar_chart(data, y, sep)
