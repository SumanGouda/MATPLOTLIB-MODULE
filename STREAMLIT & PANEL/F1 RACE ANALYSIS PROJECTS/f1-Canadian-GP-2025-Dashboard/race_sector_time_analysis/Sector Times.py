# Streamlit page: Sector Times analysis


import streamlit as st
import pandas as pd
import plotly.express as px
import fastf1

# Initialize the FastF1 API
fastf1.Cache.enable_cache(r"D:\PYTON PROGRAMMING\PYTHON FILES\Data-Visualization-Using-Python\PANEL\F1 RACE ANALYSIS PROJECTS\F1 Candian GP 2025\cache")
race = fastf1.get_session(2025, 'canada', 'R')
race.load()

# Creating Streamlit Page
st.title('F1 Canadian GP 2025 Sector Times')
st.write("Driver's Sector Times  Dashboard!")

# Creating a Driver Select Box
drivers = race.laps['Driver'].unique().tolist()
select_driver = st.selectbox('Select Driver', drivers)