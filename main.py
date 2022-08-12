import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/'

def get_books_url_from_page(titles):
    books = {}
    for title in titles:
        temp = title.find('h3').find('a')['title']
        book_url = url + title.find('h3').find('a')['href']
        books.update({temp: book_url})
    return books

def get_categories(soup):
    categories = soup.find(class_="side_categories")
    for category in categories:
        temp = category.find('a')
        print(type(temp))

if __name__ == '__main__':
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        books_from_page = get_books_url_from_page(titles)
        get_categories(soup)