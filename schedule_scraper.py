import csv
import requests
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup

# Function to extract event details from a given URL
def extract_event_details(detail_url):
    detail_res = requests.get(detail_url)

    if detail_res.status_code == 200:
        detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
        # Extracting details (modify selectors as needed)
        name = detail_soup.select_one('div.medium-6.columns.event-top > h1').text.strip()
        date_time = detail_soup.select_one('div.medium-6.columns.event-top > h4 > span:nth-child(1)').text.strip()
        location = detail_soup.select_one('div.medium-6.columns.event-top > h4 > span:nth-child(2)').text.strip()
        event_type = detail_soup.select_one('div.medium-6.columns.event-top > a:nth-child(3)').text.strip()
        region = detail_soup.select_one('div.medium-6.columns.event-top > a:nth-child(4)').text.strip()

        return [name, date_time, location, event_type, region]
    else:
        return None

base_url = "https://nominatim.openstreetmap.org/search.php"

# Function to get latitude and longitude for a given location and region
def get_lat_long(location, region):
    query_params = {
        "q": f"{location}, {region}",
        "format": "jsonv2"
    }
    res = requests.get(base_url, params=query_params)
    data = res.json()

    if not data:
        query_params_location = {
            "q": f"{location}",
            "format": "jsonv2"
        }
        res_location = requests.get(base_url, params=query_params_location)
        data_location = res_location.json()

        if data_location:
            return data_location[0]["lat"], data_location[0]["lon"]

        query_params_region = {
            "q": f"{region}",
            "format": "jsonv2"
        }
        res_region = requests.get(base_url, params=query_params_region)
        data_region = res_region.json()

        if data_region:
            return data_region[0]["lat"], data_region[0]["lon"]

        return None, None

    return data[0]["lat"], data[0]["lon"]

# Function to get weather forecast for a given latitude and longitude
def get_weather_forecast(latitude, longitude):
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_url = data['properties']['forecast']
        
        # Fetch the forecast data
        forecast_response = requests.get(forecast_url)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            return forecast_data['properties']['periods']
    
    return None

# Function to format date and time from the CSV file
def format_date_time(date, time):
    if "Ongoing" in date:
        return None  # Return None for "Ongoing" date
    elif "Now" in date:
        # If the date contains "Now," use the current date and set the time
        current_date = datetime.now()
        return current_date.replace(hour=int(time[:2]), minute=int(time[3:5]))
    else:
        # Use the regular date and time format
        return datetime.strptime(f'{date} {time}', '%m/%d/%Y %I:%M%p')

# Main script
base_url_events = 'https://visitseattle.org/events/page/{}'
all_events = []

for page_number in range(1, 39):  # Iterate over pages 1 to 38
    url = base_url_events.format(page_number)
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        selector = "div.search-result-preview > div > h3 > a"
        a_eles = soup.select(selector)

        # Extract href attributes from the anchor elements and append to the list
        all_events.extend([x['href'] for x in a_eles])

# Extract event details
all_event_details = []
for event_url in all_events:
    event_details = extract_event_details(event_url)

    if event_details:
        all_event_details.append(event_details)

# Write event details to CSV
csv_header = ['Name', 'Date + Time', 'Location', 'Type', 'Region']
with open('events.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_header)
    csv_writer.writerows(all_event_details)

# Read events from CSV and add latitude and longitude
with open('events.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # Get header
    header += ['Latitude', 'Longitude']  # Add Latitude and Longitude to header

    rows = []
    for row in reader:
        name, date_time, location, event_type, region = row
        latitude, longitude = get_lat_long(location, region)
        rows.append(row + [latitude, longitude])
        time.sleep(1)

# Write to a new CSV file
with open('events_with_coordinates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

# Read existing CSV file
with open('events_with_coordinates.csv', newline='') as csvfile:
    events_reader = csv.reader(csvfile)
    header = next(events_reader)  # Skip header row

    # Prepare new CSV file for writing
    with open('event_weather_forecast.csv', 'w', newline='') as new_csvfile:
        fieldnames = header + ['Weather Forecast']
        events_writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)
        events_writer.writeheader()

        for row in events_reader:
            if 'through' in row[1]:
                # Split the date range into two dates
                first_date, second_date = row[1].split(' through ')
                # Parse the first and second dates
                first_date_time = format_date_time(first_date, '12:00AM')
                second_date_time = format_date_time(second_date, '12:00AM')
            else:
                # Use the regular date and time format
                first_date_time = format_date_time(row[1], '12:00AM')
                second_date_time = None

            # Check if the date is "Ongoing"
            if first_date_time is None:
                event_forecast = 'unknown'
            else:
                current_date = datetime.now()
                date_difference = first_date_time - current_date

                # Check if the current date is within the date range
                if second_date_time and first_date_time <= current_date <= second_date_time:
                    # Get the weather forecast for the next day
                    forecast = get_weather_forecast(row[5], row[6])
                    if forecast:
                        event_forecast = forecast[1]['shortForecast']  # Using forecast for the next day
                    else:
                        event_forecast = 'unknown'
                # Check if the first date is within the next 7 days
                elif 0 <= date_difference.days <= 7:
                    # Get the weather forecast for the first date
                    forecast = get_weather_forecast(row[5], row[6])
                    if forecast:
                        event_forecast = forecast[0]['shortForecast']  # Using forecast for the same day
                    else:
                        event_forecast = 'unknown'
                # Check if the second date is within the next 14 days
                elif second_date_time and 0 <= (second_date_time - current_date).days <= 7:
                    # Get the weather forecast for the second date
                    forecast = get_weather_forecast(row[5], row[6])
                    if forecast:
                        event_forecast = forecast[1]['shortForecast']  # Using forecast for the next day
                    else:
                        event_forecast = 'unknown'
                else:
                    # Assign unknown if none of the above conditions are met
                    event_forecast = 'unknown'

            # Write event information along with weather forecast to the new CSV file
            events_writer.writerow(dict(zip(fieldnames, row + [event_forecast])))

print("Script executed successfully.")
