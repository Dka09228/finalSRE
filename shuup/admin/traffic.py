from elasticsearch import Elasticsearch

def get_monthly_growth():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    last_month_logs = es.count(index="server_logs", body={ "query": {
    "range": {
    "timestamp": {
    "gte": "now-1M/M",
    "lt": "now/M"
    }
    }
    }
    })['count']

    current_month_logs = es.count(index="server_logs", body={ "query": {
    "range": {
    "timestamp": { "gte": "now/M",
    "lt": "now+1M/M"
    }
    }
    }
    })['count']

    growth_rate = ((current_month_logs - last_month_logs) / last_month_logs) * 100 return growth_rate
print(f"Monthly traffic growth rate: {get_monthly_growth()}%")
