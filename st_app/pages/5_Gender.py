import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import utilities
import plotly.express as px
st.write("# Гендерные различия")
utilities.dataset_discalaimer()
st.write("## Любимые тематики")
data = st.session_state['data']
# Group by 'sex' and 'category', and count the occurrences
grouped_df = data.groupby(['sex', 'category']).size().reset_index(name='count')

# Sort by 'sex' and 'count' to get the top categories
grouped_df = grouped_df.sort_values(by=['sex', 'count'], ascending=[True, False])

# Calculate total counts for each sex
total_counts = grouped_df.groupby('sex')['count'].transform('sum')

# Calculate the proportion of each category within each sex
grouped_df['proportion'] = grouped_df['count'] / total_counts
def plot_stacked_bar_chart(grouped_df):
    total_counts = grouped_df.groupby('category')['count'].transform('sum')

    # Calculate the proportion for each sex in each category
    grouped_df['proportion'] = grouped_df['count'] / total_counts
    # Create the stacked bar chart
    fig = px.bar(
        grouped_df,
        x='category',
        y='count',
        color='sex',
        color_discrete_map={'female': 'pink', 'male': 'cyan'},
        text='proportion',  # Optional: to show the proportion as text on the bars
        title='Distribution of Categories by Sex',
        labels={'count': 'Number of Occurrences'},
        height=800
    )

    # Update the layout for better visibility
    fig.update_layout(barmode='stack', xaxis_title='Category', yaxis_title='Number of Occurrences')

    # Display the plot
    st.plotly_chart(fig)


def male_female_scatterplot(data, x_axis, y_axis):
    # Create the scatter plot
    fig = px.scatter(
        data_frame=data,
        x=x_axis,
        y=y_axis,
        color='sex',
        opacity=0.5,# Color by the 'sex' column
        color_discrete_map={'female': 'pink', 'male': 'cyan'},  # Color mapping
        title=f'Scatter Plot of {y_axis} vs {x_axis}',
        labels={'sex': 'Gender'},
        height=500
    )

    # Update layout for better visibility
    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)
# Usage
plot_stacked_bar_chart(grouped_df)
male_female_scatterplot(data.sample(n=5000, random_state=52), x_axis='total_watchtime', y_axis='duration')

# Get the top 5 categories for each sex
top_5_categories_per_sex = grouped_df.groupby('sex').head()
top_5_categories_per_sex = top_5_categories_per_sex.reset_index(drop=True)

male, female = st.columns(2)
male.write("### Мужчины 🧔🏻‍️")
female.write("### Женщины 👩🏻‍🦰")
male.write(top_5_categories_per_sex[top_5_categories_per_sex['sex']=='male'].drop(columns=['sex']).reset_index(drop=True))
female.write(top_5_categories_per_sex[top_5_categories_per_sex['sex']=='female'].drop(columns=['sex']).reset_index(drop=True))

themepicker = st.selectbox(
    "Выберите категорию",
    (data.category.unique())
)
themed_data = data[data['category']==themepicker]
sex_counts = themed_data['sex'].value_counts().reset_index()
sex_counts.columns = ['sex', 'count']
color_map = {'female': 'pink', 'male': 'cyan'}
fig = px.bar(sex_counts, x='sex', y='count',
             color='sex',  # Color based on sex
             color_discrete_map=color_map,  # Apply custom colors
             labels={'sex': 'Sex', 'count': 'Number of Entries'},
             title="Number of Entries for Each Sex")

# Display the figure
st.plotly_chart(fig)


