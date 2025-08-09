import json
from collections import Counter
import csv

# Update this path to match your actual file location
file_path = "recoverableitemsdeletions_graph_data.json"
output_csv = "recoverableitemsdeletions_graph_data.csv"

# Load the JSON data
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract email addresses
email_addresses = []
for item in data:
    from_field = item.get('from', {})
    email_info = from_field.get('emailAddress', {})
    email = email_info.get('address')
    if email:
        email_addresses.append(email)

# Count occurrences
email_counts = Counter(email_addresses)

# Sort results by count in descending order
sorted_email_counts = sorted(email_counts.items(), key=lambda x: x[1], reverse=True)

# Save results to a CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Email Address", "Count"])
    for email, count in sorted_email_counts:
        writer.writerow([email, count])

print(f"Results saved to {output_csv}")
