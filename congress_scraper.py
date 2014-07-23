from bs4 import BeautifulSoup
import urllib2
import re
import socket
import time
import lxml.html
import itertools

class CongressPerson(object):
	def __init__(self, name):
		self.name = name
class Bill(object):
	def __init__(self, sponsor, congress_num, cosponsors='', title='', summary=''):
		self.sponsors = sponsors
		self.title = title

# mapping of bills to senators that own them 
bill_dict = {}

timeout = 10
socket.setdefaulttimeout(timeout) #don't want shit lasting longer than 30 secs

base_url = "http://thomas.loc.gov/home/Browse.php?n=bills&c="
#currently on the 113th congress, so last param should be 114
congress_range = range(101, 102) 
urllist = [str(base_url + str(congress_num)) for congress_num in congress_range]
print urllist
for i in range(len(urllist)):
	request = urllib2.Request(urllist[i])
	response = urllib2.urlopen(request)
	directory_page = response.read()
	senate_regex = '\/cgi-bin\/query\/L\?c' + str(congress_range[i]) + '\:\.\/list\/c' + str(congress_range[i]) + 's.lst:\d*'
	house_regex = '\/cgi-bin\/query\/L\?c' + str(congress_range[i]) + '\:\.\/list\/c' + str(congress_range[i]) + 'h.lst:\d*'
	senate_groups = re.findall(senate_regex, directory_page)
	house_groups = re.findall(house_regex, directory_page)
	base_next_level_url = "http://thomas.loc.gov"
	senate_bill_table_urls = [base_next_level_url + a for a in senate_groups]
	house_bill_table_urls = [base_next_level_url + a for a in house_groups]
	for senate_url in senate_bill_table_urls:
		print "*** ABOUT TO VISIT: " + senate_url + " ***\n"
		request = urllib2.Request(senate_url)
		response = urllib2.urlopen(request)
		senate_numbered_page = response.read()
		final_regex_s_nums = '\/cgi-bin\/query\/z\?c' + str(congress_range[i]) + ':S\.(\d*)\.\S*:'
		senate_bill_nums = re.findall(final_regex_s_nums, senate_numbered_page)
		senate_bill_nums = ["%05.0f" % int(senate_num) for senate_num in senate_bill_nums]
		senate_final_urls = []
		for number in senate_bill_nums:
			senate_final_urls.append('http://thomas.loc.gov/cgi-bin/bdquery/z?d' + str(congress_range[i]) + ':SN'+ str(number) +':@@@L&summ2=m&')
		for url_ind in range(len(senate_final_urls)):
			request = urllib2.Request(senate_final_urls[url_ind])
			response = urllib2.urlopen(request)
			bill_page = response.read()
			bill_soup = BeautifulSoup(bill_page)
			for aref in bill_soup.find_all('a'):
				match = re.search("FLD003",str(aref))
				if match:
					print "Bill number ", senate_bill_nums[url_ind],"sponsored by: ", aref.string
	
	#for house_url in house_bill_table_urls:
	#	print "*** ABOUT TO VISIT: " + house_url + " ***"



