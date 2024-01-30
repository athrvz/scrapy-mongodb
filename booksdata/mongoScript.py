from pymongo import MongoClient
import datetime
import urllib.parse

username = urllib.parse.quote_plus('<username>') # eg: user
password = urllib.parse.quote_plus('<password>') # eg: user@123
client = MongoClient("mongodb+srv://%s:%s@cluster0.5fnfp.mongodb.net/" % (username, password))

# Testing db operations
db = client.scrapy
posts = db.test_collections

doc = post = {
    "author": "mike",
    "text": "first blog"
}

post_id = posts.insert_one(post).inserted_id

print("post_id: ", post_id)