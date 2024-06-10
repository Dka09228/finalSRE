from elasticsearch import Elasticsearch


def get_monthly_growth():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


    last_month_logs = es.count(index="server_logs", body={"query": {
        "range": {
            "timestamp": {
                "gte": "now-1M/M",
                "lt": "now/M"
            }
        }
    }
    })['count']

    current_month_logs = es.count(index="server_logs", body={"query": {
        "range": {
            "timestamp": {"gte": "now/M",
                          "lt": "now+1M/M"
                          }
        }
    }
    })['count']

    growth_rate = ((current_month_logs - last_month_logs) / last_month_logs) * 100
    return growth_rate

print(f"Monthly traffic growth rate: {get_monthly_growth()}%")


def predict_traffic_for_next_six_months(current_month_logs, growth_rate):
    predictions = []
    for _ in range(6):
        current_month_logs += current_month_logs * (growth_rate / 100)
    predictions.append(current_month_logs)
    return predictions


growth_rate = get_monthly_growth()
current_logs = es.count(index="server_logs", body={"query": {
        "range": {
            "timestamp": {"gte": "now/M",
                          "lt": "now+1M/M"
                          }
        }
    }
    })['count']
predictions = predict_traffic_for_next_six_months(current_logs, growth_rate)
print("Forecasts for the next 6 months:", predictions)
