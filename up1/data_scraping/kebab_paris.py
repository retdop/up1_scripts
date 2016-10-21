from selenium import webdriver
import re
import time
import csv

def infoskebab(emplacement):
    infos = {}

    # nom
    infos['nom'] = driver.find_element_by_id(
        emplacement).find_element_by_class_name('title').text

    # adresse
    infos['adresse'] = driver.find_element_by_id(
        emplacement).find_element_by_class_name('txt').text

    # note
    infos['note'] = driver.find_element_by_id(
        emplacement).find_element_by_class_name('bg_note').get_attribute('innerHTML')
    noteRegex = re.compile(r'.*n(\d+)".*')
    note = noteRegex.search(infos['note'])
    infos['note'] = float(note.group(1)) / float(10)

    return(infos)

# chope les informations de tous les kebabs d'un arrondissement ou d'une
# ville et les ajoute à la liste paris


def scrapepage(paris):

    # nombre de kebabs dans l'arrondissement
    nombrearrondissement = driver.find_element_by_class_name('results').text
    nombreRegex = re.compile(r'.*sur\s(\d+)')
    resultats = nombreRegex.search(nombrearrondissement)
    nombrearrondissement = resultats.group(1)

    # nombre de kebabs sur la page
    nombrekebabs = len(driver.find_elements_by_class_name('place'))

    # si le nombre de kebabs est inférieur à 20 il y a une exception
    if(int(nombrearrondissement) < 20):
        nombrekebabs = int(nombrearrondissement)

    # ON GENERE LES EMPLACEMENTS DE TOUS LES KEBABS - ceux-ci sont repérés par
    # lieu_xx
    listeemplacements = []
    for i in range(int(nombrekebabs)):
        listeemplacements.append('lieu_' + str(i))

    # on parcours tous les emplacements et on chope les infos
    for emplacement in listeemplacements:
        paris.append(infoskebab(emplacement))

    # dans le cas où il y a plus de 20 kebabs on clique sur suivant
    if(nombrekebabs >= 20):

        # on trouve le lien
        liens = driver.find_element_by_id('col_gauche').find_element_by_class_name(
            'filter_right2').find_elements_by_tag_name('a')
        longueur = len(liens)

        # on clique sur le lien
        liens[len(liens) - 1].click()
        time.sleep(2)  # sinon le lien n'apparaît pas sur la page

        # on reproduit la même histoire (fonction récursive)
        scrapepage(paris)

# scrape tous les kebabs d'un département repéré par l'url 'url'


def scrapeville(url):
    driver.get(url)  # connexion à l'url
    paris = []  # ma future liste de kebabs
    # liste des villes/arrondissements du departement
    listeliens = driver.find_elements_by_class_name('fleche')

    # pour tous les arrondissements/villes on scrape la page
    for i in range(1, len(listeliens)):

        # je vais à la page de la ville i
        listeliens[i].click()

        # je scrape
        scrapepage(paris)

        # je fais un retour en arrière
        driver.get(url)
        listeliens = driver.find_elements_by_class_name('fleche')

        # on sort le résultat sous format csv
    toCSV = paris
    keys = toCSV[0].keys()
    with open('kebab.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

if __name__ == '__main__':
    driver = webdriver.Firefox()
    scrapeville('http://www.kebab-frites.com/kebab/paris-d54.html')
