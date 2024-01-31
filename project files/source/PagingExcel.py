import pandas as pd
import json
import os

# Replace 'your_file.json' with your JSON file name
json_file = 'C://Users//priya//Downloads//data-cloud//core_utilization.json'

# Check if the file exists
if os.path.isfile(json_file):
    # Read JSON file
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # Extract data into lists for columns
    timestamps = [entry['value'][0] for entry in json_data['data']['result']]
    values = [float(entry['value'][1]) for entry in json_data['data']['result']]

    # Create a DataFrame
    data = {
        'Timestamp': timestamps,
        'Value': values,
    }
    df = pd.DataFrame(data)

    # Get the base name of the JSON file
    base_name = os.path.splitext(os.path.basename(json_file))[0]

    # Save DataFrame to Excel with the same name as JSON file
    excel_file = f"{base_name}.xlsx"
    df.to_excel(excel_file, index=False)
    print(f"Excel file '{excel_file}' created successfully.")
else:
    print("JSON file not found.")
