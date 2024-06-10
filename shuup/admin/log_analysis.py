import os import datetime
from elasticsearch import Elasticsearch
def get_logs_from_server():
    with open('/Users/Еркебулан/server.log', 'r') as file:
    logs = file.readlines() return logs
    def ingest_logs_to_elk(logs):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}]) for log in logs:
    es.index(index="server_logs", doc_type="log", body={"message": log, "timestamp": datetime.datetime.now()})

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}]) last_month_logs = es.search(index="server_logs", body={
    "query": {
    "range": {
    "timestamp": {
    "gte": "now-1M/M",
    "lt": "now/M"
    }
    }
    }
    })
    current_month_logs = es.search(index="server_logs", body={ "query": {
    "range": {
    "timestamp": { "gte": "now/M",
    "lt": "now+1M/M"
    }
    }
    }
    })
    
    last_month_count = last_month_logs['hits']['total']['value'] current_month_count = current_month_logs['hits']['total']['value']
    growth_rate = ((current_month_count - last_month_count) / last_month_count) * 100 return growth_rate

    predictions = {} for i in range(1, 7):
    current_traffic += current_traffic * (growth_rate / 100) predictions[f"Month {i}"] = current_traffic
    return predictions
if   name   == "  main  ": logs = get_logs_from_server() ingest_logs_to_elk(logs)
growth_rate = calculate_growth_rate() current_traffic = len(logs)
predictions = predict_traffic(growth_rate, current_traffic) print(predictions)
