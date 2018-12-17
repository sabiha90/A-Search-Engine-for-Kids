import os, json
import csv
import requests
import itertools

blackListed = set()
def init_index():
    delete_index()
    index_json = '{"settings":{"index" : {"number_of_shards": 1, "number_of_replicas": 1}}}'
    print(requests.put('http://localhost:9200/test_search_engine', data=index_json, headers={'content-type':'application/json'}).content)

def load_blacklist():
    documents_file = open('../data/blacklisted_wordlist.csv', 'r')
    with open('../data/blacklisted_wordlist.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            badword = row[0].encode('latin-1', 'ignore').decode('utf-8', 'ignore')
            # print(badword)
            blackListed.add(badword)


def delete_index():
    print(requests.delete('http://localhost:9200/test_search_engine').content)

def query_index(query):
    query_string = '{"sort" : [ { "_score" : "desc"} ],' \
                   ' "query": {"bool" : {"must" : {"query_string" : {"query" : "'+ query + '"}}}}}'
    response = requests.post('http://localhost:9200/test_search_engine/_search', data=query_string, headers={'content-type': 'application/json'})
    hits = json.loads(response.content)['hits']['hits']
    if query in blackListed:
        return "Sorry Not Found"

    return rankResults(hits)

def resolveTopicName(topic_id):
    topics = {
        0: 'Hobbies',
        1: 'Knowledge',
        2: 'Gaming',
        3: 'Academics',
        4: 'Health',
        5: 'Entertainment',
        6: 'Food'
    }
    return topics.get(int(topic_id), "Topic")

def weightMultiplier(topic_id):
    topics = {
        0: 4,
        1: 6,
        2: 1,
        3: 7,
        4: 5,
        5: 2,
        6: 3
    }
    return topics.get(int(topic_id), "Topic")

def rankResults(hits):
    result = []
    for hit in hits:
        id = hit['_id']
        label = hit['_source']['label']
        content = hit['_source']['content']
        topic = hit['_source']['topic']
        topicName = resolveTopicName(topic)
        score = hit['_score'] * weightMultiplier(topic)
        model = {'id': id, 'label': label, 'topic': topicName, 'content': content, 'score': score}
        result.append(model)

    ranked = sorted(result, key=lambda k: k.get('score', 0), reverse=True)
    return ranked

def prioritizeResults(result):
    #       Academics, Knowledge, Health, Hobbies, Food, Entertainment, Gaming
    priority = {'3',    '1',       '4',     '0',    '6',     '5',        '2'}
    p_result = []
    for p in priority:
        p_result.append(result.get(p, []))
    return list(itertools.chain.from_iterable(p_result))


def load_documents():
    documents_file = open('../data/topic_data.csv', 'r')
    with open('../data/topic_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in spamreader:
            print(len(row), ' ', i)
            content = row[1].encode('latin-1', 'ignore').decode('utf-8', 'ignore')
            document = '{'
            document = document + '"id": "' + row[0] + '", "content": "' + content + '", "label":"' + row[2] + \
                       '", "topic": "' + row[3] + '"'
            document = document + '}'
            id = row[0]
            response = requests.put('http://localhost:9200/test_search_engine/_doc/'+id, data=document, headers={'content-type':'application/json'})
            print(response.content)
            # if i == 100:
            #     break
            i = i+1
