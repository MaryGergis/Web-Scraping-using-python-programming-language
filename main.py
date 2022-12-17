import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

phone_description = []
more_details = []
price_before_discount = []
price_after_discount = []
links_phones = []
links = []
page_num = 1

while True:
    try:
        url = requests.get(f'https://dream2000.com/mobiles/samsung.html?_=1671293810281&p={page_num}')
        src = url.content
        soup = BeautifulSoup(src, 'html.parser')

        page_limit = 80
        if page_num > page_limit // 20:
            print("pages ended ")
            break

        details = soup.find_all("strong", {"class": "product name product-item-name"})
        for i in details:
            phone_description.append(i.text)

        old_price = soup.find_all("span",  {"class": "old-price"})
        for i in old_price:
            price_before_discount.append(i.text)

        special_price = soup.find_all("span", {"class": "special-price"})
        for i in special_price:
            price_after_discount.append(i.text)

        for link in soup.findAll('a', {"class": "product-item-link"}):
            links.append(link.get('href'))

        page_num += 1
        print("page switched")
    except:
        print("an error occurred")
        break


for i in links:
    url = requests.get(i)
    src = url.content
    soup = BeautifulSoup(src, 'html.parser')
    details = soup.find("div", {"class": "value", "itemprop": "description"})
    for i in details:
        more_details.append(i.text)


file_list = [phone_description, more_details, price_before_discount, price_after_discount, links_phones]
exported = zip_longest(*file_list)

with open("E:/Mary/samsung_phones.csv", "w") as file:
    wr = csv.writer(file)
    wr.writerow(["phone_description", "more_details", "price_before_discount", "price_after_discount", "links_phones"])
    wr.writerows(exported)