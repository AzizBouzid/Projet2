import requests
from bs4 import BeautifulSoup
from books import book_data
import csv
import os
from genericpath import exists

# Si la page contient next la fonction retourne vrai

url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Enregistre les catégories du site dans la liste (liste_categories) 
list_categories = []
list_categories = soup.find(
    class_='nav-list').find_next('li').text.replace(" ", "").split()
del (list_categories[0])

# Enregistre les liens de la catégorie
liste_url_categorie = []
lien = soup.find('ul', class_='nav nav-list').find_all('a')
for lien_categorie in lien:
    total_categorie = url + lien_categorie.get('href')
    liste_url_categorie.append(total_categorie)
del (liste_url_categorie[0])

# Enregistre les données de chaque livre de la catégorie dans un fichier csv
# Enregistre les images des livres de chaque catégorie
x = 0
while x < len(liste_url_categorie):
    url_categorie = liste_url_categorie[x]
    lien_books = []
    
    while True:
        response = requests.get(url_categorie)
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        # Enregistre les liens des livres de la catégorie
        for book in books:
            url_book = book.find('h3').a
            lien_books.append(url + "catalogue" + "/" + url_book['href'].strip("../"))

        if soup.find('li', class_='next'):
            url_categorie = liste_url_categorie[x]
            suivante = soup.find('li', class_='next').find('a').get('href')
            url_categorie = url_categorie.rstrip('index.html')
            url_categorie = url_categorie + suivante
            
        else:
            break
   
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
    
    nom_fichier = list_categories[x]
    
    if not exists(list_categories[x]):
        repertoire = os.mkdir(list_categories[x])
    print("Traitement en cours de la catégorie: " + list_categories[x])
    print("Nombre des livres: " + str(len(lien_books)))

    i = 0
    fichier = f"{nom_fichier}/{nom_fichier}.csv"    
    
    with open(fichier, 'a', encoding='UTF-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';', quoting=csv.QUOTE_ALL)
        writer.writerow(en_tete)

        while i < len(lien_books):
            retour_book = book_data(lien_books[i], nom_fichier)
            writer.writerow(retour_book)
            i += 1
            
    x += 1
    
def page_suivante(soup):

    if soup.find('li', class_='next'):
        return True