from selenium import webdriver
import math
import time
import os
os.chdir('/home/gabriel/xberkeley/mvp/up1_scripts/')
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#%%
driver = webdriver.Firefox()
linkedin_link='https://www.linkedin.com/'
driver.get(linkedin_link)

driver.find_element_by_id('login-email').clear()
driver.find_element_by_id('login-email').send_keys('h2558600@mvrht.com')
driver.find_element_by_id('login-password').clear()
driver.find_element_by_id('login-password').send_keys('azedsq')
driver.find_element_by_id('login-submit').click()

url_profiles_file = open('url_profiles_linkedin.txt','w')
url='https://www.linkedin.com/vsearch/p?title=CIO&openAdvancedForm=true&titleScope=CP&locationType=Y&f_G=us%3A0&f_I=14&rsid=5254215521475780977923&orig=ADVS&page_num='
driver.get(url + '1')
result_count = int(driver.find_element_by_id('results_count').text.split(' ')[0].replace(',',''))
nb_pages = math.ceil(result_count/10)
url_profiles=[]
start = time.time()

for i in range(103):
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
        url_profiles_file.write(str(guy_url) + '\n')

print('It took ' + str((time.time() - start)/1000) + ' seconds!')
#%%
def linkedin_connect(driver, username, password):
    linkedin_link='https://www.linkedin.com/'
    driver.get(linkedin_link)



    driver.find_element_by_id('login-email').clear()
    driver.find_element_by_id('login-email').send_keys(username)
    driver.find_element_by_id('login-password').clear()
    driver.find_element_by_id('login-password').send_keys(password)
    driver.find_element_by_id('login-submit').click()

def get_profile_info(driver, url):
    driver.get(url)
    infos = {}
    infos['name'] = driver.find_element_by_class_name('full-name').text
    infos['title'] = driver.find_element_by_class_name('title').text
    infos['current_employer'] =  driver.find_element_by_id('overview-summary-current').find_element_by_tag_name('td').find_element_by_tag_name('a').text
    infos['previous_employer'] =  driver.find_element_by_id('overview-summary-past').find_element_by_tag_name('td').find_element_by_tag_name('a').text
    infos['colleges']=[]
    colleges = driver.find_element_by_id('background-education').find_elements_by_class_name('editable-item')
    for college in colleges:
        college_infos = {}
        college_infos['college_name'] = college.find_element_by_class_name('summary').text
        college_infos['degree'] = college.find_element_by_class_name('degree').text
        college_infos['major'] = college.find_element_by_class_name('major').text

        times = college.find_element_by_class_name('education-date').find_elements_by_tag_name('time')
        college_infos['starting_date'] = times[0].text
        college_infos['ending_date'] = times[1].text[2::]
        infos['colleges'].append(college_infos)
    infos['profile_link'] = url
    return(infos)

#%%
driver = webdriver.Firefox()
linkedin_connect(driver, 'h2640643@mvrht.com','azedsq')
profiles_info_file = open('profiles_info.txt','w')
count = 0
for url in url_profiles:
    try:
        driver.get(url)
        delay = 3
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located(driver.find_element_by_id('results')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        print('yo')
        new_url = driver.current_url
        print(new_url)
        profiles_info_file.write(str(get_profile_info(driver, new_url)) + '\n')
        print('ok')
        count += 1
        print(count)
        break
    except:
        print('failed')
        pass
