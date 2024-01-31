# Read JSON data from a file
import json
import pandas as pd
import openpyxl
file_path = 'C:/Users/priya/Downloads/cpu_total_time.json'  # Update with your file path
with open(file_path, 'r') as file:
    json_data = json.load(file)
#extracting data into lists for columns
timestamps = [entry['value'][0] for entry in json_data['data']['result']]
values = [float(entry['value'][1]) for entry in json_data['data']['result']]
cores = [entry['metric']['core'] for entry in json_data['data']['result']]
modes = [entry['metric']['mode'] for entry in json_data['data']['result']]

# Creating a DataFrame
data = {
    'Timestamp': timestamps,
    'Cpu Time Total': values,
    'Core': cores,
    'Mode': modes
}
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('output_data.xlsx', index=False)