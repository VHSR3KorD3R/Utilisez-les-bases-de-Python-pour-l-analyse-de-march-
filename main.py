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
    '''récupère la liste des catégories'''
    list_categories = {}
    categories = soup.find('div', class_="side_categories").find('ul').find_all('li')[1:]
    for category in categories:
        category_name = category.find("a").text.replace(' ', '').replace('\n', '')

        list_categories.update({category_name: url + category.find("a")["href"]})
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


def get_books_url_from_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    books_url = get_books_url_from_page(titles)
    next_page = soup.find(class_='next')

    if next_page is not None:
        index = url.rindex("/")
        partial_url = url[0:index + 1]
        next_page_url = partial_url + next_page.find('a')['href']
        print(next_page_url)
        books_url.update(get_books_url_from_category(next_page_url))
    return books_url

def get_books_from_each_category(soup):
    categories = get_categories(soup)
    books = {}
    for category_name, category_url in categories.items():
        print(category_name)
        books.update({category_name: get_books_from_category(category_url)})
        print(books)
    return books

def get_books_from_category(category):
    books_url = get_books_url_from_category(category)
    books = []
    for book_url in books_url.values():
        books.append(get_book_info(book_url))
    return books

def save_in_csv(books):
    
    return books

if __name__ == '__main__':
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        books_from_page = get_books_url_from_page(titles)
        '''all_categories_url = get_categories(soup)
        category_url = all_categories_url[1]
        books = get_books_from_category(category_url)
        print(len(books))
        for url in books.values():
            print(get_book_info(url))'''
        get_books_from_each_category(soup)

