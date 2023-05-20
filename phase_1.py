def extraction_un_livre(url):

    import requests
    import re

    from bs4 import BeautifulSoup

    informations = {}

    # URL_BASE = "https://books.toscrape.com"
    URL = url

    TIMEOUT_REQUEST = 15

    page_html = requests.get(URL, timeout=TIMEOUT_REQUEST)

    soup = BeautifulSoup(page_html.content, 'html.parser')

    selection_html = soup.select(".product_main h1")
    for element in selection_html:
        title = element.get_text()
    
    # Extraction.T.L : Extraction UPC, Price (incl. tax), Price (excl. tax), availability, product_description, Number of reviews, image_url, category

    selection_html = soup.select("table.table-striped > tr")
    liste = {}
    for element in selection_html:
        element_valeur = element.find("th").get_text()
        el_valeur = element.find('td').get_text()
        liste[element_valeur] = el_valeur

    # Extraction de la description du livre
    selection_html = soup.select('article.product_page > p')
    valeur = []
    for i in selection_html:
        valeur.append(i.text)
    product_description = valeur[0]

    # Extraction de la category
    selection_html = soup.select("a[href*=\/books\/]")
    category = selection_html[0].get_text()
    
    # Extraction de l'image du livre
    selection_html = soup.find_all('img')
    for image in selection_html:
        url_src = image['src']
    image_url = url_src

    # Extraction du titre du livre
    informations["title"] = title

    # 
    informations.update(liste)
    informations["image_url"] = image_url
    informations["category"] = category
    informations["product_description"] = product_description
    
    return informations

def liste_category(url):
    
    import requests
    
    import re

    from bs4 import BeautifulSoup

    TIMEOUT_REQUEST = 15

    page_html = requests.get(url, timeout=TIMEOUT_REQUEST)

    soup = BeautifulSoup(page_html.content, 'html.parser')

    categories = []
    selection_html = soup.select(".side_categories > ul > div")
    for index in selection_html:
        url_tmp = selection_html

    return(categories)


# Programme principal


import re
URL_BASE = "https://books.toscrape.com"

# Transformation des données récupérées 

donnees_extraites = extraction_un_livre("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
#print(f"donnees_extraites : \n \n {donnees_extraites}")

# E.Transformation.L : traitement de mise en forme des données extraites : suppression des champs Tax, Availability et Product type. Mise en format numérique des prix, isolation de la valeur du nombre de reviews, repise en ordre des données en correspondance aux attendus.

price_inc = donnees_extraites.get('Price (incl. tax)')
price_includ = (price_inc).replace("£", "")
price_include_tax = price_includ
price_exc = donnees_extraites.get('Price (excl. tax)')
price_exclud = (price_exc).replace("£", "")
price_exclude_tax = price_exclud
availability = donnees_extraites.get('Availability')
available = (re.sub(r'\D', "", availability))
nbre_review = donnees_extraites.get('Number of reviews')
number_of_reviews = nbre_review
img_url = donnees_extraites.get('image_url')
valeur = str(img_url).replace("../", "")
image_url = URL_BASE + '/' + str(valeur)

donnees_purgees = {}
donnees_purgees['product_page_url'] = 'A ajouter'
donnees_purgees['universal_ product_code (upc)'] = donnees_extraites.get('UPC')
donnees_purgees['title'] = donnees_extraites.get('title')
donnees_purgees['price_including_tax'] = price_include_tax
donnees_purgees['price_excluding_tax'] = price_exclude_tax
donnees_purgees['number_available'] = available
donnees_purgees['product_description'] = donnees_extraites.get('product_description')
donnees_purgees['category'] = donnees_extraites.get('category')
donnees_purgees['review_rating'] = number_of_reviews 
donnees_purgees['image_url'] = image_url

# donnees_a_pousser = ''
# créer la ligne des en-têtes en données à envoyer vers le .csv
entetes = ""

for key in donnees_purgees:
    entetes = entetes + "\"" + str(key) + "\","
entetes_vers_csv = entetes[:-1] + '\n'
print(f"Donnees_vers_csv : {entetes_vers_csv}")

# Ajout des lignes de données dans le fichier csv.
donnees = ''
for value in donnees_purgees:
    donnees = donnees + "\"" + donnees_purgees[value] + "\","
donnees_vers_csv = donnees[:-1] + '\n'
print(f"Donnees_vers_csv : {donnees_vers_csv}")

# Creation du fichier de données cible

fichier = open("donnees.csv", "a+")
fichier.close()

# Ecriture des données dans le fichier : Entête + informations

fichier = open("donnees.csv", "a")

fichier.write(entetes_vers_csv)
fichier.write(donnees_vers_csv)
fichier.close()