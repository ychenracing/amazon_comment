# -*- coding: utf-8 -*-
import scrapy
import re
import time

from scrapy.spiders import CrawlSpider

from amazon_comment.items import AmazonCommentItem
from amazon_comment.items import AmazonProductItem


class AmazonCommentSpider(CrawlSpider):
    """爬取亚马逊商品评论"""
    name = 'amazon_comment'  # Spider名，必须唯一，执行爬虫命令时使用

    headers = {
        "Host": "www.amazon.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=LED+light",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }

    allowed_domains = ['www.amazon.com']  # 限定允许爬的域名，可设置多个

    DOMAIN_PREFIX = "https://www.amazon.com"

    start_urls = [
        "https://www.amazon.com/led-light/s?ie=UTF8&page=1&rh=i%3Aaps%2Ck%3Aled%20light"
    ]


    def parse_start_url(self, response):
        """获取LED light搜索页，抓取LED light列表，获取LED light项的详情页地址"""
        for item_div in response.xpath('//li[contains(@id, "result_") and @data-asin and @class]'):
            urls = item_div.xpath('//div[@class="a-fixed-left-grid"]/div/div[2]/div[2]/div[1]/a/@href').extract()
            for url in urls:
                time.sleep(5)
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_detail_url)


    def parse_detail_url(self, response):
        """获取LED light项的详情页，抓取评论页地址"""
        urls = response.xpath('//*[@id="reviews-medley-footer"]/div[1]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(self.DOMAIN_PREFIX + url, headers=self.headers, callback=self.parse_item)


    def parse_item(self, response):
        """获取评论页，抓取评论项和评论页下一页地址"""

        product_div = response.xpath('//*[@id="cm_cr-product_info"]/div/div[2]')
        print "\n\n\n", product_div.extract(), "\n\n\n"
        product = AmazonProductItem()
        link = product_div.xpath('/div/div/div[1]/a/@href').extract()
        if not link:
            return
        product['detail_url'] = self.DOMAIN_PREFIX + link
        product['img_url'] = product_div.xpath('/div/div/div[1]/a/img/@src').extract_first()
        product['title'] = product_div.xpath('/div/div/div[2]/div[1]/h1/a/text()').extract_first()
        dp_index = str(link).find('dp')
        if dp_index != -1:
            product_id_match = re.compile(r'dp/(.*?)/').match(link[dp_index:])
            if product_id_match:
                product['amazon_product_id'] = product_id_match.group(1)
        yield product

        comments = response.xpath('//*[@id="cm_cr-review_list"]//div[@data-hook and @class]')

        for comment in comments:
            comment_div = comment.xpath('//div[contains(@id, "customer_review) and @class="a-section celwidget"]')
            item = AmazonCommentItem()
            item['score'] = comment_div.xpath('/div[1]/a[1]/i/span/text()').extract()
            item['title'] = comment_div.xpath('/div[1]/a[2]/text()').extract()
            user_link = self.DOMAIN_PREFIX + comment_div.xpath('/div[2]/span[1]/a/@href').extract()
            if "?" in user_link:
                user_link += "&ref_=cm_cr_arp_d_pdp"
            else:
                user_link += "?ref_=cm_cr_arp_d_pdp"
            user_name = comment_div.xpath('/div[2]/span[1]/a/text()').extract()
            item['user'] = '<a href="' + user_link + '">' + user_name + '</a>';
            item['comment'] = comment_div.xpath('//div[@class="a-row review-data"]/span/text()').extract()
            item['date'] = comment_div.xpath('/div[2]/span[4]/text()').extract()
            item['amazon_product_id'] = product['amazon_product_id']
            item['support_peoples'] = comment_div.xpath('/div[7]/div/span[3]/span/span[1]/span/text()').extract()
            yield item

        # 评论页下一页
        next_comment_page_url = response.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[@class="a-last"]/a/@href/text()').extract()

        if next_comment_page_url:
            yield scrapy.Request(self.DOMAIN_PREFIX + next_comment_page_url, headers=self.headers, callback=self.parse_item)
