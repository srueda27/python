from collections import defaultdict
import csv


def summarize_events_optimized(events):
    # Initialize defaultdicts to automatically handle new keys
    events_by_type = defaultdict(int)
    most_active_users = defaultdict(int)

    # Loop through events once, updating our summaries directly
    for event in events:
        events_by_type[event['event_type']] += 1
        most_active_users[event['user_id']] += 1

    # Assemble the final summary dictionary
    summary = {
        'total_events': len(events),
        # Convert back to a regular dict for output to avoid issues with the consumers of the output data
        'events_by_type': dict(events_by_type),
        'most_active_users': dict(most_active_users)
    }

    return summary


def generate_events_csv(events, filename="events.csv"):
    fieldnames = ['timestamp', 'user_id', 'event_type', 'interaction_details']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for event in events:
            writer.writerow(event)


def generate_summary_txt(summary, filename="events_summary.txt"):
    with open(filename, 'w') as txtfile:
        for key, value in summary.items():
            txtfile.write(f"{key}: {value}\n")


# Use the sample events
events_sample = [
    {'timestamp': '2024-03-10T21:06:06.362839', 'user_id': 'user_8', 'event_type': 'click', 'interaction_details': 'details_73'},
    {'timestamp': '2024-03-10T21:06:06.362839', 'user_id': 'user_16', 'event_type': 'view', 'interaction_details': 'details_61'}
]

summary = summarize_events_optimized(events_sample)
generate_events_csv(events_sample)
generate_summary_txt(summary)

print("Files generated successfully.")