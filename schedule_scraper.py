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

# Main script
base_url_events = 'https://visitseattle.org/events/page/{}'
all_events = []

for page_number in range(1, 40):  # Iterate over pages 1 to 40
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

print("Script executed successfully.")
