from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

base_url = "https://medium.com/topic"
topics = open("./Medium_Topics.txt").read().strip().lower()
topics_list=topics.split('\n')

topics_urls = []
blog_urls = {}

driver = webdriver.Chrome("./chromedriver")

with open('Blog_URLS_P_Selenium.csv', 'w') as f:
    for topic in topics_list:
        blog_urls[topic] = []
        topic_url = base_url+'/'+topic
        driver.get(topic_url)
        time.sleep(6)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        count=0
        while(match==False):
            lastCount = lenOfPage
            time.sleep(6)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count += 1
            if lastCount==lenOfPage:
                match=True
        print("Scrolled "+str(count)+" times")

        # # for i in range(2):
        #     time.sleep(3)
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        articles = driver.find_elements_by_tag_name('h3')
        for article in articles:
            article_url = (article.find_element_by_tag_name('a')).get_attribute('href')
            blog_urls[topic].append(article_url)
            if(topic.lower() in ['arts','comics','books','film','gaming','music','social-media','tv']):
                f.write("%s,%s\n"%(article_url,'Entertainment'))
            if(topic.lower() in ['math','programming','science','technology','education','history']):
                f.write("%s,%s\n"%(article_url,'Academics'))
            if(topic.lower() in ['family','health','self','travel','food','sports']):
                f.write("%s,%s\n"%(article_url,'Life'))
            if(topic.lower() in ['cities','environment','equality','language','politics','religion','humor']):
                f.write("%s,%s\n"%(article_url,'Social'))
driver.quit()
