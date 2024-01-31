import requests
import csv
import json
from datetime import datetime, timedelta
import time

from flask import Flask, jsonify,  send_file

app = Flask(__name__)

@app.route('/download')
def hello():
    prometheus_url = "http://localhost:9090/api/v1/query"
    queryList =[
        'windows_cpu_time_total{job="WMI Exporter"}[5m]',
        '100- (avg without(cpu)(irate(windows_cpu_time_total{mode="idle"}[5m]))*100)',
        'rate(windows_logical_disk_reads_total{instance="localhost:9182",volume="C:"}[5m])',
        'rate(windows_logical_disk_read_seconds_total{instance="localhost:9182",volume="C:"}[5m])',
        'windows_os_paging_free_bytes{instance="localhost:9182",job="WMI Exporter"}',
        'windows_os_physical_memory_free_bytes',
        'windows_os_virtual_memory_free_bytes',]
    queryNameList=['cpu_time_total',
                   'core_utilization',
                   'logical_disk_reads',
                   'logical_disk_read_seconds_total',
                   'os_paging_free_bytes',
                   'os_physical_memory_free_bytes',
                   'os_virtual_memory_free_bytes']
    i = 0
    start_time = int((datetime.now() - timedelta(minutes=5)).timestamp())
    end_time = int(datetime.now().timestamp())
    for currentQuery in queryList:
        # Set up parameters for the query
        params = {
            "query": currentQuery,
            "start": 1704000000,
            "end": 1704116200,
            "step": "1s",  # Adjust the step as needed
        }
        # Fetch data from Prometheus
        response = requests.get(prometheus_url, params=params)
        print(response.json())
        data=response.json()
        fileName = queryNameList[i]
        print(queryNameList[i])
        print(i)
        with open('C://Users//priya//Downloads//data-cloud//'+fileName+'.json', 'w') as json_file:
            json.dump(data, json_file)
        i += 1
    return "downloaded Files"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    # start_time = "1641190354"#"2023-01-01T00:00:00Z"
    # end_time = "1641191554"#"2023-01-02T00:00:00Z"
    # start_time ="1642630683"
    # end_time ="1642632683"