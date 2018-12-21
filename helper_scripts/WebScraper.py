import pandas as pd
import json
import re
from bs4 import BeautifulSoup
import numpy as np
import logging
import requests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#urls_films = pd.read_csv('Blog URLs - Films.csv',header=None)
#urls_history = pd.read_csv('Blog URLs - History.csv',header=None)


def web_crawler(url):
    doc = []
    tags = []
    url_arr = []
    for i in url:
        try:
            if '@' not in i:
                print(i)
                page = requests.get(i)
                #print(logger.info(page))
                soup = BeautifulSoup(page.content, 'html.parser')
                #text = soup.find_all('p', class_='graf--p')
                document_text = ''.join(map(str, (p_tag.text for p_tag in soup.find_all('p',class_= 'graf--p'))))
                doc.append(document_text)
                script = soup.find('script')
                d = json.loads(script.text)
                s = set()
                for j in d['keywords']:
                    if 'Tag' in (j.split(':')):
                        s.add(j.split(':')[1])
                tags.append(s)

                url_arr.append(i)
        except json.decoder.JSONDecodeError:
            continue
        except AttributeError:
            continue
        except KeyError:
            continue
    return doc,tags,url_arr

def convert_to_csv(urls): 
    documents,tags,url = web_crawler(urls)
    d = {'text': documents, 'tag': tags, 'url': url}
    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose()
    #df['class'] = name
    #df.to_csv(name+'.csv')
    return df
