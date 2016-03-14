#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import time

import ssl
import requests
from lxml import html


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class Ssl3HttpAdapter(HTTPAdapter):
	""""Transport adapter" that allows us to use SSLv3."""

	def init_poolmanager(self, connections, maxsize, block=False):
		self.poolmanager = PoolManager(
			num_pools=connections, maxsize=maxsize,
			block=block, ssl_version=ssl.PROTOCOL_SSLv2)

#page = requests.get("http://econpy.pythonanywhere.com/ex/001.html")
#tree = html.fromstring(page.content)
#
##This will create a list of buyers:
#buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#
##This will create a list of prices
#prices = tree.xpath('//span[@class="item-price"]/text()')
#
#
#print 'Buyers: ', buyers
#print 'Prices: ', prices



#search_map = {
#			"家装建材":["http://search.jd.com/Search?keyword=%E5%AE%B6%E8%A3%85%E5%BB%BA%E6%9D%90&enc=utf-8&suggest=1.def.0&wq=%E5%AE%B6%E8%A3%85&pvid=1efxolli.b4phmb#keyword=%E5%AE%B6%E8%A3%85%E5%BB%BA%E6%9D%90&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&sttr=1&offset=6&page=2&click=0","32,410"],
#
#			"厨房电器":["http://search.jd.com/Search?keyword=%E5%8E%A8%E6%88%BF%E7%94%B5%E5%99%A8&enc=utf-8&wq=%E5%8E%A8%E6%88%BFdian%27qi&pvid=3llxzlli.b4phmb#keyword=%E5%8E%A8%E6%88%BF%E7%94%B5%E5%99%A8&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=2&page=10&click=0","126,2405"],
#			
#			"汽车用品":["http://search.jd.com/Search?keyword=%E6%B1%BD%E8%BD%A6%E7%94%A8%E5%93%81&enc=utf-8&wq=%E6%B1%BD%E8%BD%A6%E7%94%A8%E5%93%81&pvid=8ze00mli.b4phmb#keyword=%E6%B1%BD%E8%BD%A6%E7%94%A8%E5%93%81&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=3&page=2&click=0","98,2234"],
#
#			"手机配件":["http://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&enc=utf-8&wq=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&pvid=ni730mli.b4phmb#keyword=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=6&page=2&click=0","46,580"],
#
#			"电脑配件":["http://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91%E9%85%8D%E4%BB%B6&enc=utf-8&wq=%E7%94%B5%E8%84%91pei&pvid=s5240mli.b4phmb#keyword=%E7%94%B5%E8%84%91%E9%85%8D%E4%BB%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=4&click=0","128,2448"],
#
#			"相机及配件":["http://search.jd.com/Search?keyword=%E7%9B%B8%E6%9C%BA%E5%8F%8A%E9%85%8D%E4%BB%B6&enc=utf-8&wq=%E7%9B%B8%E6%9C%BA%E5%8F%8A%E9%85%8D%E4%BB%B6&pvid=ghn50mli.b4phmb#keyword=%E7%9B%B8%E6%9C%BA%E5%8F%8A%E9%85%8D%E4%BB%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=8&click=0","43,549"],
#
#			#"电脑平板":"http://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91%E5%B9%B3%E6%9D%BF&enc=utf-8&wq=%E7%94%B5%E8%84%91p%27b&pvid=g3lwylli.b4phmb#keyword=%E7%94%B5%E8%84%91%E5%B9%B3%E6%9D%BF&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=7&page=2&click=0",
#		}

search_map = {
		"家装建材":["http://s.taobao.com/search?q=%E5%AE%B6%E8%A3%85%E5%BB%BA%E6%9D%90&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.7724922.8452-taobao-item.1&ie=utf8&initiative_id=tbindexz_20160311&bcoffset=2&ntoffset=2&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","32,140"],

		"厨房电器":["http://s.taobao.com/search?q=%E5%8E%A8%E6%88%BF%E7%94%B5%E5%99%A8&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=2&ntoffset=2&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","126,2405"],
		
		"汽车用品":["http://s.taobao.com/search?q=%E6%B1%BD%E8%BD%A6%E7%94%A8%E5%93%81&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=0&ntoffset=0&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","98,2234"],

		"手机配件":["http://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=0&ntoffset=0&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","46,580"],

		"电脑配件":["http://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=0&ntoffset=0&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","128,2448"],

		"相机及配件":["http://s.taobao.com/search?q=%E7%9B%B8%E6%9C%BA%E5%8F%8A%E9%85%8D%E4%BB%B6&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=1&ntoffset=1&p4plefttype=2%2C1&p4pleftnum=3%2C3&s=44","43,549"],

		}

for search_word,url in search_map.items():
	for i in range(0,1):
		tmp_url = re.sub(r"s=(\d+)","s=%d" % i * 44,url[0])
		#tmp_url = re.sub(r"page=(\d+)","page=%d" % i,url[0])
		time.sleep(1)

		s = requests.Session()
		s.mount('http://s.taobao.com',Ssl3HttpAdapter())
#		result = requests.get(tmp_url,verify=False)
	#	result = requests.get("http://www.baidu.com")
		result = s.get(tmp_url,verify=False)

		if result.status_code == 200:
			tree = html.fromstring(result.content)
			print tree.text

#			for x in tree.xpath('//li[@class="gl-item"]/div/div/a/@title'):
#				if x.encode("utf8") == "点击关注":
#					continue
#				print ",".join([url[1],search_word.decode("utf8"),"jd,1",x,str(i)])

