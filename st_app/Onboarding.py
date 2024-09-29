import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download
from streamlit_extras.let_it_rain import rain

import utilities


#В первых трех функциях необходимо раскоментировать и закоментировать код, если есть желание не ждать загрузки датасета, а прочитать его из файла в директории /data

@st.cache_data
def load_all_data():
    #train_events = pd.read_csv('data/train_events.csv', sep=',')
    train_events = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='train_events.csv', repo_type='dataset'))

    #videos = pd.read_csv('data/video_info_v2.csv')
    videos = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='video_info_v2.csv', repo_type='dataset'))
    #unauthorized = pd.read_csv('data/all_events.csv')
    unauthorized = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='all_events.csv', repo_type='dataset'))
    #targets = pd.read_csv('data/train_targets.csv')
    targets = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='train_targets.csv', repo_type='dataset'))
    videos['duration']=videos['duration']/1000
    train_events['authorized'] = True
    unauthorized['authorized'] = False
    all_entries = pd.concat([train_events, unauthorized], ignore_index=True)
    data = pd.merge(all_entries, videos, on='rutube_video_id', how="outer")
    data = pd.merge(data, targets, on="viewer_uid", how="outer")
    data['event_timestamp'] = pd.to_datetime(data['event_timestamp'])

    # Extract the date part (without time) from 'event_timestamp'
    data['event_date'] = data['event_timestamp'].dt.date

    # Group by 'viewer_uid' and 'event_date', and count the number of entries per day for each user
    data['videos_per_day'] = data.groupby(['viewer_uid', 'event_date'])['event_timestamp'].transform('size')
    data['video_count'] = data.groupby('viewer_uid')['event_timestamp'].transform('size')
    return data

@st.cache_data
def load_authorized_data():
    #train_events = pd.read_csv('data/train_events.csv', sep=',')
    train_events = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='train_events.csv', repo_type='dataset'))
    #videos = pd.read_csv('data/video_info_v2.csv')
    videos = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='video_info_v2.csv', repo_type='dataset'))
    #targets = pd.read_csv('data/train_targets.csv')
    targets = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='train_targets.csv', repo_type='dataset'))

    videos['duration']=videos['duration']/1000
    train_events['authorized'] = True
    data = pd.merge(train_events, videos, on='rutube_video_id', how="outer")
    data = pd.merge(data, targets, on="viewer_uid", how="outer")
    data['event_timestamp'] = pd.to_datetime(data['event_timestamp'])

    # Extract the date part (without time) from 'event_timestamp'
    data['event_date'] = data['event_timestamp'].dt.date

    # Group by 'viewer_uid' and 'event_date', and count the number of entries per day for each user
    data['videos_per_day'] = data.groupby(['viewer_uid', 'event_date'])['event_timestamp'].transform('size')
    data['video_count'] = data.groupby('viewer_uid')['event_timestamp'].transform('size')
    return data
@st.cache_data
def load_unauthorized_data():
    #videos = pd.read_csv('data/video_info_v2.csv')
    videos = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='video_info_v2.csv', repo_type='dataset'))
    #unauthorized = pd.read_csv('data/all_events.csv')
    unauthorized = pd.read_csv(hf_hub_download(repo_id="seniichev/nationwide-2024", filename='all_events.csv', repo_type='dataset'))
    videos['duration']=videos['duration']/1000
    unauthorized['authorized'] = False
    data = pd.merge(unauthorized, videos, on='rutube_video_id', how="outer")
    data['event_timestamp'] = pd.to_datetime(data['event_timestamp'])

    # Extract the date part (without time) from 'event_timestamp'
    data['event_date'] = data['event_timestamp'].dt.date

    # Group by 'viewer_uid' and 'event_date', and count the number of entries per day for each user
    data['videos_per_day'] = data.groupby(['viewer_uid', 'event_date'])['event_timestamp'].transform('size')
    data['video_count'] = data.groupby('viewer_uid')['event_timestamp'].transform('size')
    return data

st.set_page_config(
   page_title="BBBB Dashboard",
   page_icon="📈",
   layout="wide",
   initial_sidebar_state="expanded",

)

st.write("# Добро пожаловать в интерактивный DashBBBBoard")
dataset_options = st.radio(
    "На каком датасете необходимо построить анализ",
    ["Только авторизованные", "Только неавторизованные", "Все записи"]
)
st.write(f"Строим аналитику по {dataset_options}")
# Load the dataset and store it in session state (if not already cached)
primary, secondary = st.columns(2)
if primary.button("Загрузить датасет",type="primary"):
    if dataset_options=="Только авторизованные":
            st.session_state['data'] = load_authorized_data()
            st.session_state['dataset']=load_authorized_data()
            st.session_state['dataset_type']='authorized'
    elif dataset_options=="Только неавторизованные":
            st.session_state['data'] = load_unauthorized_data()
            st.session_state['dataset']=load_unauthorized_data()
            st.session_state['dataset_type']='unauthorized'


    else:
        st.session_state['data'] = load_all_data()
        st.session_state['dataset'] = load_all_data()
        st.session_state['dataset_type'] = 'all'

    # Now the data is accessible via st.session_state['data']
    data = st.session_state['data']
    # rain(
    #     emoji="🥳",
    #     font_size=105,
    #     falling_speed=10,
    #     animation_length=1,
    # )

if secondary.button("Описание датасета"):
    utilities.show_data_info()
