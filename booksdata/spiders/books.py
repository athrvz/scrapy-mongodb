from typing import Iterable
import scrapy
from scrapy.http import Request
from pathlib import Path
from pymongo import MongoClient
import urllib.parse
import datetime

def getMongoClient():
    username = urllib.parse.quote_plus('<username>') # eg: user
    password = urllib.parse.quote_plus('<password>') # eg: user@123
    client = MongoClient("mongodb+srv://%s:%s@cluster0.5fnfp.mongodb.net/" % (username, password))
    return client

def insertToDb(page, title, rating, image, price, inStock):
    client = getMongoClient()
    db = client.scrapy
    collection = db[page]
    doc = {
        "title": title,
        "rating": rating,
        "image": image,
        "inStock": inStock,
        "price": price,
        "date": datetime.datetime.utcnow()
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        # bookDetail = {}
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            # print("title: ", title)

            image = card.css(".image_container img").attrib["src"]
            image = image.replace("../../../../media", "https://books.toscrape.com/media")

            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            # print("rating", rating)

            price = card.css(".price_color::text").get()
            # print("price: ", price)

            availability = card.css(".availability::text").css(".icon-ok")
            if len(availability) > 0:
                inStock = True
            else:
                inStock = False
            # print("instock: ", inStock)
            
            insertToDb(page, title, rating, image, price, inStock)
