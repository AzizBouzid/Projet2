import requests
from bs4 import BeautifulSoup
import csv
import books



url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

Categories = []
Categorie = soup.find_all('h3')
for categorie in Categorie:
    a = categorie.find('a')
    lien_livre = a['href'].replace('../../..', 'https://books.toscrape.com/catalogue')
    Categories.append(lien_livre)

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

with open('book.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)
    i = 0
    nombre = len(Categories)
    while i < nombre:
        writer.writerow(books.book_data(Categories[i]))
        i += 1
 