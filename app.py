import time
from datetime import datetime, timedelta
import pytz
import streamlit as st

# Function to get current time in a specific timezone
def get_time_in_timezone(timezone):
    return datetime.now(pytz.timezone(timezone))

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

# Display the time for selected locations
placeholder = st.empty()

while True:
    with placeholder.container():
        for location in selected_locations:
            current_time = get_time_in_timezone(location)
            st.text(f"Time in {location}: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(1)
