import json
import csv

# Read JSON data from file
with open('calendar_graph_data.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Define the CSV file name
csv_file = 'calendar.csv'

import csv

# Define the headers
headers = ['Created', 'Category', 'Subject', 'Organizer', 'AttendeeCountQ', 'ID']

# Write to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for item in json_data:
        created = item.get('createdDateTime', '')
        categories = item.get('categories')
        category = categories[0] if categories and isinstance(categories, list) and len(categories) > 0 else ''
        subject = item.get('subject', '')
        organizer_info = item.get('organizer')
        email_info = organizer_info.get('emailAddress') if organizer_info else {}
        organizer = email_info.get('address', '') if email_info else ''
        attendees = item.get('attendees', [])
        attendee_count = len(attendees) if isinstance(attendees, list) else 0
        event_id = item.get('id', '')
        
        # Write the row with attendee count
        writer.writerow([created, category, subject, organizer, attendee_count, event_id])

