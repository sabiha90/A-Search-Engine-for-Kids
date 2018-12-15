import os, json
import csv
import requests


def init_index():
    delete_index()
    index_json = '{"settings":{"index" : {"number_of_shards": 1, "number_of_replicas": 1}}}'
    print(requests.put('http://localhost:9200/test_search_engine', data=index_json, headers={'content-type':'application/json'}).content)


def delete_index():
    print(requests.delete('http://localhost:9200/test_search_engine').content)

def query_index(query):
    query_string = '{"query": {"bool" : {"must" : {"query_string" : {"query" : "'+ query + '"}}}}}'
    response = requests.post('http://localhost:9200/test_search_engine/_search', data=query_string, headers={'content-type': 'application/json'})
    hits = json.loads(response.content)['hits']['hits']
    results = []
    for hit in hits:
        id = hit['_id']
        url = hit['_source']['url']
        class_name = hit['_source']['class']
        label = hit['_source']['label']
        content = hit['_source']['content']
        results.append({'id': id, 'url': url, 'class': class_name, 'label': label, 'content': content})
    return results


def load_documents():
    documents_file = open('../data/classified_test_data.csv', 'r')
    with open('../data/classified_test_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in spamreader:
            print(len(row))
            content = row[1].encode('latin-1', 'ignore').decode('utf-8', 'ignore')
            document = '{'
            document = document + '"id": "' + row[0] + '", "content": "' + content + '", "label":"' + row[2] + '", "class":"' + row[3] + '",' \
                                                                                        '"url":"' + row[4] + '"'
            document = document + '}'
            id = row[0]
            response = requests.put('http://localhost:9200/test_search_engine/_doc/'+id, data=document, headers={'content-type':'application/json'})
            print(response.content)
            if i == 100:
                break
            i = i+1
