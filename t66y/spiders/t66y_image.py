# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from t66y.items import T66YItem


class T66yImageSpider(scrapy.Spider):
    name = 't66y_image'
    # allowed_domains = ['t66y.com']
    # start_urls = ['http://t66y.com/']

    def start_requests(self):
        data = {'fid':self.settings.get('INFO_PAGE')}
        base_url = self.settings.get('URL_PAGE')
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['page'] = page
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)


    def parse(self, response):
        result = response.xpath('//h3')
        for i in result:
            image = i.xpath('./a/@href').extract_first()
            split_url = image.split('/')
            if split_url[0] == 'htm_data':
                if int(split_url[1]) == 1907:
                    page_url = "http://t66y.com/" + image
                    yield Request(url=page_url, callback=self.image_down)


    

    def image_down(self, response):
        # result = response.xpath('//input/@data-link').extract_first()
        result = response.css('input::attr(data-src)').extract()
        for i in result:
            item = T66YItem()
            item['url'] = i
            yield item

        # result = response.xpath('//input').extract_first()
        # print(result)
        # images = result.xpath('input/@src').extract_first()
        # print()

        # content = response.body
        # soup = BeautifulSoup(content, "html.parser")
        # a_list = soup.find_all('a', attrs={'href': True, 'id': True})
        # for item in a_list:
        #     temp_result = item['href'].split('/')
        #     if len(temp_result) == 4:
        #         if int(temp_result[2]) > 1800:
        #             print(item['href'])
