# i have a local csv file called 'calenderDelete.csv'.  There is one column called ID.  Column headers are in the first row.  I want to create a python script that does the following:  Loop through the rows of the CSV file, using RowNumber as an integer, beginning with StartRow and ending at EndRow, which are console line parameters and are integers. Get the value of ID from RowNumber, and set the value of URL as (F"https://graph.microsoft.com/v1.0/me/events/{ID}/microsoft.graph.permanentDelete").  Next, using requests, send a POST request to the URL.  There is no body with the request.  headers are {"Authorization": "Bearer {token}",  "Accept": "application/json" }.   The response will have no body.  A successful response will have HTTP status code 204.  An unsuccessful response will have HTTP status code 404.  The output from this function will be a csv file named calendarDelete_{timestamp}.csv containing three columns:  ID, URL, and HTTP Status Code.  Can you write this Python script?

import csv
import sys
import requests
from datetime import datetime

# Check for correct number of command-line arguments
if len(sys.argv) != 3:
    print("Usage: python script.py StartRow EndRow")
    sys.exit(1)

# Parse command-line arguments
try:
    start_row = int(sys.argv[1])
    end_row = int(sys.argv[2])
except ValueError:
    print("StartRow and EndRow must be integers.")
    sys.exit(1)

# Read token from token.txt
try:
    with open('token.txt', 'r', encoding='utf-8') as token_file:
        token = token_file.read().strip()
except FileNotFoundError:
    print("Error: token.txt file not found.")
    sys.exit(1)

# Input and output file names
input_file = 'calendarDelete.csv'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'calendarDelete_{timestamp}.csv'

# Prepare headers for the request
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Read input CSV and process rows
results = []
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

    for i in range(start_row, min(end_row + 1, len(rows))):
        row = rows[i]
        event_id = row.get('ID', '')
        url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}/microsoft.graph.permanentDelete"


        try:
            response = requests.post(url, headers=headers)
            status_code = response.status_code
            print(f"i: {i} status_code: {status_code} timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} event_id:{event_id[-15:]}")
        except requests.RequestException as e:
            status_code = f"Error: {e}"

        results.append({
            
            'HTTP Status Code': status_code,
            'ID': event_id,
            'URL': url
        })

# Write results to output CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['HTTP Status Code','ID', 'URL'])
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to {output_file}")
