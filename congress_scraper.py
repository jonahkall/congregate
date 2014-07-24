from bs4 import BeautifulSoup
import urllib2
import re
import socket
import time
import lxml.html
import itertools
import cp_namer


class CongressPerson(object):
	def __init__(self, name, bills=[]):
		self.name = name
	def addBill(self, bill):
		self.bills.append(bill)

class Bill(object):
	def __init__(self, sponsor, congress_num, date, cosponsors=[], title='', summary=''):
		self.sponsor = sponsor
		self.congress_num = congress_num
		self.date = date
		self.cosponsors = cosponsors
		self.title = title
		self.summary = summary
	def addCosponsor(self, cosponsor):
		self.cosponsors.append(cosponsor)

# Use urllib2 to get the HTML text of the page specified 
# by "url".
def url_to_page_contents(url):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	page = response.read()
	return page

# Mapping of bills to senators that own them 
bill_dict = {}
bill_list = []
congress_people = set([])

timeout = 30
socket.setdefaulttimeout(timeout) # don't want shit lasting longer than 30 secs
printing = True # Make false if you want to suppress output.

base_url = "http://thomas.loc.gov/home/Browse.php?n=bills&c="
# currently on the 113th congress, so last param should be 114
congress_range = range(101, 102) 
urllist = [str(base_url + str(congress_num)) for congress_num in congress_range]
for i in range(len(urllist)):
	directory_page = url_to_page_contents(urllist[i])
	senate_regex = '\/cgi-bin\/query\/L\?c' + str(congress_range[i]) + '\:\.\/list\/c' + str(congress_range[i]) + 's.lst:\d*'
	house_regex = '\/cgi-bin\/query\/L\?c' + str(congress_range[i]) + '\:\.\/list\/c' + str(congress_range[i]) + 'h.lst:\d*'
	senate_groups = re.findall(senate_regex, directory_page)
	house_groups = re.findall(house_regex, directory_page)
	base_next_level_url = "http://thomas.loc.gov"
	senate_bill_table_urls = [base_next_level_url + a for a in senate_groups]
	house_bill_table_urls = [base_next_level_url + a for a in house_groups]
	for senate_url in senate_bill_table_urls[0:1]:
		if printing: print "*** ABOUT TO VISIT: " + senate_url + " ***\n"
		# Visit the page of bills 101-200 for example
		senate_numbered_page = url_to_page_contents(senate_url)
		final_regex_s_nums = '\/cgi-bin\/query\/z\?c' + str(congress_range[i]) + ':S\.(\d*)\.\S*:'
		senate_bill_nums = re.findall(final_regex_s_nums, senate_numbered_page)
		senate_bill_nums = ["%05.0f" % int(senate_num) for senate_num in senate_bill_nums]
		senate_final_urls = []
		for number in senate_bill_nums:
			senate_final_urls.append('http://thomas.loc.gov/cgi-bin/bdquery/z?d' + str(congress_range[i]) + ':SN'+ str(number) +':@@@L&summ2=m&')
		for url_ind in range(len(senate_final_urls[0:14])):
			if printing: print "Bill url is: ", senate_final_urls[url_ind]
			# Explore the all information individual bill page
			bill_page = url_to_page_contents(senate_final_urls[url_ind])
			bill_soup = BeautifulSoup(bill_page)
			title = bill_soup.findAll(attrs={"name":"dc.title"})[0]
			title = str(title).split("\"")[1]
			summary = bill_soup.findAll(attrs={"name":"dc.description"})[0]
			summary = str(summary).split("\"")[1]
			date = bill_soup.findAll(attrs={"name":"dc.date"})[0]
			date = str(date).split("\"")[1]
			if printing: print "Bill title is: ", title
			if printing: print "Bill date is: ", date
			if printing: print "Bill summary is:", summary
			sponsor_index = 0
			cosponsor_index = 0
			for aref in bill_soup.find_all('a'):
				match_spons = re.search("FLD003",str(aref))
				match_cospons = re.search("FLD004",str(aref))
				if match_spons and sponsor_index == 0:
					if printing: print "Bill number ", senate_bill_nums[url_ind],"sponsored by: ", aref.string
					sponsor_index += 1
					# now that we have a sponsor, we can use the Bill defualt constructor
					new_bill = Bill(str(aref.string), congress_range[i], date, [], title, summary)
					bill_list.append(new_bill)
				if match_cospons:
					if printing: print "Bill number ", senate_bill_nums[url_ind],"cosponsored by: ", aref.string
					cosponsor_index += 1
					new_bill.addCosponsor(str(aref.string))
	
	for house_url in house_bill_table_urls:
		if printing: print "*** ABOUT TO VISIT: " + house_url + " ***"
