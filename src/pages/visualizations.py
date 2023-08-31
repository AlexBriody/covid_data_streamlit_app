import os
import streamlit as st
import pandas as pd
import plotly.express as px
from to_mongo import ToMongo
from pathlib import Path

#******************added below**********************
# Create a dictionary to map display names to column names
column_name_map = {
    'Total Cases': 'totalCases',
    'Total Deaths': 'totalDeaths',
    'Total Recovered': 'totalRecovered',
    'Percent Deaths': 'percentDeaths',
    'Percent Recovered': 'percentRecovered',
    'Rank Percent Recovered': 'rankPercentRecovered',
    'Rank Percent Deaths': 'rankPercentDeaths'
}

# Create a list of display names for the dropdown
display_names = list(column_name_map.keys())

#******************added above **********************

# # Establish a filepath to the oracle_cards.csv file
# filepath = Path('/Users/alexanderbriody/Desktop/Coding Temple/capstone_2/covid_data_streamlit_app/covid_data_streamlit_app/src/data/covid_data_eng.csv')

filepath = os.path.join(Path(__file__).parents[1], 'data/covid_data_eng.csv')
df = pd.read_csv(filepath, low_memory=False)

df = pd.read_csv(filepath, low_memory=False)

# Create an instance of the ToMongo class
mongo = ToMongo()

# Fetch data from MongoDB and convert to DataFrame
data = pd.DataFrame(list(mongo.cards.find()))

# Drop the '_id' field
data = data.drop(columns=['_id'])

# Dropdown widgets for visualization type
vis_to_use = ['Histogram', 'Line Chart', 'Scatter Plot']
# Add "Choose an Option" as the initial option for the type of visualization dropdown
type_vis = st.selectbox('Select the type of visualization:', options=['Choose an Option'] + vis_to_use)

# # Dropdown widgets for data selection
# # Add "Choose an Option" as the initial option for the covid-19 metric dropdown
# x_column = st.selectbox('Select a covid-19 metric:', options=['Choose an Option', 'totalCases', 'totalDeaths', 'totalRecovered', 'percentDeaths', 'percentRecovered', 'rankPercentRecovered', 'rankPercentDeaths'])

#******************added below**********************

# Dropdown widget for data selection
# Add "Choose an Option" as the initial option for the covid-19 metric dropdown
x_column_display = st.selectbox('Select a covid-19 metric:', options=['Choose an Option'] + display_names)

# Get the column name corresponding to the selected display name
x_column = column_name_map.get(x_column_display)

#******************added above**********************

# Define the options for the ranking range dropdown with "Choose an Option" as the initial option
y_column_options = ['Choose an Option', 'Top 25 Countries', 'Bottom 25 Countries']
y_column = st.selectbox('Select a ranking range:', options=y_column_options)

# Check if both dropdowns are selected before filtering and plotting
if type_vis != 'Choose an Option' and x_column != 'Choose an Option' and y_column != 'Choose an Option':
    # Filter data based on y_column selection
    if y_column == 'Top 25 Countries':
        if x_column == 'rankPercentRecovered' or x_column == 'rankPercentDeaths':
            data = data[data[x_column] >= 1].nsmallest(25, x_column)
        else:
            data = data[data[x_column] != -1].nlargest(25, x_column)
    elif y_column == 'Bottom 25 Countries':
        if x_column == 'rankPercentRecovered' or x_column == 'rankPercentDeaths':
            data = data[data[x_column] <= data[x_column].max()].nlargest(25, x_column)
        else:
            data = data[data[x_column] != -1].nsmallest(25, x_column)
    else:
        # For 'totalCases', 'totalDeaths', 'totalRecovered', 'percentDeaths', 'percentRecovered'
        if y_column == 'Top 25 Countries':
            data = data[data[x_column] != -1].nlargest(25, x_column)
        else:
            data = data[data[x_column] != -1].nsmallest(25, x_column)

     # Plot the selected visualization type
    if type_vis == 'Histogram':
        fig = px.histogram(data, x='country', y=x_column)
        fig.update_xaxes(title_text='Countries')  # Correct the x-axis label
        fig.update_xaxes(tickangle=45)  # Angle the x-axis labels
        fig.update_yaxes(title_text=x_column_display, tickprefix='')  # Update y-axis label
        fig.update_layout(height=600, width=1000)  
        st.plotly_chart(fig, use_container_width=True)
    elif type_vis == 'Line Chart':
        fig = px.line(data, x='country', y=x_column)
        fig.update_xaxes(title_text='Countries')  # Correct the x-axis label
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(title_text=x_column_display, tickprefix='')  # Update y-axis label 
        fig.update_layout(height=600, width=1000)  
        st.plotly_chart(fig, use_container_width=True)
    elif type_vis == 'Scatter Plot':
        fig = px.scatter(data, x='country', y=x_column, hover_data=['country'])
        fig.update_xaxes(title_text='Countries')  # Correct the x-axis label
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(title_text=x_column_display, tickprefix='')  # Update y-axis label
        fig.update_layout(height=600, width=1000)  
        st.plotly_chart(fig, use_container_width=True)

   # Display ranked list for rankPercentRecovered
    if x_column == 'rankPercentRecovered':
        # Display ranked list
        st.write("Ranked List for rankPercentRecovered:")
        ranked_data = data[['country', 'rankPercentRecovered']]
        ranked_data_html = ranked_data.to_html(index=False)
        st.write(ranked_data_html, unsafe_allow_html=True)
            
    # Display ranked list for rankPercentDeaths
    if x_column == 'rankPercentDeaths':
        # Display ranked list
        st.write("Ranked List for rankPercentDeaths:")
        ranked_data = data[['country', 'rankPercentDeaths']]
        ranked_data_html = ranked_data.to_html(index=False)
        st.write(ranked_data_html, unsafe_allow_html=True)
        
