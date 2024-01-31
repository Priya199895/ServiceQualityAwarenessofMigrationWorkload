"""Grafana dashboard exporter"""

import json
import os
import requests

HOST = 'http://localhost:3000'
API_KEY = "glsa_2QtMEh7selgb79jAOx4xtl9SQjA4FadO_5ef057e9"

DIR = 'exported-dashboards/'


def main():
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get('%s/api/search?query=&' % (HOST,), headers=headers)
    response.raise_for_status()
    dashboards = response.json()
    print(dashboards)

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    for d in dashboards:
        print("Saving: " + d['title'])
        # response = requests.get('%s/api/dashboards/%s' % (HOST, d['uri']), headers=headers)
        # response = requests.get('http://localhost:3000/api/datasources',headers=headers) #this fetches the dataset
        # requests.body()
        response = requests.post('http://localhost:3000/api/ds/query?ds_type=prometheus&requestId=Q626',
                                 headers=headers)

        print(response.json())
        data = response.json()['dashboard']
        dash = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        name = data['title'].replace(' ', '_').replace('/', '_').replace(':', '').replace('[', '').replace(']', '')
        tmp = open(DIR + name + '.json', 'w')
        tmp.write(dash)
        tmp.write('\n')
        tmp.close()

if __name__ == '__main__':
    main()