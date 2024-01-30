import time
from datetime import datetime, timedelta
import pytz
import streamlit as st

# Function to get current time in a specific timezone and Unix epoch time
def get_time_in_timezone(timezone):
    current_time = datetime.now(pytz.timezone(timezone))
    unix_epoch_time = int(current_time.timestamp())
    return current_time, unix_epoch_time

# List of timezones for the drop-down menu
timezones = [
    "UTC",
    "America/New_York",
    "Europe/London",
    "Asia/Tokyo",
    # Add more timezones as needed
]

# Select up to 4 locations
selected_locations = st.multiselect("Select up to 4 locations", timezones, default=timezones[:4])

# Display the time and Unix epoch time for selected locations
placeholder = st.empty()

while True:
    with placeholder.container():
        for location in selected_locations:
            current_time, epoch_time = get_time_in_timezone(location)
            st.metric(f"Epoch Time in {location}", epoch_time)
            st.metric(f"Time in {location}", current_time.strftime('%Y-%m-%d %H:%M:%S'))
            st.text("")  # Add an empty line for separation
    time.sleep(1)
