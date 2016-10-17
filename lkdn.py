from selenium import webdriver
import math
import time
import os
import re
os.chdir('/home/gabriel/xberkeley/mvp/up1_scripts/')
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
#%%
def do_search(driver):
    url_profiles_file = open('url_profiles_linkedin.txt','r')
    url='https://www.linkedin.com/vsearch/p?title=CIO&openAdvancedForm=true&titleScope=CP&locationType=Y&f_G=us%3A0&f_I=14&rsid=5254215521475780977923&orig=ADVS&page_num='
    driver.get(url + '1')
    result_count = int(driver.find_element_by_id('results_count').text.split(' ')[0].replace(',',''))
    nb_pages = min(math.ceil(result_count/10),100)
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
            url_profiles_file.write(str(guy_url) + '\n')
    
    print('It took ' + str((time.time() - start)/1000) + ' seconds!')

url_profiles = [line.strip() for line in open('url_profiles_linkedin.txt','r')]
url_profiles = url_profiles[0].replace('https://','azertyuiophttps://').split('azertyuiop')[1:]
#%%
def linkedin_connect(driver, username, password):
    linkedin_link='https://www.linkedin.com/'
    driver.get(linkedin_link)



    driver.find_element_by_id('login-email').clear()
    driver.find_element_by_id('login-email').send_keys(username)
    driver.find_element_by_id('login-password').clear()
    driver.find_element_by_id('login-password').send_keys(password)
    driver.find_element_by_id('login-submit').click()

phoneRegex = re.compile(r'''(
(\d{3}|\(\d{3}\))? # area code
(\s|-|\.)? # separator
(\d{3}) # first 3 digits
(\s|-|\.) # separator
(\d{4}) # last 4 digits
(\s*(ext|x|ext.)\s*(\d{2,5}))? # extension
)''', re.VERBOSE)

emailRegex = re.compile(r'''(
[a-zA-Z0-9._%+-]+
@
[a-zA-Z0-9.-]+
(\.[a-zA-Z]{2,4})
)''', re.VERBOSE)



def get_profile_info(driver, url):
    driver.get(url)
    infos = {}
    try:
        infos['name'] = driver.find_element_by_class_name('full-name').text
        infos['title'] = driver.find_element_by_class_name('title').text
        infos['current_employer'] =  driver.find_element_by_id('overview-summary-current').find_element_by_tag_name('td').find_element_by_tag_name('a').text
        infos['previous_employer'] =  driver.find_element_by_id('overview-summary-past').find_element_by_tag_name('td').find_element_by_tag_name('a').text
        infos['colleges']=[]
        colleges = driver.find_element_by_id('background-education').find_elements_by_class_name('editable-item')
        for college in colleges:
            college_infos = {}
            college_infos['college_name'] = college.find_element_by_class_name('summary').text
            try:
                college_infos['degree'] = college.find_element_by_class_name('degree').text   
            except NoSuchElementException:
                pass
            try:        
                college_infos['major'] = college.find_element_by_class_name('major').text
            except NoSuchElementException:
                pass
    
            times = college.find_element_by_class_name('education-date').find_elements_by_tag_name('time')
            if times:        
                college_infos['starting_date'] = times[0].text
                if len(times)>1:
                    college_infos['ending_date'] = times[1].text[2::]
            infos['colleges'].append(college_infos)
    except NoSuchElementException:
        print("profile incomplete")
    infos['profile_link'] = url[:url.index('?')]

    try:    
        phones = []
        text = driver.find_element_by_id('profile').text
        for groups in phoneRegex.findall(text):
            phoneNum = '-'.join([groups[1], groups[3], groups[5]])
            if groups[8] != '':
                phoneNum += ' x' + groups[8]
                phones.append(phoneNum)
        if len(phones) > 0:
            infos['email'] = ', '.join(phones)
        
        emails=[]
        for groups in emailRegex.findall(text):
            emails.append(groups[0])
        if len(emails) > 0:
            infos['email'] = ', '.join(emails)
    except NoSuchElementException:
        print('weird profile')
        
    
    return(infos)

def scrape_all_profiles(driver, url_profiles, start):
    profiles_info_file = open('profiles_info.txt','w')
    count = 0
    success_count = 0
    for i in range(start,len(url_profiles)):
        url=url_profiles[i]
        count+=1
        driver.get(url)
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "headline"))
            )            
            print("Page is ready!", count)
        except TimeoutException:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "pagekey-uas-consumer-login-internal"))
                ) 
                print('got caught')
                return(start+count)
            except TimeoutException:
                print("Page was too long to load")
                pass
#                linkedin_connect(driver, 'h2827476@mvrht.com','azedsq')
        new_url = driver.current_url
        if 'www.linkedin.com/in/' in new_url:
            print("public profile")
            info = get_profile_info(driver, new_url)
            profiles_info_file.write(str(info) + '\n')
            profiles_infos.append(info)
            print('added infos to file')
            success_count += 1
            print('sucesses :', success_count)

#%%
profiles_infos=[]
driver = webdriver.Firefox()
linkedin_connect(driver, 'h3005628@mvrht.com','azedsq')
scrape_all_profiles(driver, url_profiles, 2060)
profiles_infos_no_dup=[i for n, i in enumerate(profiles_infos) if i not in profiles_infos[n + 1:]]

#%% let's remove useless colleges

for person in profiles_infos_no_dup:
    try:
        chosen_college = person['colleges'][0]
        person.update(chosen_college)
        del person['colleges']
    except IndexError:
        del person['colleges']
        pass
    except KeyError:
        pass
            



#%%
import csv


#keys=profiles_infos_no_dup[23].keys()
keys = ['name', 'title', 'current_employer', 'email', 'previous_employer', 'profile_link', 'college_name', 'starting_date', 'ending_date', 'major', 'degree']
with open('profiles_info.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(profiles_infos_no_dup)

#%%






