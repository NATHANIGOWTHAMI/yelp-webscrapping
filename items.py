# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpWebsiteItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    restaurant_link = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    price_range = scrapy.Field()


