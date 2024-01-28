import requests
from bs4 import BeautifulSoup
import csv

#retour du lien url
url = input('Entrez votre lien: ')
#url = 'https://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)

# Retour la valeur upc
def valeurs_upc():
    retour_Upc = soup.find('th', string='UPC').find_next('td')
    return retour_Upc.text
    
# Retour du Titre
def titres():
    retour_Title = soup.find('h1')
    return retour_Title.text

# Retour du prix en TTC
def prix_ttc():
    retour_TTC = soup.find('th', string='Price (incl. tax)').find_next('td')
    return retour_TTC.text

# Retour du prix en HT
def prix_ht():
    retour_HT = soup.find('th', string='Price (excl. tax)').find_next('td')
    return retour_HT.text

# Retour du nombre en stock
def stocks():
    retour_Available = soup.find('th', string='Availability').find_next('td')
    return retour_Available.text

# Retour de la description
def descriptions():
    retour_Description = soup.find('h2').find_next()
    return retour_Description.text

# Retoure de la catégorie
def caterories():
    retour_Category = soup.find('li', class_='active').find_previous('a')
    return retour_Category.text

# Retour de la notation
def notations():
    retour_Rating = soup.find('th', string='Number of reviews').find_next('td')
    return retour_Rating.text

# Retour du lien de l'image
def images():
    retour_Image = soup.select_one('img')['src'].replace("../..", "https://books.toscrape.com")
    return retour_Image

# Création du fichier cvs

en_tete = [
    'product_page_url',
    'universal_product_code',
    'title',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'product_description',
    'category',
    'review_rating',
    'image_url'
    ]

retour_book = {
    'product_page_url': url,
    'universal_product_code': valeurs_upc(),
    'title': titres(),
    'price_including_tax': prix_ttc(),
    'price_excluding_tax': prix_ht(),
    'number_available': stocks(),
    'product_description': descriptions(),
    'category': caterories(),
    'review_rating': notations(),
    'image_url': images()
    }

with open('book.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)
    writer.writerow(retour_book.values())

