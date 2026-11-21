import csv
import json
from pathlib import Path
from datetime import datetime

"""
Generic file parser 
"""

def parse_file(file_path):

    path = Path(file_path)
    extension = path.suffix.lower() #finds just the extension (ex .csv)

    # Throws error file file does not exist
    if not path.is_file():
        raise FileNotFoundError(f"No file found at {file_path}")

    elif extension == '.csv':
        with open(path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)    

    lines = {}

    with open(path, 'r', encoding='utf-8') as file: #Opens file at path, reads it, python interpets, and names the file "file"
        for lineNum, text in enumerate(file, start = 1):
            lines[lineNum] = text.rstrip("\r\n")
                  #Dictionary key  = Value

    return lines
# converts and sorts the events in datetime format form ealiest to latest (all other values kept same)
def prep_events(events):
    for event in events:
        event["timestamp"] = datetime.fromisoformat(event["timestamp"]) #converts current timestamp value into a datetime obj
    events.sort(key = lambda event: event["timestamp"]) #sorts events by keys from ealiests to latest (key = get_timestamp)
    return events 
   
def get_failed_events(events):
    failed_events = []

    for event in events:
        if event["outcome"] == "failure":
            failed_events.append(event)
    return failed_events

def find_suspicious_activity(events):

    events = prep_events(events)

    groupings = {} #empty dictionary

    for event in get_failed_events(events):
        key = (event["username"], event["source_ip"], event["host"]) #creates tuple key for id each group (ex.("alice", "192.0.2.10", "research-server"))

        if key not in groupings: #if the key (name, ip, host) is not already part of the grouping, create a new one
            groupings[key] = []

        groupings[key].append(event) #add the event to the existing key

    alerts = [] #empty list of dictionaries
    message = False
    for key, group in groupings.items():
        for i in range (len(group) - 4):
            first_fail = group[i]
            fifth_fail = group[i + 4]

            time_diff = (fifth_fail["timestamp"] - first_fail["timestamp"]) #time between 1st fail and 5th fail

            if time_diff.total_seconds() <= 300: #if the same user fails more than 5 times within 5 mins, throw an alert
                message = True
                alert = {
                    "username": key[0],
                    "source_ip": key[1],
                    "host": key[2],
                    "failure_count": 5,
                    "start": first_fail["timestamp"],
                    "end": fifth_fail["timestamp"]
                }
                alerts.append(alert) #add that alert dictionary to alerts
    if message:
        print("User", alert["username"].upper(), "was flagged for having 5 or more failed logins in 5 minutes")
    return alerts

    
    

events = parse_file("sample2_logins.csv")

print(find_suspicious_activity(events))

# failures = get_failed_events(events)

# print("Total events:", len(events))
# print("Failed events:", len(failures))

# print(type(events[0]["timestamp"]))

# time_difference = events[-1]["timestamp"] - events[0]["timestamp"]
# print(time_difference.total_seconds())

    