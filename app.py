import time
from datetime import datetime
import pytz
import streamlit as st
import yfinance as yf  

# Function to get current time in a specific timezone and Unix epoch time
def get_time_in_timezone(timezone):
    current_time = datetime.now(pytz.timezone(timezone))
    unix_epoch_time = int(current_time.timestamp())
    return current_time, unix_epoch_time

# Function to convert UNIX timestamp to Human time
def convert_unix_to_human(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

# Function to fetch real-time stock data
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1d')
    return data

# Main page - Display time and Unix epoch time for selected locations
def main():
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

# Convert UNIX timestamp to Human time page
def convert_unix_page():
    st.title("Convert UNIX Timestamp to Human Time")

    unix_time_input = st.number_input("Enter UNIX Timestamp:", min_value=0, step=1, value=0)
    human_time = convert_unix_to_human(unix_time_input)

    st.write(f"Human Time: {human_time}")

# Fetch real-time financial data page
def fetch_financial_data_page():
    st.title("Real-time Stock Data")

    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL for Apple):")

    if symbol:
        data = get_stock_data(symbol)
        if data is not None:
            st.write(f"Real-time Stock Data for {symbol}:")
            st.write(data)
        else:
            st.write("No data available for the entered stock symbol.")

# Streamlit app navigation with dropdown menu
if __name__ == "__main__":
    pages = {
        "Main": main,
        "Convert UNIX to Human": convert_unix_page,
        "Realtime Stock Data": fetch_financial_data_page,
    }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox("Go to", list(pages.keys()))

    pages[selected_page]()
