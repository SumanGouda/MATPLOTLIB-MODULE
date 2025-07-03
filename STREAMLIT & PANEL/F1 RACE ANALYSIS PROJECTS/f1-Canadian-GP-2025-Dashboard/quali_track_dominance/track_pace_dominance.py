import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import fastf1

# Enable FastF1 cache
fastf1.Cache.enable_cache(r"D:\PYTON PROGRAMMING\PYTHON FILES\Data-Visualization-Using-Python\STREAMLIT & PANEL\F1 RACE ANALYSIS PROJECTS\F1 Candian GP 2025\cache")

# Load race session
race = fastf1.get_session(2025, 'Canada', 'R')
race.load()

# Streamlit Title & Description
st.title("🇨🇦 F1 Canadian GP 2025 - Track Pace Dominance")
st.markdown("Compare the **fastest laps** of any two drivers and visualize track dominance using segment colors!")

# Select Drivers
drivers = race.laps['Driver'].unique().tolist()
col1, col2 = st.columns(2)
with col1:
    driver1 = st.selectbox('Select Driver 1', drivers, index=0)
with col2:
    driver2 = st.selectbox('Select Driver 2', drivers, index=1)

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
    colors = ['magenta' if s1 > s2 else 'red' for s1, s2 in zip(df1['Speed'], df2['Speed'])]

    # Build segments using driver1’s coordinates (same for both)
    x = df1['X'].values
    y = df1['Y'].values
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create the line collection
    lc = LineCollection(segments, colors=colors, linewidths=3)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1E1E1E')
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"{driver1} vs {driver2} — Track Pace Dominance", fontsize=16, color='white', pad=20)

    # Annotate Legend (top-left corner)
    ax.text(0.01, 1.02, f"{driver1} Faster", transform=ax.transAxes, color='magenta', fontsize=10, fontweight='bold')
    ax.text(0.01, 0.97, f"{driver2} Faster", transform=ax.transAxes, color='red', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.close(fig)  # Prevents duplicate rendering in notebook

    return fig

# Render in Streamlit
fig = plot_dominance()
st.pyplot(fig)
