import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        data = []
        
        for row in csv_reader:
            data.append(row)
    
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage:
csv_to_json('monthly_stop_data.csv', 'monthly_stop_data.csv.json')