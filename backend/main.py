import streamlit as st
import serial

# Establish serial connection with Arduino [Device Manager, Ports (COM & LPT), Arduino]
ser = serial.Serial('COM8', 9600) 

# Streamlit app
st.title('Arduino Data Stream')
st.write('Reading data from Arduino:')

# Read and display data from Arduino
while True:
    line = ser.readline().decode().strip()
    
    components = line.split()

    if len(components) >= 3:
        status = components[0]
        humidity = components[1]
        temperature = components[2]

        st.write('Status:', status)
        st.write('Humidity (%):', humidity)
        st.write('Temperature (C):', temperature)
    else:
        st.write('Invalid data:', line)