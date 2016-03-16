#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import traceback
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html


# waitForLoad
def waitForLoad(driver):
	elem = driver.find_element_by_tag_name("html")
	count = 0
	while True:
		count += 1
		if count > 20:
			print "Timing out after 10 seconds and returning"
			return
		time.sleep(.5)
		try:
			elem == driver.find_element_by_tag_name("html")
		except StaleElementReferenceException:
			return


search_map = {
		#"家装建材":["http://s.taobao.com/search?q=%E5%AE%B6%E8%A3%85%E5%BB%BA%E6%9D%90&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.7724922.8452-taobao-item.1&ie=utf8&initiative_id=tbindexz_20160311&bcoffset=2&ntoffset=2&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","32,140"],

		#"厨房电器":["http://s.taobao.com/search?q=%E5%8E%A8%E6%88%BF%E7%94%B5%E5%99%A8&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=2&ntoffset=2&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","126,2405"],
		
		#"汽车用品":["http://s.taobao.com/search?q=%E6%B1%BD%E8%BD%A6%E7%94%A8%E5%93%81&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=0&ntoffset=0&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","98,2234"],

		#"手机配件":["http://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=0&ntoffset=0&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","46,580"],

		#"电脑配件":["http://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=0&ntoffset=0&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44","128,2448"],

		"相机及配件":["http://s.taobao.com/search?q=%E7%9B%B8%E6%9C%BA%E5%8F%8A%E9%85%8D%E4%BB%B6&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160311&ie=utf8&bcoffset=1&ntoffset=1&p4plefttype=2%2C1&p4pleftnum=3%2C3&s=44","43,549"],
		}

setting = {'phantomjs.page.settings.resourceTimeout':5000,'phantomjs.page.settings.loadImages':False,'phantomjs.page.settings.userAgent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5','phantomjs.page.settings.resourceTimeout':5000}
phantomjs_driver = "/Users/Charming_Who/Desktop/Software/phantomjs-2.1.1-macosx/bin/phantomjs"

# new a driver instance
driver = webdriver.PhantomJS(executable_path=phantomjs_driver,service_log_path='./ghostdriver.log',service_args=["--webdriver-loglevel=DEBUG"],desired_capabilities=setting)


for search_word,url in search_map.items():

	print "#### start to crawling %s" % search_word
	# try to get the range num
	try:
		driver.get(url[0])
		time.sleep(5)
		tree = html.fromstring(driver.page_source)
		range_num = tree.xpath('//li/span[@class="current"]/..')[0].text_content().split("/")[1]
		#range_num = "4"
	except:
		print traceback.print_exc()
		continue

	for i in range(0,int(range_num)):
		tmp_url = re.sub(r"&s=(\d+)","&s=%d" % (i * 44),url[0])
		driver.get(tmp_url)

		time.sleep(5)

		try:
			element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,"mainsrp-itemlist")))
		except:
			print traceback.print_exc()
			continue

		tree = html.fromstring(driver.page_source)

		#for x in tree.xpath('//a[starts-with(@id,"J_Itemlist_TLink_")]'):
		#for x in tree.xpath('//a[matches(@id,"J_Itemlist_TLink_\d+")]'):
		#for x in tree.xpath('//*[contains(@id,"J_Itemlist_TLink_")]'):
		for x in tree.xpath('//a[starts-with(@id,"J_Itemlist_TLink_")]'):
			print ",".join([url[1],search_word.decode("utf8"),"jd,1",x.text_content().replace("\n","").strip(),str(i)])

driver.close()
