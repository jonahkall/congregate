from bs4 import BeautifulSoup
import urllib2
import re
#import sys
#import collections
import socket
import time
import lxml.html
import itertools

timeout = 10
socket.setdefaulttimeout(timeout) #don't want shit lasting longer than 30 secs

base_url = "http://thomas.loc.gov/home/Browse.php?n=bills&c="
#currently on the 113th congress, so last param should be 114
congress_range = range(101, 114) 
urllist = [str(base_url + str(congress_num)) for congress_num in congress_range]
print urllist
for i in range(len(urllist)):
	req = urllib2.Request(urllist[i])
	response = urllib2.urlopen(req)
	directory_page = response.read()
	senate_regex = '\/cgi-bin\/query\/L\?c' + str(congress_range[i]) + '\:\.\/list\/c' + str(congress_range[i]) + 's.lst:\d*'
	house_regex = '\/cgi-bin\/query\/L\?c' + str(congress_range[i]) + '\:\.\/list\/c' + str(congress_range[i]) + 'h.lst:\d*'
	senate_groups = re.findall(senate_regex, directory_page)
	house_groups = re.findall(house_regex, directory_page)
	base_next_level_url = "thomas.loc.gov"
	senate_bill_table_urls = [base_next_level_url + a for a in senate_groups]
	house_bill_table_urls = [base_next_level_url + a for a in house_groups]
	for senate_url in senate_bill_table_urls:
		print "*** ABOUT TO VISIT: " + senate_url + " ***"
		senate_soup = BeautifulSoup(senate_url)
		print senate_soup.prettify()
	for house_url in house_bill_table_urls:
		print "*** ABOUT TO VISIT: " + house_url + " ***"
		house_soup = BeautifulSoup(house_url)
