import requests
import csv
import json
from datetime import datetime, timedelta
import time
"""
# Prometheus server details
prometheus_url = "http://localhost:9090"

# Prometheus query to fetch data (modify as needed)
prometheus_query = 'windows_cpu_time_total{job="WMI Exporter"}'

# Time range for the query (modify as needed)
start_time = "1641190354"#"2023-01-01T00:00:00Z"
end_time = "1641191554"#"2023-01-02T00:00:00Z"

# Prometheus API endpoint for query
api_endpoint = f"{prometheus_url}/api/v1/query"

# Set up parameters for the query
params = {
    "query": prometheus_query,
    "start": start_time,
    "end": end_time,
    #"step": "15s",  # Adjust the step as needed
}

# Fetch data from Prometheus
response = requests.get(api_endpoint, params=params)
print(response.json())
"""

from flask import Flask, jsonify,  send_file

app = Flask(__name__)

@app.route('/download')
def hello():
    prometheus_url = "http://localhost:9090" #"http://192.168.202.23:9090"#
    queryList =[
        'windows_cpu_time_total{job="WMI Exporter"}',
        #'(100- avg without(cpu)(sum(irate(windows_cpu_time_total{mode="idle"}[5m])) by (instance)) )',
        '100- (avg without(cpu)(irate(windows_cpu_time_total{mode="idle"}[5m]))*100)',
        'rate(windows_logical_disk_reads_total{instance="localhost:9182",volume="C:"}[5m])',
        'rate(windows_logical_disk_read_seconds_total{instance="localhost:9182",volume="C:"}[5m])',
        'windows_os_paging_free_bytes{instance="localhost:9182",job="WMI Exporter"}',
        'windows_os_physical_memory_free_bytes',
        'windows_os_virtual_memory_free_bytes',
        'sum(rate(windows_net_bytes_total{instance="localhost:9182"}[30s]))']
    queryNameList=['cpu_time_total',
                   'core_utilization',
                   'logical_disk_reads',
                   'logical_disk_read_seconds_total',
                   'os_paging_free_bytes',
                   'os_physical_memory_free_bytes',
                   'os_virtual_memory_free_bytes',
                   'net_bytes_total']
    i = 0
    start_time = int((datetime.now() - timedelta(minutes=10)).timestamp())
    end_time = int(datetime.now().timestamp())
    for currentQuery in queryList:
        #start_time = int((datetime.now() - timedelta(minutes=10)).timestamp())
        #end_time = int(datetime.now().timestamp())
        #start_time = "1641190354"#"2023-01-01T00:00:00Z"
        #end_time = "1641191554"#"2023-01-02T00:00:00Z"
        #start_time ="1642630683"
        #end_time ="1642632683"

        # Prometheus API endpoint for query
        api_endpoint = f"{prometheus_url}/api/v1/query"
        print(currentQuery)
        # Set up parameters for the query
        params = {
            "query": currentQuery,
            "start": start_time,
            "end": end_time,
            "step": "1s",  # Adjust the step as needed
        }

        # Fetch data from Prometheus
        response = requests.get(api_endpoint, params=params)
        #print(response.json())
        print(start_time)
        print(end_time)
        data=response.json()
        fileName = queryNameList[i]
        print(queryNameList[i])
        print(i)
        try:
            with open('C:\\Users\\brtiw\\OneDrive\\Desktop\\MS - HIS - Sem 1\\Cloud Computing\\Data\\prometheus_data'+fileName+'.json', 'r') as existing_file:
                existing_data = json.load(existing_file)
        except FileNotFoundError:
            existing_data = []
        if not isinstance(existing_data, list):
            existing_data = [existing_data]
        existing_data.append(data)
        with open('C:\\Users\\brtiw\\OneDrive\\Desktop\\MS - HIS - Sem 1\\Cloud Computing\\Data\\prometheus_data'+fileName+'.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)

        #with open('C:\\Users\\brtiw\\OneDrive\\Desktop\\MS - HIS - Sem 1\\Cloud Computing\\Data\\prometheus_data'+fileName+'.json', 'w') as json_file:
        #    json.dump(data, json_file)
        i += 1
    return "downloaded Files"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
