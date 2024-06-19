import plotly.express as px
import streamlit as st
import pandas as pd
import serial
import time
import init_db

# Setup Streamlit
st.title("DHT11 Sensor Data")

if 'humidity' not in st.session_state:
    st.session_state.humidity = "Humidity (%): --"

if 'temperature' not in st.session_state:
    st.session_state.temperature = "Temperature (C): --"

humidity_placeholder = st.empty()
temperature_placeholder = st.empty()
graph_placeholder_temp = st.empty()
graph_placeholder_hum = st.empty()

# Function to insert data into the database
def insert_into_database(humidity, temperature):
    init_db.insert_data("sensor.db", humidity, temperature)

# Function to fetch and display data from the database
def display_data():
    df = init_db.fetch_all_data("sensor.db")
    if not df.empty:
        fig_temp = px.line(df, x='timestamp', y='temperature', title='Temperature Over Time')
        fig_hum = px.line(df, x='timestamp', y='humidity', title='Humidity Over Time')
        graph_placeholder_temp.plotly_chart(fig_temp)
        graph_placeholder_hum.plotly_chart(fig_hum)
    else:
        st.write("No data available in the database.")

# Main loop to update the Streamlit display
def main():
    serial_port = 'COM3'  # Adjust to your actual serial port
    ser = serial.Serial(serial_port, 9600, timeout=1)
    insert_data = True
    while True:
        line = ser.readline().decode().strip()
        if "Humidity" in line:
            new_humidity = line
            if new_humidity != st.session_state.humidity:
                st.session_state.humidity = new_humidity
                insert_data = True
            else:
                insert_data = False
        elif "Temperature" in line:
            new_temperature = line
            if new_temperature != st.session_state.temperature:
                st.session_state.temperature = new_temperature
                insert_data = True
            else:
                insert_data = False

        # Check if both humidity and temperature are valid before inserting into the database
        if insert_data:
            try:
                humidity_value = float(st.session_state.humidity.split(': ')[1])
                temperature_value = float(st.session_state.temperature.split(': ')[1])
                insert_into_database(humidity_value, temperature_value)
            except ValueError:
                # Skip insertion if values are not valid numbers
                pass

        humidity_placeholder.text(st.session_state.humidity)
        temperature_placeholder.text(st.session_state.temperature)
        display_data()
        time.sleep(1)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
