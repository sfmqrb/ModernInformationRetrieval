from urllib.parse import MAX_CACHE_SIZE
from selenium import webdriver
from selenium.webdriver import common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import json
import pandas as pd

######
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
######

visited_ids = ['2981549002', '3105081694', '2950893734','3119786062', '2145339207', '2153579005']
MAX_FILE_NUMBER = 2_000
q = visited_ids.copy()
file_name = 'CrawledPapers.json'

def make_url(id):
    """
    id :: str 
    return :: link
    """
    base = 'https://academic.microsoft.com/paper/'
    return base + id

def crawl(max_file_num=MAX_FILE_NUMBER, visited_ids=visited_ids, name_of_file_to_save_crawling_results="CrawledPapersTest.json"):
    q = visited_ids.copy()
    file_name = name_of_file_to_save_crawling_results
    MAX_FILE_NUMBER = max_file_num

    with open(file_name, "w") as f:
        f.write('[')

    counter = 0

    while counter < MAX_FILE_NUMBER:
        try:
            driver = webdriver.Chrome()
            curr_id = q.pop(0)
            curr_url = make_url(curr_id)
            driver.get(curr_url)

            driver.implicitly_wait(1000)
            title = driver.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/h1').text 

            driver.implicitly_wait(1000)
            ref_ls = driver.find_elements_by_xpath('//ma-card/div/compose/div/div[1]/a[1]')

            driver.implicitly_wait(1000)
            abstract = driver.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/p').text

            driver.implicitly_wait(1000)
            date = driver.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/a/span[1]').text

            driver.implicitly_wait(1000)
            authors = driver.find_elements_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/ma-author-string-collection/div/div/div/a[1]')

            driver.implicitly_wait(1000)
            rel_topics = driver.find_elements_by_xpath('//*[@id]/a/div[2]')

            driver.implicitly_wait(1000)
            cc = driver.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/div[1]/ma-statistics-item[2]/div[2]/div[2]/div[1]').text

            driver.implicitly_wait(1000)
            rc = driver.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/div[1]/ma-statistics-item[1]/div[2]/div[2]/div[1]').text

            ref_ls_id = []
            for i in range(len(ref_ls)):
                if rc == '0':
                    break
                next_ref = ref_ls[i]
                ref_new = next_ref.get_attribute('href')
                new_id = ref_new.split('/')[-2]
                ref_ls_id.append(new_id)

                if new_id not in visited_ids:
                    visited_ids.append(new_id)
                    q.append(new_id)

            author_ls_id = []
            for i in range(len(authors)):
                author = authors[i]
                author_name = author.get_attribute('aria-label')
                author_ls_id.append(author_name)

            rel_topics_ls_id = []
            for i in range(len(rel_topics)):
                rel_topic = rel_topics[i]
                name_rel_topic = rel_topic.text
                rel_topics_ls_id.append(name_rel_topic)
            
            z = {
            "id": curr_id,
            "title": title,
            "abstract": abstract,
            "date": date,
            "authors": author_ls_id,
            "related_topics": rel_topics_ls_id,
            "citation_count": cc,
            "reference_count": rc,
            "references": ref_ls_id
            }

            with open(file_name, "a+") as f:
                json.dump(z, f, indent=4)
                if counter != MAX_FILE_NUMBER-1:
                    f.write(',')
                else:
                    f.write(']')


            counter += 1

        except:
            print("In counter =", counter, "error occured", "id =", curr_id)
        finally:
            driver.quit()
            continue

