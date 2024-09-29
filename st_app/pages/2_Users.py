import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import utilities
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def active_user_metrics(data):
    # Ensure 'event_timestamp' is a datetime column
    data['event_timestamp'] = pd.to_datetime(data['event_timestamp'], errors='coerce')

    # Drop NaT values
    data = data.dropna(subset=['event_timestamp'])

    # Extract just the date (without time) from 'event_timestamp'
    data['event_date'] = data['event_timestamp'].dt.date

    # Calculate DAU
    last_day = data['event_date'].max()
    dau = data[data['event_date'] == last_day]['viewer_uid'].nunique()

    # Calculate WAU
    last_week = last_day - pd.Timedelta(days=6)
    wau = data[(data['event_date'] >= last_week) & (data['event_date'] <= last_day)]['viewer_uid'].nunique()

    # Calculate MAU
    last_month = last_day - pd.Timedelta(days=29)
    mau = data[(data['event_date'] >= last_month) & (data['event_date'] <= last_day)]['viewer_uid'].nunique()

    return dau, wau, mau


def active_user_trends(data):
    # Ensure 'event_timestamp' is a datetime column
    data['event_timestamp'] = pd.to_datetime(data['event_timestamp'], errors='coerce')

    # Drop NaT values
    data = data.dropna(subset=['event_timestamp'])

    # Extract just the date (without time) from 'event_timestamp'
    data['event_date'] = data['event_timestamp'].dt.date

    # Calculate DAU
    daily_data = data.groupby('event_date')['viewer_uid'].nunique().reset_index()
    daily_data.columns = ['event_date', 'DAU']

    # Calculate WAU
    weekly_data = data.resample('W-Mon', on='event_timestamp').viewer_uid.nunique().reset_index()
    weekly_data.columns = ['event_date', 'WAU']

    # Calculate MAU
    monthly_data = data.resample('M', on='event_timestamp').viewer_uid.nunique().reset_index()
    monthly_data.columns = ['event_date', 'MAU']

    return daily_data, weekly_data, monthly_data


st.markdown("# Данные о пользователях")
data = st.session_state['data']
number_of_users = data.viewer_uid.nunique()
utilities.dataset_discalaimer()
st.metric("Уникальных пользователей", (f"{number_of_users//1000}k"))

dau, wau, mau = active_user_metrics(data)
dau_col, wau_col, mau_col = st.columns(3)
dau_col.metric("Daily Active Users (DAU)", dau)
wau_col.metric("Weekly Active Users (WAU)", wau)
mau_col.metric("Monthly Active Users (MAU)", mau)

daily_data, weekly_data, monthly_data = active_user_trends(data)

# Create bar charts
dau_col.subheader("Daily Active Users (DAU)")
dau_col.bar_chart(daily_data.set_index('event_date'))

wau_col.subheader("Weekly Active Users (WAU)")
wau_col.bar_chart(weekly_data.set_index('event_date'))

mau_col.subheader("Monthly Active Users (MAU)")
mau_col.bar_chart(monthly_data.set_index('event_date'))

user_video_counts = data.groupby('viewer_uid').size().reset_index(name='video_count')
fig = px.histogram(user_video_counts, x='video_count', nbins=100, title='Distribution of Watched Videos per User')
trend_data = user_video_counts['video_count'].value_counts().sort_index().rolling(window=5).mean()

# Add trendline using Scatter plot
fig.add_trace(go.Scatter(
    x=trend_data.index,
    y=trend_data,
    mode='lines',
    name='Trendline',
    line=dict(color='red', width=2)
))

fig.update_xaxes(range=[0,100])

# Show the figure in Streamlit or Jupyter Notebook
st.plotly_chart(fig)


style_metric_cards()
