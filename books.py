import requests
from bs4 import BeautifulSoup
import csv
from PIL import Image
from io import BytesIO

directory = 'Images'
input_url = 'https://books.toscrape.com/catalogue/red-hoodarsenal-vol-1-open-for-business-red-hoodarsenal-1_729/index.html'
def book_data(input_url, directory):
    url = input_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


# Retour la valeur upc
    retour_Upc = soup.find('th', string='UPC').find_next('td')
       
# Retour du Titre
    retour_Title = soup.find('h1')
    image_Title = soup.find('h1').text\
        .replace("'","").replace("\\","").replace(",","").replace("-","_")\
	    .replace(":","").replace("?","").replace(")","").replace(".","")\
        .replace("(","").replace("*","").replace("!","").replace("#","")\
		.replace(" ","_").replace("&","").replace("/","_").replace("\"","_")
    
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
    Image2Save = requests.get(retour_Image)
    image = Image.open(BytesIO(Image2Save.content))
    image_png = f"{directory}/{image_Title}.jpeg"
    image.save(image_png, "JPEG")
    image.close
    image_png = f"{image_Title}.jpeg"
    

# Création du fichier cvs

    retour_book = [
        url,
        retour_Upc.text,
        retour_Title.text,
        retour_TTC.text,
        retour_HT.text,
        retour_Available.text,
        retour_Description.text.replace('"',"'").replace(";", ","),
        retour_Category.text,
        retour_Rating.text,
        image_png
    ]
    
    return retour_book

        
if __name__ == "__main__":
    
    retour_book = book_data(input_url, directory)

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
 

    with open('books.csv', 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow(retour_book)
