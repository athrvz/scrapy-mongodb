# scrapy-mongodb
## Data scraping application using scrapy
Scrape book data like title, price, rating, etc. <br>
Use a non-relational data store (mongodb) to store this scraped data as a document.

Steps: 
1. pip install scrapy
2. connect to mongodb by connection string and run the js script
3. scrapy startproject <project-name>
4. scrapy genspider <example> <site to scrape (example.com)>
    eg: scrapy genspider books toscrape.com
5. cd to the folder which has spiders dir -> "scrapy crawl <example>"
    eg: scrapy crawl books
