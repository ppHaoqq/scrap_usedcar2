from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import math


#ページスクロール
def get_num(soup):
    center_nav_block = soup.find('div', class_='centernavblock')
    _total_record = center_nav_block.find('span', class_='totalrecord').text
    if ',' in _total_record:
        total_record = int(_total_record.replace(',', ''))
        num = math.ceil(total_record / len(outer_details))
        return num
    else:
        total_record = math.ceil(int(_total_record))
        num = math.ceil(total_record / len(outer_details))
        return num


def get_df(items):
    df = pd.DataFrame()

    df['id'] = items[0]
    df['years'] = items[1]
    df['grades'] = items[2]
    df['mileages'] = items[3]
    df['base_prices'] = items[4]
    df['total_prices'] = items[5]

    return df



kw = input('車種を入力してください>>')  # 'RX-8'
base_url = 'https://www.goo-net.com/cgi-bin/fsearch/goo_used_search.cgi?category=USDN&phrase={}&query={}'.format(kw, kw)
html = requests.get(base_url).text
soup = bs(html, 'html.parser')
num = get_num(soup)

id_s = []
years = []
grades = []
mileages = []
base_prices = []
total_prices = []
items = [id_s, years, grades, mileages, base_prices, total_prices]

for i in range(num):
    url = 'https://www.goo-net.com/cgi-bin/fsearch/goo_used_search.cgi?category=USDN&phrase={}&query={}&page={}'.format(
        kw, kw, i)
    html2 = requests.get(url).text
    soup2 = bs(html2, 'html.parser')
    outer_details = soup2.find_all('div', class_='outerDetail')
    for outer_detail in outer_details:
        img_url = outer_detail.find('img', src='https://')

        text_detail = outer_detail.find('div', class_='textDetail')
        bottom_detail = text_detail.find('div', class_='bottomDetail')

        id_ = text_detail.find('a').get('href')
        id_s.append(id_)

        year = bottom_detail.find('dl', class_='model_year').text.replace('\n', '').strip('年式').strip()
        years.append(year)

        grade = ''
        grades.append(grade)

        mileage = bottom_detail.find('dl', class_='mileage').text.replace('\n', '').strip('走行距離').strip()
        mileages.append(mileage)

        base_price = (bottom_detail.find('div', class_='base_price').find_all('dl')[0].text.strip().strip('本体価格\n'))
        base_prices.append(base_price)

        total_price = bottom_detail.find('div', class_='base_price').find_all('dl')[1].text.strip().strip('合計金額\n')
        total_prices.append(total_price)

df = get_df(items)





