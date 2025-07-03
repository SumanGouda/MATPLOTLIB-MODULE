import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import fastf1
import pathlib

# Enable FastF1 cache
fastf1.Cache.enable_cache(r"D:\PYTON PROGRAMMING\PYTHON FILES\Data-Visualization-Using-Python\STREAMLIT & PANEL\F1 RACE ANALYSIS PROJECTS\F1 Candian GP 2025\cache")

# Load race session
race = fastf1.get_session(2025, 'Canada', 'R')
race.load()

# Function to load CSS from 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path(r"D:\PYTON PROGRAMMING\PYTHON FILES\Data-Visualization-Using-Python\STREAMLIT & PANEL\F1 RACE ANALYSIS PROJECTS\f1-Canadian-GP-2025-Dashboard\assets\canadian_gp_css.css")
load_css(css_path)

# Streamlit Title & Description
st.title("F1 Canadian GP 2025 - Track Pace Dominance")
st.markdown("Compare the **fastest laps** of any two drivers and visualize track dominance using segment colors!")

# Get telemetry data for both drivers
def get_telemetry(driver1, driver2):
    df1 = race.laps.pick_driver(driver1).pick_fastest().get_telemetry().copy()
    df2 = race.laps.pick_driver(driver2).pick_fastest().get_telemetry().copy()

    df1['Driver'] = driver1
    df2['Driver'] = driver2

    combined = pd.concat([df1, df2])
    return combined

# Plot the track dominance
def plot_dominance():
    data = get_telemetry(driver1, driver2)

    # Sync both drivers' telemetry lengths
    min_len = data.groupby("Driver").size().min()
    trimmed = data.groupby("Driver").head(min_len).reset_index(drop=True)

    # Separate back into two synced dataframes
    df1 = trimmed[trimmed['Driver'] == driver1].reset_index(drop=True)
    df2 = trimmed[trimmed['Driver'] == driver2].reset_index(drop=True)

    # Determine color per segment: magenta if driver1 faster, red if driver2 faster
    colors = ['#EF3DF2' if s1 > s2 else "#00FF40" for s1, s2 in zip(df1['Speed'], df2['Speed'])]

    # Build segments using driver1’s coordinates (same for both)
    x = df1['X'].values
    y = df1['Y'].values
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create the line collection
    lc = LineCollection(segments, colors=colors, linewidths=3)

    # Plot
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('#1E1E1E')
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect('equal')
    ax.axis('off')

    # Annotate Legend (top-left corner)
    ax.text(0.8, 1, f"{driver1}", transform=ax.transAxes,
            color='#EF3DF2', fontsize=5, ha='left')
    
    ax.text( 0.81, 0.975, f"V/S", transform=ax.transAxes,
            color='white', fontsize=5, ha='left')

    ax.text(0.8, 0.95, f"{driver2}", transform=ax.transAxes,
            color='#00FF40', fontsize=5, ha='left')


    plt.tight_layout()
    plt.close(fig)  # Prevents duplicate rendering in notebook

    return fig

# --- TRACK DOMINANCE PLOT FIRST ROW, FIRST COLUMN ---
col1, col2 = st.columns([3, 1])  # Wider graph, narrow column for extras

with col2:
    st.markdown("### Driver Selection")
    
    # Select Drivers
    drivers = race.laps['Driver'].unique().tolist()
    driver1 = st.selectbox("Select Driver 1", drivers, index=0)
    driver2 = st.selectbox("Select Driver 2", drivers, index=1)

with col1:
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    fig = plot_dominance()
    st.pyplot(fig)
    




