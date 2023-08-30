import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
from to_mongo import ToMongo
 
# Create an instance of the ToMongo class
mongo = ToMongo()

# Convert MongoDB data to a DataFrame
data = pd.DataFrame(list(mongo.cards.find()))

# Display the main title and description
st.title("COVID-19 Data App")
st.write("This app provides COVID-19 data statistics and graphs for various Covid outcomes.")
st.write("")  # line space
st.write("")  # line space
# Create a multiselect widget for selecting countries
selected_countries = st.multiselect("Select a country", sorted(data['country'].unique()))

if selected_countries:
    # Filter the data for the selected countries
    selected_data = data[data['country'].isin(selected_countries)]

    # Additional country information
    country_data = selected_data[selected_data['country'] == selected_countries[0]]
    st.write("")  # line space
    st.write("")  # line space
    st.write(f"Total Cases: {country_data['totalCases'].values[0]:,.0f}")
    total_deaths_percentage = (country_data['totalDeaths'].values[0] / country_data['totalCases'].values[0]) * 100
    total_recovered_percentage = (country_data['totalRecovered'].values[0] / country_data['totalCases'].values[0]) * 100
    st.write(f"Total Deaths: {country_data['totalDeaths'].values[0]:,.0f} ({total_deaths_percentage:.2f}% of total cases)")
    st.write(f"Total Recovered: {country_data['totalRecovered'].values[0]:,.0f} ({total_recovered_percentage:.2f}% of total cases)")
    st.write(f"Ranking of percentage recovered for 231 countries: {country_data['rankPercentRecovered'].values[0]}")
    st.write(f"Ranking of percentage deaths for 231 countries: {country_data['rankPercentDeaths'].values[0]}")
    st.write("")  # line space
    st.write("")  # line space
    # Create a bar chart for the selected countries
    fig = px.bar(selected_data, x=['totalCases', 'totalDeaths', 'totalRecovered'], y='country',
             orientation='h', title="Total Cases, Total Deaths, and Total Recovered")

    fig.update_layout(barmode='group', bargap=0.5, margin=dict(l=10, r=10, b=10, t=40),
                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0.1)', showlegend=True)
    st.plotly_chart(fig)



