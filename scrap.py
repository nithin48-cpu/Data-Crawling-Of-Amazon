import requests
from bs4 import BeautifulSoup

import csv

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

import time
import re
from tqdm.auto import tqdm

driver = Chrome()

product_names = []
prices = []
links = []
ratings = []
reviews = []

list1 = [product_names, links, prices, ratings, reviews]


def pop_index(l):
    list2 = []
    for l in list1:
        l.pop(0)
        list2.append(l)
    return list2


# --------------------------part1-----------------------------------------------

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
for i in tqdm(range(1, 21), desc="Data From Amazon"):
    driver.get(url)
    # time.sleep(1000)
    # print("count: "+str(i)+" "+url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all('div', 'a-section a-spacing-small a-spacing-top-small')
    temp = 0
    for div in divs:
        if temp == 0:
            temp += 1
            continue
        product = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        if product is None:
            product_names.append(None)
        else:
            product_names.append(product.text)

        link = div.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        if link is None:
            links.append(None)
        else:
            links.append("https://www.amazon.in" + link.get("href"))

        price = div.find('span', 'a-price-whole')
        if price is None:
            prices.append(None)
        else:
            prices.append(price.text)

        rate = div.find('span', 'a-icon-alt')
        if rate is None:
            if link is None:
                pass
            ratings.append(None)
        else:
            ratings.append(rate.text.split()[0])

        review = div.find('span', 'a-size-base s-underline-text')
        if review is None:
            if link is None:
                pass
            reviews.append(None)
        else:
            reviews.append(review.text)

    divs = soup.find('div', 'a-section a-text-center s-pagination-container')
    a = divs.find('a', 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator')
    if not a:
        print("completed")
        break
    temp = 0
    url = "https://www.amazon.in" + a.get("href")

print("length of products: ", len(product_names))
print("length of prices: ", len(prices))
print("length of links: ", len(links))
print("length of ratings: ", len(ratings))
print("length of reviews: ", len(reviews))

driver.quit()
csv_file = open("part1_data.csv", 'w', newline="", encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['product_names', 'prices', 'links', 'ratings', 'reviews'])

for product, price, link, rate, review in zip(product_names, prices, links, ratings, reviews):
    csv_writer.writerow(
        [product, price, link, rate, review])
csv_file.close()
print("SAVED THE FILE!!! part1_data.csv")

# ------------------------part2 starts----------------------------------------------

ASINS = []
Manufacturers = []
Product_descriptions = []
Discriptions = []

option = ChromeOptions()
option.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

driver = Chrome(options=option)

count = 0
temp = 0

pattern = "^https://aax-eu.amazon.in.*"

for link in tqdm(links[:200], desc="Data About Bags"):
    if temp >= 200:
        print("Reached 200")
        break

    result = re.search(pattern, link)
    if result:
        driver.get(link)
        # print("count: ", count, " " + link)
    else:
        driver.get(link)
        # print("count: ", count, link)

    count += 1
    # time.sleep()
    soup = BeautifulSoup(driver.page_source, 'html5lib')

    table = soup.find('div', "a-section table-padding")
    if table is None:
        ul = soup.find('ul', "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
        # print(ul)
        if ul is None:
            print("ASINS count: ", count, link)
            ASINS.append(None)
        else:
            spans = ul.find_all('span', 'a-list-item')
            list1 = []
            list2 = []
            for s in spans:
                list1.extend(s.find_all('span'))
            for s in list1:
                s = s.text.replace(':', '').strip()
                s = s.replace(' ', '').strip()
                s = s.replace('\n', '').strip()
                s = s.replace('\u200f\u200e', '').strip()
                s = s.replace('\u200e', '').strip()
                list2.append(s)
                # print(list1)
            if 'ASIN' in list2:
                index_ASIN = list2.index('ASIN')
                # print(list2[index_ASIN+1])
                ASINS.append(list2[index_ASIN + 1])
            else:
                ASINS.append(None)
    else:
        ASINS.append(table.find('td', "a-size-base prodDetAttrValue").text.strip())

    table = soup.find('div', "a-expander-content a-expander-section-content a-section-expander-inner")
    if table is None:
        ul = soup.find('ul', "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
        # print(ul)
        if ul is None:
            print("Manufacturers count: ", count, link)
            Manufacturers.append(None)
        else:
            spans = ul.find_all('span', 'a-list-item')
            list1 = []
            list2 = []
            for s in spans:
                list1.extend(s.find_all('span'))
            for s in list1:
                s = s.text.replace(':', '').strip()
                s = s.replace(' ', '').strip()
                s = s.replace('\n', '').strip()
                s = s.replace('\u200f\u200e', '').strip()
                s = s.replace('\u200e', '').strip()
                list2.append(s)
            # print(list2)
            if 'Manufacturer' in list2:
                index_Manufacturer = list2.index('Manufacturer')
                # print(temp2[index_Manufacturer])
                Manufacturers.append(list2[index_Manufacturer + 1])
                # Manufacturers.append(th[1].text.strip())
            else:
                Manufacturers.append(None)
    else:
        # th = table.find_all('td', "a-size-base prodDetAttrValue")
        # if th is None:
        #     print("Manufacturers count: ", count,link)
        #     Manufacturers.append(None)
        # else:
        th = table.find_all('th')
        td = table.find_all('td')
        # print(th)
        list1 = []
        list2 = []
        temp1 = []
        temp2 = []
        for t in th:
            list1.append(t.text.strip())
        for t in td:
            list2.append(t.text.strip())
        for s in list1:
            s = s.replace(':', '').strip()
            s = s.replace(' ', '').strip()
            s = s.replace('\n', '').strip()
            s = s.replace('\u200f\u200e', '').strip()
            s = s.replace('\u200e', '').strip()
            temp1.append(s)
        for s in list2:
            s = s.replace(':', '').strip()
            s = s.replace(' ', '').strip()
            s = s.replace('\n', '').strip()
            s = s.replace('\u200f\u200e', '').strip()
            s = s.replace('\u200e', '').strip()
            temp2.append(s)
        if 'Manufacturer' in temp1:
            index_Manufacturer = temp1.index('Manufacturer')
            # print(temp2[index_Manufacturer])
            Manufacturers.append(temp2[index_Manufacturer])
            # Manufacturers.append(th[1].text.strip())
        else:
            Manufacturers.append(None)

    div = soup.find('div', "aplus-v2 desktop celwidget")
    # print(div)
    if div is None:
        div = soup.find('div', "a-row feature")
        if div is None:
            # print("Product_descriptions count: ", count, link)
            Product_descriptions.append(None)
        else:
            tag = div.find('span')
            if tag is None:
                # print("Product_descriptions count: ", count, link)
                Product_descriptions.append(None)
            else:
                Product_descriptions.append(tag.text.replace('\n', '').strip())
    else:
        Product_description = div.find_all('p')
        if Product_description is None or len(Product_description) == 0:
            div = soup.find('div', "a-row feature")
            if div is None:
                # print("Product_descriptions count: ", count, link)
                Product_descriptions.append(None)
            else:
                tag = div.find('span')
                if tag is None:
                    # print("Product_descriptions count: ", count, link)
                    Product_descriptions.append(None)
                else:
                    Product_descriptions.append(tag.text.replace('\n', '').strip())
        else:
            str1 = ''
            for dis in Product_description:
                str1 += dis.text
            Product_descriptions.append(str1.replace('\n', '').strip())

    Discription = ''
    div = soup.find('div', "a-section a-spacing-medium a-spacing-top-small")
    if div is None:
        ul = soup.find('ul', "a-unordered-list a-vertical a-spacing-mini")
        if ul is None:
            ul = soup.find('ul', "a-unordered-list a-vertical a-spacing-small")
            if ul is None:
                print("Discriptions count1: ", count, link)
                Discriptions.append(None)
            else:
                tags = ul.find_all('span')
                if tags is None:
                    print("Discriptions count2: ", count, link)
                    Discriptions.append(None)
                else:
                    for tag in tags:
                        Discription += tag.text
                    Discription.replace('<br>', '')
                    Discriptions.append(Discription.replace('\n', '').strip())
        else:
            # print(ul)
            tags = ul.find_all('span')
            if tags is None:
                print("Discriptions count3: ", count, link)
                Discriptions.append(None)
            else:
                for tag in tags:
                    Discription += tag.text
                Discription.replace('<br>', '')
                Discriptions.append(Discription.replace('\n', '').strip())
    else:
        tags = div.find_all('span', 'a-list-item')
        if tags is None:
            print("Discriptions count4: ", count, link)
            Discriptions.append(None)
        else:
            for tag in tags:
                Discription += tag.text
                Discription.replace('<br>', '')
            Discriptions.append(Discription.replace('\n', '').strip())
    temp += 1

print("length of ASINS: ", len(ASINS))
print("length of Manufacturers: ", len(Manufacturers))
print("length of Product_descriptions: ", len(Product_descriptions))
print("length of Discriptions: ", len(Discriptions))

csv_file = open("part2_data.csv", 'w', newline="", encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['ASIN', 'Manufacturer', 'Product Description', 'Description'])
for ASIN, Manufacturer, Product_description, Discription in zip(ASINS, Manufacturers, Product_descriptions,
                                                                Discriptions):
    csv_writer.writerow(
        [ASIN, Manufacturer, Product_description, Discription])
csv_file.close()
print("SAVED THE FILE!!! part2_data.csv")
