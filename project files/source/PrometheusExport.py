from flask import Flask, send_file
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/download-data')
def download_data():
    try:
        prometheus_url = 'http://localhost:9090/api/v1/query'
        query = 'windows_cpu_time_total{job="WMI Exporter"}'
        cpu_usage_query="100- (avg without(cpu)(irate(windows_cpu_time_total{mode='idle'}[5m]))*100) "
        start_time = int((datetime.now() - timedelta(minutes=5)).timestamp())
        end_time = int(datetime.now().timestamp())
        step = '15s'

        params = {
            'query': cpu_usage_query,
            'start': start_time,
            'end': end_time,
            'step': step,
            'format': 'json'
        }
        url=f"{prometheus_url}/?query={query}&start={start_time}&end={end_time}/&format=csv"
        print(url)
        prometheus_response = requests.get(prometheus_url,params=params)
        data = prometheus_response.json()

        with open('prometheus_data.json', 'w') as json_file:
            json.dump(data, json_file)

        return send_file('prometheus_data.json', as_attachment=True)

    except Exception as e:
        print(e)
        return 'Error downloading data', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


