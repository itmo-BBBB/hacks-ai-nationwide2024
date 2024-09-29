import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import utilities
import plotly.express as px
import pandas as pd
data = st.session_state['data']

# Preview the aggregated chart data
data_with_coordinates = utilities.add_coordinates(data)

# Group data by latitude and longitude to count the number of entries (or any other metric)
chart_data = data_with_coordinates.groupby(['region', 'lat', 'lon']).size().reset_index(name='entries')

# Rename the latitude and longitude columns to 'lat' and 'lon' for compatibility with PyDeck
chart_data.rename(columns={'latitude': 'lat', 'longitude': 'lon'}, inplace=True)

# Preview the data to make sure 'latitude' and 'longitude' are added
st.write("# География пользователей")
utilities.exmaple_map(chart_data, weight="entries")
st.write(chart_data)
