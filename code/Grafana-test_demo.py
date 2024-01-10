import requests
import json
import openpyxl
import pandas as pd

# Variables
url = "http://localhost:3000"  # The root URL of your Grafana instance
api_key = "glsa_K69N1nXZb3VdFVl25RXFxorVUnlYKROx_81379963"  # Your Grafana API token
headers = {"Authorization": "Bearer " + api_key}
uid = "f9a134ab-0c8f-446d-a5bd-6b9ec5fa394f"  # The unique identifier of the dashboard you want

# The API endpoint URL
endpoint_url = url + "/api/dashboards/uid/" + uid

# Send GET request to Grafana API
response = requests.get(endpoint_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print or save the dashboard JSON data
    print(response.json())
    df = pd.json_normalize(response.json())
    df.to_excel("output.xlsx")
else:
    print("Failed to fetch dashboard:", response.content)
