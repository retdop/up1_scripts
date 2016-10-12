from bs4 import BeautifulSoup
from selenium import webdriver
import math
import time
#%%
driver = webdriver.Firefox()
linkedin_link='https://www.linkedin.com/'
driver.get(linkedin_link)


driver.find_element_by_id('login-email').clear()
driver.find_element_by_id('login-email').send_keys('h2108596@mvrht.com')
driver.find_element_by_id('login-password').clear()
driver.find_element_by_id('login-password').send_keys('azedsqazedsq')
driver.find_element_by_id('login-submit').click()

#html=driver.page_source
#soup=BeautifulSoup(html)
url='https://www.linkedin.com/vsearch/p?title=CIO&openAdvancedForm=true&titleScope=CP&locationType=Y&f_G=us%3A0&f_I=14&rsid=5254215521475780977923&orig=ADVS&page_num='
driver.get(url + '1')
result_count = int(driver.find_element_by_id('results_count').text.split(' ')[0].replace(',',''))
nb_pages = math.ceil(result_count/10)
url_profiles=[]
start = time.time()

for i in range(nb_pages):
    print(i)
    driver.get(url + str(i+1))
    while True:
        try:
            a=driver.find_element_by_id('results').find_elements_by_class_name('result')
            break
        except:
            print('failed')
            pass
    for guy in a:
        guy_url = guy.find_element_by_class_name('result-image').get_attribute('href')
        url_profiles.append(guy_url)

print('It took ' + str((time.time() - start)/1000) + ' seconds!')
