import motor
import requests
from bs4 import BeautifulSoup as bs
import pymongo
import shutil
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

db_url1 = "mongodb://localhost:27004"
db_url2 = "mongodb://mongo:mongo@localhost:27002"
client = pymongo.MongoClient(db_url2)
# client = motor_asyncio.AsyncIOMotorClient(db_url)
db = client.olx

url1 = "https://www.olx.uz/d/nedvizhimost/"
url2 = "https://m.olx.uz/nedvizhimost/"
url3 = "https://www.olx.uz/d/transport/legkovye-avtomobili"
page = "?page="

coll_name = "car"

our = ['Damas', 'Labo', 'Tico',
       'Matiz', 'Nexia', 'Nexia 2',
       'Lacetti', 'Captiva', 'Epica',
       'R2', 'Malibu', 'R4', 'Gentra',
       'Orlando', 'Nexia', 'Malibu 2',
       'Tracker', 'TrailBlazer', 'Equinox',
       'Traverse', 'Tahoe', 'Cobalt', 'Spark']


def db_method(to_coll, coll_name="car"):
    if db[coll_name].find_one({"_id": to_coll["_id"]}) is not None:
        db[coll_name].replace_one({"_id": to_coll["_id"]}, to_coll)
        return 1
    else:
        db[coll_name].insert_one(to_coll)
        return 0


def splt(s: str):
    arr = s.split(": ")
    if len(arr) == 1:
        return arr[0], True
    title = arr[0]
    tags = arr[1].split(", ")
    if len(tags) == 1:
        return title, tags[0]
    for i in range(len(tags)):
        tags[i] = tags[i].strip()
    return title, tags


def money(s: str):
    arr = s.split(" ")
    sign = arr[-1]
    tmp = arr[:-1]
    price = ""
    for i in tmp:
        price += i
    price = int(price)
    if sign == "сум":
        norm_price = round(price / 11000)
    else:
        norm_price = price
    return sign, price, norm_price

'''
def download(link: str, _id: str):
    # print(link)
    # print(os.path.basename(link))
    with open(f"images/{_id}.webp", "wb") as f:
        f.write(requests.get(link).content)
    im = Image.open(f"images/{_id}.webp").convert("RGB")
    im.save(f"images/{_id}.jpg", "jpeg")
    os.remove(f"images/{_id}.webp")
    # print()
    pass
'''

def main():
    # print(res.text)
    hrefs = []
    for i in range(1, 25+1):
        hrefs.append(f"{url3}{page}{i}")
    print(hrefs)
    #print(hrefs)
    for j in hrefs:
        #print(j)
        site = requests.get(j)
        soup = bs(site.text, "html")
        result = soup.findAll('a', {"class": "css-1bbgabe"})
        for i in result:
            try:
                flag = 0
                href = f"https://www.olx.uz{i.get('href')}"
                #print(href)
                site2 = requests.get(href)
                soup2 = bs(site2.text, "html")
                to_coll = {"link": href}
                if (var := soup2.find(attrs={'class': 'css-r9zjja-Text'}).text) is not None:
                    to_coll["title"] = var
                if (var := soup2.findAll(attrs={"class": "css-7dfllt"})) is not None:
                    if "район" in var[-1].text.split(" - ")[-1]:
                        addres = (var[-2].text.split(" - ")[-1])
                    else:
                        addres = (var[-1].text.split(" - ")[-1])
                    to_coll["addres"] = addres
                if (var := soup2.find(attrs={'class': 'css-okktvh-Text'}).text) is not None:
                    sign, price, norm_price = money(var)
                    to_coll["sign"] = sign
                    to_coll["price"] = price
                    to_coll["nprice"] = norm_price
                if (var := soup2.find(attrs={'class': 'css-9xy3gn-Text'}).text) is not None:
                    to_coll["_id"] = var.split(" ")[-1]
                if (var := soup2.find(attrs={'class': 'css-g5mtbi-Text'}).text) is not None:
                    to_coll["disc"] = var
                if (var := soup2.find(attrs={'class': 'css-sfcl1s'})) is not None:
                    tags = var.findAll("p")
                    for i in tags:
                        z = i.text
                        if (tmp := i.find("span")) is not None:
                            z = tmp.text
                        title, tg = splt(z)
                        to_coll[title] = tg
                    try:
                        if to_coll["Модель"] in our:
                            to_coll["our"] = 1
                            flag = 1
                        else:
                            to_coll["our"] = 0
                    except:
                        pass
                if (var := soup2.find(attrs={'class': 'css-1bmvjcs'})) is not None:
                    try:
                        to_coll["image"] = var.get("src")
                    except:
                        to_coll["image"] = ""
                    #ilnk = var.get("src")
                    #download(ilnk, to_coll["_id"])

                if "image" in to_coll:
                    img = 1
                else:
                    img = 0
                    logger.info(f"ERROR - no image")
                    continue
                q = db_method(to_coll)
                logger.info(f"DONE - d:{q} - i:{img} -o:{flag} - {to_coll['_id']}")
                #print(to_coll)
            except BaseException as e:
                logger.error(e)
                #print(f"======================================\nERROR: {e}\n======================================")


if __name__ == "__main__":
    main()
