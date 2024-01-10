import json
import pandas as pd
import openpyxl
import math

file_path_new = 'C:\\Users\\brtiw\\OneDrive\\Desktop\\MS - HIS - Sem 1\\Cloud Computing\\Data\\prometheus_datacore_utilization.json'
file_path_mem = 'C:\\Users\\brtiw\\OneDrive\\Desktop\\MS - HIS - Sem 1\\Cloud Computing\\Data\\prometheus_dataos_virtual_memory_free_bytes.json'
file_path_phy_mem = 'C:\\Users\\brtiw\\OneDrive\\Desktop\\MS - HIS - Sem 1\\Cloud Computing\\Data\\prometheus_dataos_physical_memory_free_bytes.json'
file_path_net_byte_total = 'C:\\Users\\brtiw\\OneDrive\\Desktop\\MS - HIS - Sem 1\\Cloud Computing\\Data\\prometheus_datanet_bytes_total.json'


# Read JSON data from the file
with open(file_path_new, 'r') as file:
    json_data = file.read()
with open(file_path_mem, 'r') as file1:
    json_data_mem = file1.read()
with open(file_path_phy_mem, 'r') as file2:
    json_data_phy_mem = file2.read()
with open(file_path_net_byte_total, 'r') as file2:
    json_data_net_byte_total = file2.read()


# Parse JSON data
data = json.loads(json_data)
df = pd.DataFrame()
# Below code is to export CPU per core utilization to csv file
#print(data['data']['result'])
# Extract metric and value information for each item in the 'result' list
for item in data:
    datalist = []
    #print(item['data']['result'])
    for metricInfo in item['data']['result']:        
        metric_info = metricInfo['metric']
        core = metricInfo['metric']['core']
        instance = metricInfo['metric']['instance']
        mode = metricInfo['metric']['mode']
        value_info = metricInfo['value']
        time = metricInfo['value'][0]
        core_value = metricInfo['value'][1]
        #print("Metric Information:")
        #print(metric_info)
        
        #print("\nValue Information:")
        #print(value_info)
        
        #print("\n---\n")
        datalist = [{'core':core,
                     'instance':instance,
                     'mode':mode,
                     'time': math.floor(float(time)),
                     'core_value':core_value}]
        df = df._append(datalist)

df_vir_new=pd.DataFrame()
data_mem = json.loads(json_data_mem)
for item in data_mem:
    datalist = []
    for metricInfo in item['data']['result']:                
        time = metricInfo['value'][0]
        vir_mem_value = metricInfo['value'][1]
        print(vir_mem_value)
        datalist =[{'time': math.floor(float(time)),
                    'vir_mem_value': vir_mem_value}]
        df_vir_new = df_vir_new._append(datalist)
        
df = pd.merge(df, df_vir_new, on='time')

df_phy_new=pd.DataFrame()
data_phy_mem = json.loads(json_data_phy_mem)
for item in data_phy_mem:
    datalist = []
    for metricInfo in item['data']['result']:                
        time = metricInfo['value'][0]
        phy_mem_value = metricInfo['value'][1]
        print(phy_mem_value)
        datalist =[{'time': math.floor(float(time)),
                    'phy_mem_value': phy_mem_value}]
        df_phy_new = df_phy_new._append(datalist)
        
df= pd.merge(df, df_phy_new, on='time')


df_net_bytes_total=pd.DataFrame()
data_net_bytes_total = json.loads(json_data_net_byte_total)
print(data_net_bytes_total)
for item in data_net_bytes_total:
    datalist = []
    for metricInfo in item['data']['result']:                
        time = metricInfo['value'][0]
        data_net_bytes_total = metricInfo['value'][1]
        print(data_net_bytes_total)
        datalist =[{'time': math.floor(float(time)),
                    'data_net_bytes_total': data_net_bytes_total}]
        df_net_bytes_total = df_net_bytes_total._append(datalist)
        
df= pd.merge(df, df_net_bytes_total, on='time')
df.to_excel('output_core_data.xlsx', index=False)
#df.to_csv('output_core_data.csv', index=False)

    

