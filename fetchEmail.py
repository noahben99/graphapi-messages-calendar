import requests
import json
import sys
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Read token from token.txt
try:
    with open('token.txt', 'r', encoding='utf-8') as token_file:
        token = token_file.read().strip()
except FileNotFoundError:
    print("Error: token.txt file not found.")
    sys.exit(1)

def fetch_graph_data_with_limit(initial_url, headers=None, max_requests=50):
    all_items = []
    url = initial_url
    request_count = 0

    while url and request_count < max_requests:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            break

        data = response.json()
        items = data.get("value", [])
        all_items.extend(items)
        
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        skip_value = query_params.get('$skip', [''])[0]  
        print(f"skip_value {skip_value} timestamp {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        url = data.get("@odata.nextLink")
        request_count += 1
    return all_items

# Example usage
#deleted
#graph_api_url = "https://graph.microsoft.com/v1.0/me/mailFolders/{}/messages?$count=true&$select=bodyPreview,subject,from"
#inbox
#graph_api_url = "https://graph.microsoft.com/v1.0/me/mailFolders/{}/messages?$count=true&$select=bodyPreview,subject,from"
#recoverableitemsdeletions
#graph_api_url = "https://graph.microsoft.com/v1.0/me/mailFolders/{}/messages?$select=subject,from,toRecipients,bodyPreview,receivedDateTime"
#calendar
graph_api_url = "https://graph.microsoft.com/v1.0/me/calendar/events?%24select=subject%2ccategories,attendees,organizer,createdDateTime&%24top=100&%24skip=0"

auth_headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Fetch data with a limit 
all_messages = fetch_graph_data_with_limit(graph_api_url, headers=auth_headers)

# Save to file
output_file_path = "calendar_graph_data.json"  
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(all_messages, f, indent=2)

print(f"Saved {len(all_messages)} items to {output_file_path}")
