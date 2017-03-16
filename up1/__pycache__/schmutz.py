import math
import os
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import copy

#I want to extract data from a website, and copy them into a google spreadsheet.
# I want to collect all the companies listed in the 
# website http://www.vrmeister.com/vr-companies/ according to their categories, and 
# get the information into an excel with 
#'Description' 'Location' 'Contact email' ' Phone number' ' website'



def go_to_website(driver, url, xpath):
    driver.get(url)
    WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, xpath))
    )

#%%

def scrape_companies(driver, companies_infos):
#    profiles_info_file = open('profiles_info1.txt', 'w')
#    count = 0
#    success_count = 0
    
    lis = driver.find_elements_by_xpath('/html/body/section[3]/div/div/div/ul/li')
    #company name,
# profit,
# #followers,
# duration,
# amount raised 
#and website
    for li in lis:
        comp={}
#        try:
        comp['name'] = li.find_element_by_xpath('div/div/h6').text
        comp['profit'] = li.find_element_by_xpath('div/div/div[2]/div/p/span').text
        comp['followers'] = li.find_element_by_xpath('div/div/div[3]/div[1]/p/span').text
        comp['duration'] = li.find_element_by_xpath('div/div/div[3]/div[2]/p/span').text
        comp['raised'] = li.find_element_by_class_name('funded').find_element_by_tag_name('strong').text
        comp['url'] = li.find_element_by_xpath('div/a').get_attribute('href')
#        except:
#            print('fuck')
        companies_infos.append(comp)
    return(companies_infos)
#%%
import csv
def dicts_to_csv(filename, list_of_dicts, keys):
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)
#%%
if __name__=='__main__':

    os.chdir('/home/gabriel/xberkeley/up1/up1_scripts/')

    companies = []
    driver = webdriver.Firefox()
    go_to_website(driver, 'http://www.vrmeister.com/vr-companies/', '/html/body')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    categories_elements = driver.find_elements_by_class_name('content-box-column')
    categories = []
    for category in categories_elements:
        url = category.find_element_by_class_name('heading-link').get_attribute('href')
        name = category.find_element_by_tag_name('h2').text
        categories.append([url,name])
    for category in categories:
        url = category[0]
        name = category[1]
        print(name)
        go_to_website(driver, url, '/html/body')
#        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        nav = driver.find_element_by_class_name('nav-tabs')
        lis = nav.find_elements_by_tag_name('a')
        urls=[]
        subcats = []
        j = 0
        for i, li in enumerate(lis):
            subcat = li.text
            if i>0:
                li.click()
            print(subcat)
            subcats.append(subcat)
            print(len(subcats))
            posts_container = driver.find_elements_by_class_name('fusion-posts-container')
            posts = posts_container[j].find_elements_by_tag_name('a')
            for post in posts:
                if post.get_attribute('href') != 'http://www.vrmeister.com/hardware/#':
                    if post.get_attribute('href') not in urls:
                        urls.append(post.get_attribute('href'))
                        companies.append({'category': name, 'subcategory': subcat, 'url': post.get_attribute('href')})
            j+=1
    comp = copy.deepcopy(companies)  
#%%
start=time.time()
driver = webdriver.PhantomJS()
cont=0
for company in companies:
    cont+=1
    print(cont)
    try:
        go_to_website(driver, company['url'], '/html/body')
        company['description'] = driver.find_element_by_class_name('fusion_builder_column_3_4').text
        infos = driver.find_element_by_class_name('fusion-checklist-1')
        lis = infos.find_elements_by_tag_name('li')
        company['name'] = lis[0].text[14:]
        company['location'] = lis[1].text[10:]
        company['website'] = lis[2].find_element_by_tag_name('a').get_attribute('href')
        company['contact_person'] = lis[3].text[16:]
        company['email'] = lis[4].text[6:]        
        company['phone'] = lis[5].text[7:]
    except:
        print(company['url'])
        pass
print((time.time() - start)/1000)
a = copy.deepcopy(comp)
#%%

keys = ['name', 'category', 'subcategory', 'website', 'url', 'description', 'contact_person', 'email', 'phone', 'location']
dicts_to_csv('vr_infos.csv', comp, keys)
