import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import json

def dataset_discalaimer():
    if st.session_state['dataset_type']=='unauthorized':
        st.caption("Данные построены по датасету с неавторизованными пользователями")
    elif st.session_state['dataset_type']=='authorized':
        st.caption("Данные построены по датасету с авторизованными пользователями")
    else:
        st.caption("Данные построены по датасету со всеми пользователями")
def no_data_alert():
    st.card("😞 Этот чарт невозможно построить на выбранном датасете")
def exmaple_map(chart_data, weight):
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=55.7558,  # Latitude for Moscow, Russia
                longitude=37.6173,  # Longitude for Moscow, Russia
                zoom=5,  # Adjust the zoom level
                pitch=50  # Adjust the pitch for 3D view
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=chart_data,
                    get_position="[lon, lat]",
                    getElevationWeight=weight,  # Use 'entries' column for height
                    elevation=weight,  # Extrusion height based on 'entries'
                    getColorWeight=weight,  # Color based on the 'entries' column
                    colorRange=[
                        [255, 255, 178],  # Light color for low entries
                        [254, 204, 92],
                        [253, 141, 60],
                        [240, 59, 32],
                        [189, 0, 38]  # Darker color for high entries
                    ],
                    radius=50000,
                    elevation_scale=500,
                    elevation_range=[100, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position="[lon, lat]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                ),
            ],
        )
    )
def show_data_info():
    st.write("Колонки датасета и описание")
    description = {
        "event_timestamp": "Время события, когда пользователь взаимодействовал с видео.",
        "region": "Регион, из которого был сделан запрос.",
        "ua_device_type": "Тип устройства, с которого осуществляется доступ (мобильное, десктоп и т.д.).",
        "ua_client_type": "Тип клиента, через который осуществляется доступ (например, браузер, приложение).",
        "ua_os": "Операционная система, используемая на устройстве (например, Windows, macOS, Android).",
        "ua_client_name": "Название клиента (например, название браузера или приложения).",
        "total_watchtime": "Общее время просмотра видео в секундах.",
        "rutube_video_id": "Уникальный идентификатор видео на платформе Rutube.",
        "viewer_uid": "Уникальный идентификатор зрителя, для отслеживания пользовательской активности.",
        "authorized": "Статус авторизации пользователя (например, авторизован или нет).",
        "title": "Название видео.",
        "category": "Категория, к которой относится видео.",
        "duration": "Длительность видео в секундах.",
        "author_id": "Уникальный идентификатор автора видео.",
        "age": "Возраст пользователя.",
        "sex": "Пол пользователя (например, мужской или женский).",
        "age_class": "Класс возраста пользователя (например, 18-24, 25-34 и т.д.).",
        "videos_per_day": "Сколько видео этот пользователь посмотрел за день",
        "video_count":"Сколько видео этот пользователь посмотрел за все время"
    }

    description_df = pd.DataFrame(list(description.items()), columns=["Column", "Description"])
    available_columns = st.session_state['data'].columns
    description_df = description_df[description_df['Column'].isin(available_columns)]
    st.dataframe(description_df)


def add_coordinates(data, coordinates_file="region_coordinates.json"):
    # Load the coordinates from the JSON file
    with open(coordinates_file, 'r') as file:
        region_coordinates = json.load(file)

    # Define a function to get latitude and longitude from the region name
    def get_lat_long(region_name):
        coordinates = region_coordinates.get(region_name)
        if coordinates:
            return coordinates['latitude'], coordinates['longitude']
        else:
            return None, None

    # Apply the function to the 'region' column and create two new columns for latitude and longitude
    data['lat'], data['lon'] = zip(*data['region'].apply(get_lat_long))

    return data