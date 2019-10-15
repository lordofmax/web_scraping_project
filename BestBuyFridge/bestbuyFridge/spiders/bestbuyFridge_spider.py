from scrapy import Spider, Request
from bestbuyFridge.items import bestbuyFridgeItem
import re, math

def convert(s):
    return ("".join(s))


class bestbuyFridge(Spider):
    name = 'bestbuyFridge_spider'
    allowed_domains = ['www.bestbuy.com']
    start_urls = ['https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=category_facet%3DAll%20Refrigerators~pcmcat367400050001&sc=Global&st=refrigerator&type=page&usc=All%20Categories']
    
    def parse(self, response):
        text=response.xpath('//div[@class="left-side"]/span/text()').extract_first()

        _, num_per_page, total_num = list(map(lambda x: int(x), re.findall('\d+', text)))

        total_pages = math.ceil(total_num / num_per_page)

        result_urls = ['https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&cp={}&iht=y&keys=keys&ks=960&list=n&qp=category_facet%3Dpcmcat367400050001&sc=Global&st=refrigerator&type=page&usc=All%20Categories'.format(x) for x in range(1, total_pages+1)]
        
        for url in result_urls:
            yield Request(url, callback=self.parse_result_page)

    def parse_result_page(self, response): # 35 products list pages
        product_urls = response.xpath('//h4[@class="sku-header"]/a/@href').extract()

        product_urls = ['https://www.bestbuy.com' + x for x in product_urls]

        # price = response.xpath('//div[@class="priceView-hero-price priceView-customer-price"]/span').extract_first()
        # price1 = re.findall('\d+',price)
        # product_price = str(price1[0]) + ',' +  str(price1[1]) + '.' + str(price1[2])



        for url in product_urls:
            yield Request(url, callback=self.parse_detail_page)

    def parse_detail_page(self, response): #come back to scrapy shell

        price = ((convert(response.xpath('//div[@class="priceView-hero-price priceView-customer-price"]/span/text()').extract())).split(" "))[-1]
        try:
            ratings =((convert(response.xpath('//span[@class="c-review-average"]/text()').extract()).split(" ")))[-1]
        except IndexError:
            ratings = 'NA'    
        try:
            number_of_reviews = convert(response.xpath('//span[@class="ugc-accordion-rating-review-count"]/span/text()').extract()).split(" ")[1].replace("(",'').replace(")",'')
        except IndexError:
            number_of_reviews = 'NA'
        product_description = response.xpath('//h1[@class="heading-5 v-fw-regular"]/text()').extract()
        brand = (convert(response.xpath('//h1[@class="heading-5 v-fw-regular"]/text()').extract())).split(" ")[0]
        

        #total_capacity = response.xpath('//div[@class="row-value col-xs-6 v-fw-regular"]/text()').extract()[6]
        # freezer_capacity = response.xpath('//div[@class="row-value col-xs-6 v-fw-regular"]/text()').extract()[29]

        item = bestbuyFridgeItem()
        item['brand'] = brand
        item['product_description'] = product_description
        # item['total_capacity'] = total_capacity
        # item['freezer_capacity'] = freezer_capacity
        item['price'] = price
        item['ratings'] = ratings
        item['number_of_reviews'] = number_of_reviews
       
        yield item