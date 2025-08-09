import json
import argparse

def filter_emails_by_sender(email_data, sender_email):
    filtered = []

    for item in email_data:
        sender = item.get("from", {}).get("emailAddress", {}).get("address")
        if sender == sender_email:
            filtered.append({
                "subject": item.get("subject", ""),
                 "bodyPreview": item.get("bodyPreview", "")
            })

    return filtered

def main():
    parser = argparse.ArgumentParser(description="Filter emails by sender.")
    parser.add_argument("sender_to_filter", type=str, help="Email address of the sender to filter")
    parser.add_argument("--file", type=str, default="inbox_graph_data.json",
                        help="Path to the JSON file containing email data")
    parser.add_argument("--body", type=str, default="false",
                        help="Path to the JSON file containing email data")
    args = parser.parse_args()

    # Load the JSON data
    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filtered_emails = filter_emails_by_sender(data, args.sender_to_filter)

    for email in filtered_emails:
        print(f"Subject: {email['subject']}")
        if args.body == 'true':
            print(f"Body Preview: {email['bodyPreview']}\n")

if __name__ == "__main__":
    main()
