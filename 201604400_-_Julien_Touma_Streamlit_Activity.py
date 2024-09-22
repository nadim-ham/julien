import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your dataset
df = pd.read_csv("/Users/nadimhammoud/Desktop/julien/13e1689d0a84bc62e3e3a309c06956fc_20240902_120434.csv")

# Manually renaming the columns by removing spaces and special characters
df = df.rename(columns={
    'Existence of nearby care centers - exists': 'Existence_of_nearby_care_centers_exists',
    'Existence of special needs care centers - does not exist': 'Existence_of_special_needs_care_centers_does_not_exist',
    'Existence of health resources - exists': 'Existence_of_health_resources_exists',
    'Existence of a first aid center - exists': 'Existence_of_a_first_aid_center_exists'
})

# Sidebar: Project summary with owner details
st.sidebar.title("Project Summary")
st.sidebar.write("""
- **Project Owner**: Julien Touma
- **Purpose**: Analyzing the existence of various medical resources across different towns.
""")

# Line chart section
st.subheader("Health Resources in Different Regions (Sorted from Highest to Lowest)")

# Filter for region (dropdown below the line chart)
region_filter = st.selectbox("Filter by Region", ["All"] + df['refArea'].unique().tolist())

# Filter the dataset for the line chart based on region
line_data = df if region_filter == "All" else df[df['refArea'] == region_filter]
line_data = line_data.groupby('refArea')['Existence_of_health_resources_exists'].sum().reset_index()

# Sorting by the number of health resources (highest to lowest)
line_data = line_data.sort_values(by='Existence_of_health_resources_exists', ascending=False)

# Create the line chart
line_chart = px.line(line_data, x='refArea', y='Existence_of_health_resources_exists', 
                     title='Health Resources in Different Regions (Sorted from Highest to Lowest)')

# Adding markers and adjusting the layout for better readability
line_chart.update_traces(mode='lines+markers')
line_chart.update_layout(
    xaxis_title='Region',
    yaxis_title='Number of Towns with Health Resources',
    xaxis_tickangle=-45,  # Rotate the x-axis labels for better readability
    height=600,
    width=900
)

# Display the line chart in Streamlit
st.plotly_chart(line_chart)

# Heatmap section
st.subheader("Existence of Medical Resources in Different Towns (Sorted)")

# Filter for town (dropdown below the heatmap)
town_filter = st.selectbox("Filter by Town", ["All"] + df['Town'].unique().tolist(), key="town_filter")

# Filter the dataset for the heatmap based on the selected town
heatmap_data = df if town_filter == "All" else df[df['Town'] == town_filter]

# Sorting towns by the total number of resources
heatmap_data['Total_Resources'] = heatmap_data[['Existence_of_nearby_care_centers_exists', 
                                                'Existence_of_special_needs_care_centers_does_not_exist',
                                                'Existence_of_health_resources_exists', 
                                                'Existence_of_a_first_aid_center_exists']].sum(axis=1)
heatmap_data = heatmap_data.sort_values(by='Total_Resources', ascending=False)

# Create heatmap
heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data[['Existence_of_nearby_care_centers_exists', 'Existence_of_special_needs_care_centers_does_not_exist',
                    'Existence_of_health_resources_exists', 'Existence_of_a_first_aid_center_exists']].values,
    x=['Care Centers', 'Special Needs Centers', 'Health Resources', 'First Aid Centers'],
    y=heatmap_data['Town'],
    colorscale='Blues',
    text=heatmap_data[['Existence_of_nearby_care_centers_exists', 'Existence_of_special_needs_care_centers_does_not_exist',
                       'Existence_of_health_resources_exists', 'Existence_of_a_first_aid_center_exists']].values,
    hoverinfo="text"
))

# Update heatmap layout
heatmap.update_layout(
    title='Existence of Medical Resources in Different Towns (Sorted)',
    xaxis_title='Medical Resources',
    yaxis_title='Town',
    yaxis_nticks=50,  # Increase the number of ticks to accommodate more towns
    width=800,
    height=1000
)

# Display the heatmap in Streamlit
st.plotly_chart(heatmap)
