import streamlit as st
import random
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import time

# Function to simulate sensor data for different locations
def simulate_sensor_data(location):
    return {
        "location": location,
        "water_level": round(random.uniform(0, 5), 2),  # Water level in meters
        "rainfall": round(random.uniform(0, 150), 2),   # Rainfall in mm
        "temperature": round(random.uniform(20, 35), 2), # Temperature in Celsius
    }

# Set up Streamlit page configuration for black-grey theme
st.set_page_config(page_title="Flood Monitoring Dashboard", layout="wide")

# Custom CSS to make the theme dark (black and grey)
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stButton>button {
            background-color: #333333;
            color: white;
            border: none;
        }
        .stSlider>div>div>input {
            background-color: #333333;
            color: white;
        }
        .stMarkdown {
            color: #e6e6e6;
        }
        .stTextInput>div>div>input {
            background-color: #333333;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Header of the dashboard
st.title("Flood Monitoring Dashboard")
st.markdown("### Real-time flood sensor data (Simulated)")

# Define locations (example areas in Chennai)
locations = {
    "Adyar": [13.0047, 80.2670],
    "Anna Nagar": [13.0878, 80.2101],
    "Chennai Port": [13.0896, 80.2970],
    "Koyambedu": [13.0658, 80.2107],
    "T. Nagar": [13.0406, 80.2345]
}

# Sidebar for location selection
location_selected = st.sidebar.selectbox("Select Location", list(locations.keys()))

# Initialize session state for sensor data if not already initialized
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = {location: simulate_sensor_data(location) for location in locations}

# Initialize session state for water level trends (sliding window of last 10 values)
if 'water_level_trends' not in st.session_state:
    st.session_state.water_level_trends = {location: [] for location in locations}

# Map for displaying locations
m = folium.Map(location=[13.0827, 80.2707], zoom_start=12, control_scale=True)

# Adding markers for each location on the map
for location, coords in locations.items():
    data = st.session_state.sensor_data[location]
    folium.Marker(
        location=coords,
        popup=f"{location}\nWater Level: {data['water_level']}m\nRainfall: {data['rainfall']}mm\nTemperature: {data['temperature']}°C",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Display map in Streamlit app
st_folium(m, width=800)

# Display data for the selected location
location_data = st.session_state.sensor_data[location_selected]

# Display key metrics
st.subheader(f"Sensor Data for {location_selected}")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Water Level (m)", value=location_data['water_level'])
with col2:
    st.metric(label="Rainfall (mm)", value=location_data['rainfall'])
with col3:
    st.metric(label="Temperature (°C)", value=location_data['temperature'])

# Real-time Water Level Trend (Simulated)
st.subheader(f"Water Level Trend for {location_selected} (Last 10 Updates)")

# Update water levels dynamically every few seconds
# Add the latest water level to the trend history
new_water_level = random.uniform(0, 5)
timestamp = datetime.now().strftime("%H:%M:%S")
st.session_state.water_level_trends[location_selected].append((timestamp, new_water_level))

# Maintain a sliding window of last 10 water levels
if len(st.session_state.water_level_trends[location_selected]) > 10:
    st.session_state.water_level_trends[location_selected].pop(0)

# Prepare the data for charting
trend_data = pd.DataFrame(st.session_state.water_level_trends[location_selected], columns=["Time", "Water Level (m)"])

# Display line chart
st.line_chart(trend_data.set_index("Time"))

# Update data button
if st.button("Update Sensor Data"):
    st.session_state.sensor_data[location_selected] = simulate_sensor_data(location_selected)
    st.success("Sensor data updated successfully!")

# Alert if water level is above threshold (3 meters)
if location_data['water_level'] > 3:
    st.warning(f"⚠️ **Warning**: Water level in {location_selected} is above the danger threshold! Current level: {location_data['water_level']} meters.")

# Display a Heatmap for flood risk across the city (using simulated data)
st.subheader("Flood Risk Heatmap")
heatmap_data = []

# Simulate heatmap data based on location water levels
for location, coords in locations.items():
    data = st.session_state.sensor_data[location]
    heatmap_data.append([coords[0], coords[1], data['water_level']])

# Create the heatmap using Folium
from folium.plugins import HeatMap
m = folium.Map(location=[13.0827, 80.2707], zoom_start=12, control_scale=True)

# Add heatmap layer
HeatMap(heatmap_data).add_to(m)

# Display heatmap
st_folium(m, width=800)

# Display historical data (simulated)
st.subheader("Historical Data (Water Level Over Last 7 Days)")

# Simulate past 7 days of water level data
days = [f"Day {i+1}" for i in range(7)]
historical_water_levels = [random.uniform(0, 5) for _ in range(7)]

# Create a DataFrame for the historical data
historical_df = pd.DataFrame({
    'Day': days,
    'Water Level (m)': historical_water_levels
})

# Plot the historical data as a bar chart
st.bar_chart(historical_df.set_index('Day'))

# Footer
st.markdown("---")
st.markdown("**Made with ❤️ for Hackathon**")
st.markdown("Data is simulated for demonstration purposes.")
