import scrapy
from scrapy.http import Request
from ..items import YelpWebsiteItem



class YelpSpider(scrapy.Spider):
    name = 'yelp'
    allowed_domains = ['yelp.com']
    #start_urls = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=Mount+Pleasantc%2CMI+48858&start=0']

    def start_requests(self):
        url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Mount+Pleasantc%2CMI+48858&start=0'
        yield scrapy.Request(url,callback=self.parse,dont_filter = True)

    def parse(self, response,pg_no=1,start=0):
        items = YelpWebsiteItem()
        products = response.xpath("//div[@class=' container__09f24__mpR8_ hoverable__09f24__wQ_on border-color--default__09f24__NPAKY']")

        for product in products:

            title = product.xpath(".//h3[@class='css-1agk4wl']//a/text()").get()
            restaurant_link = product.xpath(".//h3[@class='css-1agk4wl']//a/@href").get()
            if 'https://www.yelp.com' not in restaurant_link:
                restaurant_link = f'https://www.yelp.com{restaurant_link}'
            rating = product.xpath(".//div[@class=' five-stars__09f24__mBKym five-stars--regular__09f24__DgBNj display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY']/@aria-label").get()
            if rating == None :
                rating = 0
            else:
                rating = rating.split(" ")[0]
            review_count = product.xpath(".//div[@class=' display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY']//span[@class=' css-chan6m']/text()").get()
            if review_count == None:
                review_count = 0
            else:
                review_count = review_count.split(" ")[0].split("(")[1]
            description = product.xpath('.//p[@class="css-16lklrv"]/text()').get()
            price_range = response.xpath("//span[@class='priceRange__09f24__mmOuH css-chan6m']/text()").get()
            image_url = response.xpath("//img[@class=' css-xlzvdl']/@src").get()


            items['title'] = title
            items['restaurant_link'] = restaurant_link
            items['rating'] = rating
            items['review_count'] = review_count
            items['description'] = description
            items['price_range'] = price_range
            items['image_url'] = image_url

            yield items

        total_pages = response.xpath("//span[@class=' css-chan6m']/text()").extract()[-1].split(" ")[-1]
        if int(total_pages) >= pg_no:
            pg_no += 1
            start += 10
            next_page_url = f'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Mount+Pleasantc%2CMI+48858&start={start}'

            if next_page_url:
                #print(next_page_url)
                yield Request(url=next_page_url,callback=self.parse,dont_filter = True,
                              cb_kwargs={
                                  'start':start,
                                  'pg_no': pg_no}
                              )
