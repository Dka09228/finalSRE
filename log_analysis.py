import os
import datetime
from elasticsearch import Elasticsearch

# 1. Automated script for regular extraction of server logs
def get_logs_from_server():
    with open('../shuup/server.log', 'r') as file:
        logs = file.readlines()
    return logs
def ingest_logs_to_elk(logs):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    for log in logs:
        es.index(index="server_logs", doc_type="log", body={"message": log, "timestamp": datetime.datetime.now()})

def calculate_growth_rate():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    last_month_logs = es.search(index="server_logs", body={
        "query": {
            "range": {
                "timestamp": {
                    "gte": "now-1M/M",
                    "lt": "now/M"
                }
            }
        }
    })
    current_month_logs = es.search(index="server_logs", body={"query": {
        "range": {
            "timestamp": {"gte": "now/M",
                          "lt": "now+1M/M"
                          }
        }
    }
    })

    last_month_count = last_month_logs['hits']['total']['value']
    current_month_count = current_month_logs['hits']['total']['value']
    growth_rate = ((current_month_count - last_month_count) / last_month_count) * 100
    return growth_rate

def predict_traffic(growth_rate, current_traffic):
    predictions = {}
    for i in range(1, 7):
        current_traffic += current_traffic * (growth_rate / 100)
        predictions[f"Month {i}"] = current_traffic
    return predictions
if __name__ == "__main__":
    logs = get_logs_from_server()
    ingest_logs_to_elk(logs)
    growth_rate = calculate_growth_rate()
    current_traffic = len(logs)
    predictions = predict_traffic(growth_rate, current_traffic)
    print(predictions)



# def set_scaling_thresholds(predicted_traffic):
#     BASE_RPM = 10000 # The number of requests per minute your server can handle without scaling.
#     SCALE_UP_THRESHOLD = 0.8 # Scale up when traffic is at 80% capacity. SCALE_DOWN_THRESHOLD = 0.5 # Scale down when traffic drops to 50% capacity.
#
#     scale_up = BASE_RPM * SCALE_UP_THRESHOLD scale_down = BASE_RPM * SCALE_DOWN_THRESHOLD
#     if predicted_traffic > scale_up: return "Scale Up"
#     elif predicted_traffic < scale_down: return "Scale Down"
#     else:
#     return "Maintain Current Infrastructure"
