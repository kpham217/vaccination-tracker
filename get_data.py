import requests
import json
import csv


def get_updated_data(link):
    try:
        r = requests.get(link)
        # data = r.text.results
        data = r.text
        json_data = json.loads(data)["results"]
        print("> Successfully get data from Nova Scotia health")
        return json_data
    except:
        print("An exception occurred")


def get_ref_data(path):
    id_list = []
    with open (path,'r') as csv_file:
        reader =csv.reader(csv_file)
        next(reader) # skip first row
        for row in reader:
            id_list.append(row[0])
    # print(halifax_id)
    print("> Successfully load data from csv file")
    return id_list
