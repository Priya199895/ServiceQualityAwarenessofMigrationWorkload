import requests
import pandas as pd

# Define your Grafana details
GRAFANA_URL = 'https://localhost:3000'
API_KEY = 'glsa_2QtMEh7selgb79jAOx4xtl9SQjA4FadO_5ef057e9'

# Dashboard and panel IDs to fetch data from
DASHBOARD_ID = 1
PANEL_IDS = [1, 2, 3]  # Replace with your panel IDs

# Fetch data from each panel
combined_data = pd.DataFrame()
for panel_id in PANEL_IDS:
    url = f"{GRAFANA_URL}/api/dashboards/uid/b9c2d533-3bda-4174-a015-eddc6a14872e"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers,verify=False)

    if response.status_code == 200:
        panel_data = pd.read_csv(pd.compat.StringIO(response.text))
        combined_data = pd.concat([combined_data, panel_data], axis=1)

# Export combined data to a CSV file
combined_data.to_csv('combined_data.csv', index=False)
