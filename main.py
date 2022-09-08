import re
import requests
import pandas as pd
import os
import shutil

from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/'


def get_books_url_from_page(titles):
    '''récupère toutes les url des livres d'une page'''
    print('get_books_url_from_page')
    books = {}
    for title in titles:
        temp = title.find('h3').find('a')['title']
        # trouve le titre du livre et le transforme en lien
        book_url = url + 'catalogue/' + title.find('h3').find('a')['href'].replace('../../../', '')
        # ajoute au dictionnaire le titre et lien du livre
        books.update({temp: book_url})
    return books


def get_categories(soup):
    '''récupère la liste des catégories'''
    print('get_categories')
    list_categories = {}
    # Récupère toutes les catégories
    categories = soup.find('div', class_="side_categories").find('ul').find_all('li')[1:]
    for category in categories:
        # Néttoie le nom de catégories
        category_name = category.find("a").text.replace(' ', '').replace('\n', '')
        # ajoute au dictionnaire le nom de la catégorie et son lien
        list_categories.update({category_name: url + category.find("a")["href"]})
    return list_categories


def get_book_info(url):
    '''récupère toutes les infos des livres'''
    print('get_book_info')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = re.sub(r"[^a-zA-Z0-9 ]", "", soup.select_one("article > p").text.replace(',', ' '))
    tds = soup.find('table', class_='table table-striped').findAll("td")
    upc = tds[0].text
    price_including_tax = float(tds[3].text.replace('Â£', ''))
    price_excluding_tax = float(tds[2].text.replace('Â£', ''))
    number_available = int(tds[5].text.replace('In stock (', '').replace(' available)', ''))
    # review rating est la note donnée au livre sous forme d'étoile, mais est stocké sous forme de chiffre en toute lettre
    review_rating = soup.find('p', class_='star-rating')
    review_rating = review_rating.get('class')[1]
    image_url = 'http://books.toscrape.com/' + soup.find('div', class_='item active').find('img')['src'].replace(
        '../../', '')
    category = soup.find('ul', class_='breadcrumb').findNext('li').findNext('li').findNext('li').text.replace('\n', '')
    title = soup.find('h1').text
    book = dict([
        ('product_page_url', url),
        ('universal_product_code', upc),
        ('title', title),
        ('price_including_tax', price_including_tax),
        ('price_excluding_tax', price_excluding_tax),
        ('number_available', number_available),
        ('product_description', description),
        ('category', category),
        ('review_rating', review_rating),
        ('image_url', image_url),
    ])
    return book


def get_books_url_from_category(url):
    '''récupère toutes les url des livres d'une catégorie'''
    print('get_books_url_from_category')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    books_url = get_books_url_from_page(titles)
    next_page = soup.find(class_='next')

    if next_page is not None:
        index = url.rindex("/")
        partial_url = url[0:index + 1]
        next_page_url = partial_url + next_page.find('a')['href']
        #appel récursif de la fonction pour les catégories qui ont plusieurs pages de livres
        books_url.update(get_books_url_from_category(next_page_url))
    return books_url


def get_books_from_each_category(soup):
    '''récupère toutes les infos des tous les livres de chaque catégorie'''
    print('get_books_from_each_category')
    categories = get_categories(soup)
    books = {}
    for category_name, category_url in categories.items():
        books.update({category_name: get_books_from_category(category_url)})
    return books


def get_books_from_category(category):
    '''récupère toutes les infos des tous les livres d'une catégorie'''
    print('get_books_from_category')
    books_url = get_books_url_from_category(category)
    books = []
    for book_url in books_url.values():
        books.append(get_book_info(book_url))
    return books


def save_in_csv(soup):
    '''sauvegarde toutes les infos des livre dans un csv'''
    print('save_in_csv')
    all_books = get_books_from_each_category(soup)
    header = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
              "number_available", "product_description", "category", "review_rating", "image_url"]
    cwd = os.getcwd()
    target_dir = cwd + '\csv'
    if os.path.exists(target_dir) is False:
        os.mkdir(target_dir)
    for category, books in all_books.items():
        df = pd.DataFrame()
        for book in books:
            df = pd.concat([df, pd.DataFrame([book])])
        if os.path.exists(target_dir + '\\' + category + ".csv") is False:
            df.to_csv(target_dir + '\\' + category + ".csv", header=header, sep=',', index=False, mode='a')
        else:
            os.remove(target_dir + '\\' + category + ".csv")
            df.to_csv(target_dir + '\\' + category + ".csv", header=header, sep=',', index=False, mode='a')
    return all_books


def download_image(all_books):
    '''télécahrge les images des couvertures de livre'''
    print('download_image')
    cwd = os.getcwd()
    target_dir = cwd + '\images'
    if os.path.exists(target_dir) is False:
        os.mkdir(target_dir)
    for category, books in all_books.items():
        for book in books:
            image_url = book.get('image_url')
            # nettoyage du titre pour éviter des caratères qui sauterait l'extension (.jpg)
            filename_cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", book.get('title')) + '.jpg'
            r = requests.get(image_url, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open(target_dir + '\\' + filename_cleaned, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)


if __name__ == '__main__':
    response = requests.get(url)
    if response.ok:
        print('début')
        soup = BeautifulSoup(response.text, 'html.parser')
        all_books = save_in_csv(soup)
        download_image(all_books)
        print('fin')
