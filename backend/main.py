import streamlit as st
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

# Function to insert data into the database
def insert_into_database(humidity, temperature):
    init_db.insert_data("sensor.db", humidity, temperature)

# Main loop to update the Streamlit display
def main():
    serial_port = 'COM3'  # Adjust to your actual serial port
    ser = serial.Serial(serial_port, 9600, timeout=1)
    while True:
        line = ser.readline().decode().strip()
        if "Humidity" in line:
            new_humidity = line
            if new_humidity != st.session_state.humidity:
                st.session_state.humidity = new_humidity
                insert_into_database(st.session_state.humidity.split(': ')[1], st.session_state.temperature.split(': ')[1])
        elif "Temperature" in line:
            new_temperature = line
            if new_temperature != st.session_state.temperature:
                st.session_state.temperature = new_temperature
                insert_into_database(st.session_state.humidity.split(': ')[1], st.session_state.temperature.split(': ')[1])

        humidity_placeholder.text(st.session_state.humidity)
        temperature_placeholder.text(st.session_state.temperature)
        time.sleep(1)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()