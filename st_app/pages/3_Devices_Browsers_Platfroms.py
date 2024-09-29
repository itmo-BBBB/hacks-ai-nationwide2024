import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import utilities

st.write("# Распределения по платформам")
utilities.dataset_discalaimer()

st.write("## Девайсы")
data = st.session_state['data']
st.write(list(data['ua_device_type'].unique()))
devices = list(data['ua_device_type'].unique())
type_counts = list(data['ua_device_type'].value_counts().sort_index())
device_user_counts = data.groupby('ua_device_type')['viewer_uid'].nunique().sort_index().tolist()
st.write(data.groupby('ua_device_type')['viewer_uid'].nunique().sort_index())
emoji_dictionary = dict({"desktop": "🖥️", "tablet": "📋", "smartphone": "📱"})
avg_view_count_per_user = [
    x / y if y > 0 else 0  # Prevent division by zero
    for x, y in zip(type_counts, device_user_counts)
]
# Display the results in Streamlit
def devices_columns(array, title):
    st.write(f"### {title}")
    left, middle, right = st.columns(3)
    for i in range(len(array)):
        if i % 3 == 0:
            col = left
        elif i % 3 == 1:
            col = middle
        else:
            col = right
        col.metric(devices[i].upper(), (emoji_dictionary[devices[i]].upper()+": "+"\n"+str(round(array[i],2))))


devices_columns(type_counts, "Уникальных просмотров по девайсам")
devices_columns(device_user_counts, "Уникальных пользователей по девайсам")
devices_columns(avg_view_count_per_user, "Среднее количество просмотров на юзера")
st.write("Desktop")
desktop_details = st.expander("Детальный взгляд")
desktop_os_distribution=data[data['ua_device_type']=='desktop']['ua_os'].value_counts()
top_3_os = desktop_os_distribution.head(3).index.tolist()

desktop_os_df = desktop_os_distribution.reset_index()
desktop_os_df.columns = ['Operating System', 'Count']

# Create a bar chart using Plotly Express
fig = px.bar(desktop_os_df, x='Operating System', y='Count', title='Distribution of Desktop Operating Systems')

# Show the figure in Streamlit
desktop_details.plotly_chart(fig)

desktop_data = data[data['ua_device_type'] == 'desktop']
top_os_data = desktop_data[desktop_data['ua_os'].isin(top_3_os)]

# Create a histogram of the duration for the top 3 operating systems
fig = px.histogram(top_os_data,
                   x='duration',
                   color='ua_os',
                   title='Distribution of Duration for Top 3 OS on Desktop',
                   nbins=100,  # Smaller bins
                   range_x=[0, 50000],  # Limit x-axis to a maximum of 50,000
                   labels={'duration': 'Duration', 'ua_os': 'Operating System'},
                   barmode='overlay')

# Show the figure
desktop_details.plotly_chart(fig)

style_metric_cards()

