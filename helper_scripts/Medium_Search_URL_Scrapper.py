from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

base_url = "https://medium.com/search?q="
topics = open("Medium_Topics_negative.txt").read().strip().lower()
topics_list=topics.split('\n')
topics_urls = []
blog_urls = {}
driver = webdriver.Chrome('./chromedriver')

with open('Neg.csv', 'w') as f:
    for topic in topics_list:
        blog_urls[topic] = []
        topic_url = base_url+topic
        print(topic_url)
        driver.get(topic_url)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        count=0
        while(match==False):
            lastCount = lenOfPage
            time.sleep(4)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count += 1
            if lastCount==lenOfPage:
                match=True
        print("Scrolled "+str(count)+" times")
        articles = driver.find_elements_by_class_name('postArticle-content')
        article_count=0
        for article in articles:
            article_url = (article.find_element_by_tag_name('a')).get_attribute('href')
            blog_urls[topic].append(article_url)
            f.write("%s,%s\n"%(article_url,topic))
            article_count+=1
        print("total articles retrieved = "+str(article_count))
driver.quit()
