import requests
from bs4 import BeautifulSoup
import csv

#retour du lien url

input_url = 'https://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html'
def book_data(input_url):
    url = input_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)

# Retour la valeur upc
    retour_Upc = soup.find('th', string='UPC').find_next('td')
       
# Retour du Titre
    retour_Title = soup.find('h1')
    
# Retour du prix en TTC
    retour_TTC = soup.find('th', string='Price (incl. tax)').find_next('td')

# Retour du prix en HT
    retour_HT = soup.find('th', string='Price (excl. tax)').find_next('td')

# Retour du nombre en stock
    retour_Available = soup.find('th', string='Availability').find_next('td')

# Retour de la description
    retour_Description = soup.find('h2').find_next()

# Retoure de la catégorie
    retour_Category = soup.find('li', class_='active').find_previous('a')

# Retour de la notation
    retour_Rating = soup.find('th', string='Number of reviews').find_next('td')

# Retour du lien de l'image
    retour_Image = soup.select_one('img')['src'].replace("../..", "https://books.toscrape.com")

# Création du fichier cvs


    retour_book = [
        url,
        retour_Upc.text,
        retour_Title.text,
        retour_TTC.text,
        retour_HT.text,
        retour_Available.text,
        retour_Description.text,
        retour_Category.text,
        retour_Rating.text,
        retour_Image
    ]
    return retour_book


        
if __name__ == "__main__":
    url = 'https://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html'
    retour_book = book_data(url)

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
        writer.writerow(retour_book)
    