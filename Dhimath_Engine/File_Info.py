import os
import csv
import psutil
import json

def get_sys_specs():
    sys_specs = {
        "cpu": {
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": psutil.cpu_freq().max,
            "cpu_load_avg": psutil.cpu_percent(interval=1)
        },
        "ram": {
            "total_ram": psutil.virtual_memory().total,
            "available_ram": psutil.virtual_memory().available
        },
        
    }
    return json.dumps(sys_specs)

def write_to_csv(file_path, data):
    file_id = data[0][0]  
    with open(file_path, 'r+', newline='') as file:
        reader = csv.reader(file)
        writer = csv.writer(file)

        file_id_found = False
        for row in reader:
            if row and row[0] == file_id:
                file_id_found = True
                break
        if not file_id_found:
            writer.writerow(data[0])
        else:
            file.seek(0, 2)
            writer.writerow(data[0])