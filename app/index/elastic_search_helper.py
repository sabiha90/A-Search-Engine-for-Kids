import os, json
import csv
import requests
import itertools

from flask import render_template

blackListed = set()


def init_index():
    delete_index()
    index_json = '{' \
                     '"settings":' \
                        '{' \
                            '"index" : ' \
                            '{' \
                                '"number_of_shards": 1, ' \
                                '"number_of_replicas": 1' \
                            '}' \
                        '}' \
                 '}'
    print(requests.put('http://localhost:9200/test_search_engine', data=index_json, headers={'content-type':'application/json'}).content)


def load_blacklist():
    documents_file = open('../data/blacklisted_wordlist.csv', 'r')
    with open('../data/blacklisted_wordlist.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            badword = row[0].encode('latin-1', 'ignore').decode('utf-8', 'ignore')
            blackListed.add(badword)


def delete_index():
    print(requests.delete('http://localhost:9200/test_search_engine').content)


def query_index(query):
    query_string = '{"sort" : [ { "_score" : "desc"} ],' \
                   ' "query": {"bool" : {"must" : {"query_string" : {"query" : "'+ query + '"}}}}}'
    response = requests.post('http://localhost:9200/test_search_engine/_search/?size=20', data=query_string, headers={'content-type': 'application/json'})
    hits = json.loads(response.content)['hits']['hits']
    if query.lower() in blackListed:
        return 'Sorry, no results found'
        # return render_template('index.html', no_results='Sorry, no results found')

    return rankResults(hits)


def resolveTopicName(topic_id):
    topics = {
        0: 'Entertainment',
        1: 'Academics',
        2: 'Life',
        3: 'Social'
    }
    return topics.get(int(topic_id), "Topic")


def weightMultiplier(topic_id):
    topics = {
        0: 2,
        1: 4,
        2: 3,
        3: 1
    }
    return topics.get(int(topic_id), "Topic")


def rankResults(hits):
    result = []
    for hit in hits:
        id = hit['_id']
        label = hit['_source']['label']
        content = hit['_source']['content']
        topic = hit['_source']['topic']
        topic_name = resolveTopicName(topic)
        score = hit['_score'] * weightMultiplier(topic)
        model = {'id': id, 'label': label, 'topic': topic_name, 'content': content, 'score': score}
        result.append(model)
    ranked = sorted(result, key=lambda k: k.get('score', 0), reverse=True)
    return ranked


def prioritizeResults(result):
    #       Academics, Life, Entertainment, Social
    priority = {'1',    '2',       '0',     '3'}
    p_result = []
    for p in priority:
        p_result.append(result.get(p, []))
    return list(itertools.chain.from_iterable(p_result))


def load_documents():
    documents_file = open('../data/topic_classified_original_data.csv', 'r')
    with open('../data/topic_classified_original_data.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in spamreader:
            print(len(row), ' ', i)
            content = row[1].replace("'", '')
            document = '{'
            document = document + '"id": "' + row[0] + '", "content": "' + content + '", "label":"' + row[2] + \
                       '", "topic": "' + row[3] + '"'
            document = document + '}'
            id = row[0]
            response = requests.put('http://localhost:9200/test_search_engine/_doc/'+id, data=document, headers={'content-type':'application/json'})
            print(response.content)
            i = i+1
