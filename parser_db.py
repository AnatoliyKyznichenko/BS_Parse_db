import requests
from bs4 import BeautifulSoup
import sqlite3


def book_parsing():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    query = """CREATE TABLE IF NOT EXISTS book(
    Title TEXT,
    Availability VARCHAR(20),
    Price TEXT
    )"""

    cursor.execute(query)

    url = 'https://book24.ua/ua/catalog/letnee_chtenie_po_shkolnoy_programma/'
    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    page_count = int(soup.find('div', class_='nums').find_all('a', class_='dark_link')[-1].text.strip())
    print(f'Всего страниц {page_count}...')
    for page in range(1, page_count + 1):
        print(f'[INFO] Обработка {page} страницы')
        url = f'https://book24.ua/ua/catalog/letnee_chtenie_po_shkolnoy_programma/?PAGEN_1={page}'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        items = soup.select('.inner_wrap > .item_info')
        for item in items:
            try:
                title = item.select(".item-title > a > span")
                title = title[0].text
                Availability = soup.select('.item-stock > span')[1].text.strip()
                sale = item.select('.cost > .price_matrix_wrapper > .price > span > .price_value')[0].text.strip()
                cursor.execute("INSERT INTO book VALUES(?,?,?)", (title, Availability, sale,))
                db.commit()
            except Exception as Error:
                pass


if __name__ == '__main__':
    book_parsing()