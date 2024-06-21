import plotly.express as px
import streamlit as st
import pandas as pd
import serial
import time
from datetime import datetime
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

def insert_into_database(humidity, temperature):
    """
    Inserts humidity and temperature data into the SQLite database.

    Parameters:
    - humidity (float): Humidity value in percentage.
    - temperature (float): Temperature value in Celsius.
    """
    init_db.insert_data("sensor.db", humidity, temperature)

def display_data():
    """
    Fetches data from the SQLite database and displays it using Plotly charts.
    """
    df = init_db.fetch_all_data("sensor.db")
    if not df.empty:
        fig_temp = px.line(df, x='timestamp', y='temperature', title='Temperature Over Time')
        fig_hum = px.line(df, x='timestamp', y='humidity', title='Humidity Over Time')
        graph_placeholder_temp.plotly_chart(fig_temp)
        graph_placeholder_hum.plotly_chart(fig_hum)
    else:
        st.write("No data available in the database.")

def main():
    """
    Main function to continuously read data from the serial port,
    update Streamlit display, and insert data into the database.
    """
    serial_port = '/dev/ttyACM0'  # Adjust to your actual serial port
    ser = serial.Serial(serial_port, 9600, timeout=1)
    insert_data = True
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = ser.readline().decode().strip()
        if "Humidity" in line:
            new_humidity = line
            print(current_time, new_humidity)
            if new_humidity != st.session_state.humidity:
                st.session_state.humidity = new_humidity
                insert_data = True
            else:
                insert_data = False
        elif "Temperature" in line:
            new_temperature = line
            print(current_time, new_temperature)
            if new_temperature != st.session_state.temperature:
                st.session_state.temperature = new_temperature
                insert_data = True
            else:
                insert_data = False

        if insert_data:
            try:
                humidity_value = float(st.session_state.humidity.split(': ')[1])
                temperature_value = float(st.session_state.temperature.split(': ')[1])
                insert_into_database(humidity_value, temperature_value)
            except ValueError:
                pass 
    
        humidity_placeholder.text(st.session_state.humidity)
        temperature_placeholder.text(st.session_state.temperature)
        display_data()
        time.sleep(30)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
