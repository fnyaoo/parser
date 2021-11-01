from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
import csv

option = webdriver.FirefoxOptions()
option.set_preference("dom.webdriver.enabled", False)
option.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40")


def get_all_pages ():
    url = "https://www.detmir.ru/catalog/index/name/accessori_car_interior/"
    driver = webdriver.Firefox(options=option)
    driver.get(url=url)

    time.sleep(3)

    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/button").click()
            time.sleep(1)
        except NoSuchElementException:
            break
        
    if not os.path.exists("data"):
        os.mkdir("data")

    with open('data/page.html','w', encoding='utf-8') as f:
        f.write(driver.page_source)


    driver.close()
    driver.quit()

    
def get_items(file_path):

    with open("data.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(
            (
                "id",
                "title",
                "price",
                "promo_price",
                "url"
            )
        )

    with open(file_path, encoding='utf-8') as file:
        src = file.read()
        
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="yU")
    
    
    for item in items_divs:
        item_url = item.find("div", class_="yW").find("a").get("href") #ссылка
        item_name = item.find("p", class_="N_3").getText() #название
        item_id = item_url.split("/id/")[1] #id
        item_id = item_id[:len(item_id)-1] #
        try:
            price = item.find("p", class_="Oe").getText()

            try:
                price = item.find("p", class_="Of").getText()
                promo_price = item.find("p", class_="Oe").getText()
            except AttributeError:
                promo_price = "-"
        except AttributeError:
            return

        with open("data.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(
                (
                    item_id,
                    item_name,
                    price,
                    promo_price,
                    item_url
                )
            )


def main():
    # get_all_pages ()
    get_items(file_path = "data\page.html")

if __name__ == "__main__":
    main()