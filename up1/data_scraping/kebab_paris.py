from selenium import webdriver
import re
import time
import csv



def infoskebab(emplacement):
    infos = {}
    try:
        infos['name'] = driver.find_element_by_id(
            emplacement).find_element_by_class_name('title').text
    except NoSuchElementException:
        infos['name'] = ''

    try:
        infos['address'] = driver.find_element_by_id(
            emplacement).find_element_by_class_name('txt').text
    except NoSuchElementException:
        infos['address'] = ''

    infos['grade'] = driver.find_element_by_id(
        emplacement).find_element_by_class_name('bg_grade').get_attribute('innerHTML')
    gradeRegex = re.compile(r'.*n(\d+)".*')
    grade = gradeRegex.search(infos['grade'])
    infos['grade'] = float(grade.group(1)) / float(10)
    return(infos)

def scrapepage(paris):
    nombrearrondissement = driver.find_element_by_class_name('results').text
    nombreRegex = re.compile(r'.*sur\s(\d+)')
    resultats = nombreRegex.search(nombrearrondissement)
    nombrearrondissement = resultats.group(1)
    nombrekebabs = len(driver.find_elements_by_class_name('place'))
    if(int(nombrearrondissement) < 20):
        nombrekebabs = int(nombrearrondissement)

    listeemplacements = []
    for i in range(int(nombrekebabs)):
        listeemplacements.append('lieu_' + str(i))

    for emplacement in listeemplacements:
        paris.append(infoskebab(emplacement))

    if(nombrekebabs >= 20):
        liens = driver.find_element_by_id('col_gauche').find_element_by_class_name(
            'filter_right2').find_elements_by_tag_name('a')
        longueur = len(liens)

        liens[len(liens) - 1].click()
        time.sleep(2)

        scrapepage(paris)




def scrapeville(url):
    driver.get(url)
    paris = []
    listeliens = driver.find_elements_by_class_name('fleche')
    for i in range(1, len(listeliens)):
        listeliens[i].click()
        scrapepage(paris)
        driver.get(url)
        listeliens = driver.find_elements_by_class_name('fleche')

    toCSV = paris
    keys = toCSV[0].keys()
    with open('kebab.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

if __name__ == '__main__':
    driver = webdriver.Firefox()
    scrapeville('http://www.kebab-frites.com/kebab/paris-d54.html')
