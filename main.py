import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/'

def get_books_url_from_page(titles):
    books = {}
    for title in titles:
        temp = title.find('h3').find('a')['title']
        book_url = url +'catalogue/'+ title.find('h3').find('a')['href'].replace('../../../', '')
        books.update({temp: book_url})
    return books

def get_categories(soup):
    list_categories = []
    categories = soup.find('div', class_="side_categories").find('ul').find_all('li')[1:]
    for category in categories:
        list_categories.append(url + category.find("a")["href"])
    return list_categories

def get_book_info(url):
    book = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = soup.select_one("article > p").text
    tds = soup.find('table', class_='table table-striped').findAll("td")
    upc = tds[0].text
    price_including_tax = float(tds[3].text.replace('Â£', ''))
    price_excluding_tax = float(tds[2].text.replace('Â£', ''))
    number_available = int(tds[5].text.replace('In stock (', '').replace(' available)', ''))
    review_rating = soup.find('p', class_='star-rating')
    review_rating = review_rating.get('class')[1]
    image_url = 'http://books.toscrape.com/' + soup.find('div',class_='item active').find('img')['src'].replace('../../', '')
    category = soup.find('ul', class_='breadcrumb').findNext('li').findNext('li').findNext('li').text
    print(category)
    book = dict([
        ('product_page_url', url),
        ('universal_ product_code', upc),
        ('price_including_tax', price_including_tax),
        ('price_excluding_tax', price_excluding_tax),
        ('number_available', number_available),
        ('product_description', description),
        ('category', category),
        ('review_rating', review_rating),
        ('image_url', image_url),
    ])
    return book

def get_books_from_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    books = get_books_url_from_page(titles)
    return books

if __name__ == '__main__':
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        books_from_page = get_books_url_from_page(titles)
        all_categories_url = get_categories(soup)
        category_url = all_categories_url[1]
        books = get_books_from_category(category_url)
        book_url = list(books.items())[1][1]
        print(book_url)
        get_book_info(book_url)
