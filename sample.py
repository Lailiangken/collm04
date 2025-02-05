import streamlit as st
import time
from datetime import datetime

# A complex function using logging
def complex_function(log_area):
    log_data = ""
    for i in range(5):
        log_line = f'{datetime.now()} - INFO - Processing {i}\n'
        log_data += log_line
        log_area.markdown(f"```\n{log_data}\n```")  # Display logs using markdown
        time.sleep(1)  # Simulate processing time

# Streamlit UI setup
st.title("Display Logger in Streamlit")

if st.button('Run Complex Function'):
    log_area = st.empty()  # Placeholder for text_area update
    complex_function(log_area)