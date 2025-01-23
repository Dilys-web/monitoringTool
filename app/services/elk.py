from elasticsearch import Elasticsearch

def retrieve_logs(index: str, query: dict) -> dict:
    client = Elasticsearch()
    response = client.search(index=index, body={"query": query})
    return {"logs": response["hits"]["hits"]}
