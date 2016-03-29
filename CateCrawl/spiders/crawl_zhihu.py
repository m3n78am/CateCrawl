#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import requests
import time
from lxml import html

topic_set = set()
people_set = set()
people_queue = list()

def get_zhihuid_from_url(url):
	return url.split("/")[4]

# try to login in
session_requests = requests.session()
login_url = "https://www.zhihu.com/#signin"
result = session_requests.get(login_url,verify=False)
tree = html.fromstring(result.text)

authenticity_token = list(set(tree.xpath("//input[@name='_xsrf']/@value")))[0]
params = {'email':'wtf@gmail.com','password':'xxxxxxx','_xsrf':authenticity_token}

result = session_requests.post("https://www.zhihu.com/login/email",data=params)
session_requests.headers.update({"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"})

#people_queue.append("xubinlvshi")
people_queue.append("Charming_Who")

while len(people_queue) > 0:
	current_person = people_queue.pop(0)

	# already walked,continue
	if current_person in people_set:
		continue

	try:
		# walk the follwees url
		result = session_requests.get("https://www.zhihu.com/people/%s/followees" % current_person)
		tree = html.fromstring(result.content)

		# extract profile
		zhihuid = current_person
		nickname = tree.xpath("//span[@class='bio']/../a/text()")[0] 
		motto = tree.xpath("//span[@class='bio']/@title")[0]

		#intro = tree.xpath("//span[@class='content']/text()")[0].strip("\n")
		intro_list = tree.xpath("//span[@class='fold-item']/span[@class='content']/descendant-or-self::text()")
		#intro_list = tree.xpath("//span[@class='fold-item']/span[@class='content']/child::text()")
		intro = "".join([x.replace("\n"," ") for x in intro_list])

		print "\t".join(["1",current_person,nickname,motto,intro])

		# extract followees
		followees_url_list = tree.xpath("//h2[@class='zm-list-content-title']/a/@href")
		followees_list = [get_zhihuid_from_url(x) for x in followees_url_list]

		print "\t".join(["2",current_person,",".join(followees_list)])

		for x in followees_list:
			people_queue.append(x)
		
		time.sleep(1)
		# walk the topics url
		result = session_requests.get("https://www.zhihu.com/people/%s/topics" % current_person)
		tree = html.fromstring(result.content)
		topics_list = tree.xpath("//div[@class='zm-profile-section-main']/a[@data-tip]/strong/text()")

		print "\t".join(["3",current_person,",".join(topics_list)])
		people_set.add(current_person)

	except KeyboardInterrupt:
		os.exit(-1)
	except:
		pass
