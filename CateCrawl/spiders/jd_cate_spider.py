#!/usr/bin/env python

import scrapy
import re
import sys

#from CateCrawl.items import JdProductItem

#sys.stdout=open('output_final.txt','w')


jd_product_url_pattern = re.compile(r'https?://item.jd.com/(\d+).html')

class JdProductSpider(scrapy.Spider):
	name = "jd_product"
	allowed_domains = ["jd.com"]
	start_urls = ["http://search.jd.com/Search?keyword=%E6%88%B7%E5%A4%96%E8%A3%85%E5%A4%87&enc=utf-8&suggest=2.def.0&wq=%E6%88%B7%E5%A4%96&pvid=mxkcnkli.d1rhkk",
			"http://search.jd.com/Search?keyword=%E5%AD%95%E5%A6%88&enc=utf-8&wq=yun%27ma&pvid=ssrcnkli.d1rhkk",
			"http://search.jd.com/Search?keyword=%E5%AE%B6%E8%A3%85%E5%BB%BA%E6%9D%90&enc=utf-8&pvid=by9fnkli.d1rhkk"
			]

	def parse(self,response):
		for href in response.xpath('//a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url,callback=self.parse_title)
	
	def parse_title(self,response):
		# jd product url
		if jd_product_url_pattern.match(response.url):
			#item = JdProductItem()
			# extract and store
			title = response.xpath("//div[@id='itemInfo']/div[@id='name']/h1/text()").extract()[0]
			root_cate = response.xpath("//div[@class='breadcrumb']/strong/a/text()").extract()[0]
			span_cate_list = [x.extract() for x in response.xpath("//div[@class='breadcrumb']/span/a/text()")]
			span_cate = ",".join([root_cate] + span_cate_list)

			#item["title"] = title.encode("utf8")
			#item["category"] = span_cate.encode("utf8")
			print title.encode("utf8") + "\t" + span_cate.encode("utf8")

			# new Request
			for href in response.xpath('//a/@href'):
				url = response.urljoin(href.extract())
				yield scrapy.Request(url,callback=self.parse_title)
