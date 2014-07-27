from bs4 import BeautifulSoup
import urllib2

class CongressPersonInfo(object):
	def __init__(self, party, state, served_string, img_url, bills=[]):
		self.party = party
		self. state = state
		self.served_string = served_string
		self.img_url = img_url
	def addBill(self, bill):
		self.bills.append(bill)

# Use urllib2 to get the HTML text of the page specified 
# by "url".
def url_to_page_contents(url):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	page = response.read()
	return page

def url_to_soup(url):
	return BeautifulSoup(url_to_page_contents(url))

# Not actually used yet at least, used congress.gov instead
def get_wiki_name(name):
	excluded = ["I","II", "III", "IV", "V", "VI", "VII", "Jr.", "Sr."]
	name = name.split(" ")
	first_name = name[0]
	if name[-1] in excluded:
		last_name = name[-2]
	else:
		last_name = name[-1]
	return first_name + '_' + last_name

def url_to_page_contents(url):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	page = response.read()
	return page

def produce_congress_dict(base_url):
	congress_pages = [url_to_page_contents(i) for i in [base_url + str(j) for j in range(1,6)]]
	print i
	# Dictionary of name of congressperson to CongressPersonInfo object
	congress_dict = {}
	for index in range(0,1):
		soup = BeautifulSoup(congress_pages[index], "html.parser")
		for i in soup.findAll("li"):
			try:
				name = ""
				names = i.findAll("h2")
				for j in names:
					name += str(j.string)
				imgdiv = i.find("div",{"class":"memberImage"})
				img = imgdiv.find("img")
				img_src = img['src']
				img_url = 'https://beta.congress.gov/' + img_src
				print img_url
				#print "Name is: ", name
				for k in i.findAll("tr"):
					if k.find("th").string == "Party:":
						party = k.find("td").string
					if k.find("th").string == "State:":
						state = k.find("td").string
					if k.find("th").string == "Served:":
						served_string = ""
						for list_elem in k.findAll("li"):
							served_string = served_string + list_elem.string + "\n"
				tmp_congress_person = CongressPersonInfo(party, state, served_string, img_url)
				congress_dict[name] = tmp_congress_person
			except:
				# if an exception was thrown, ignore it (there will be lots of these)
				# from the wrong li objects...i know this is kind of bad
				pass
	return congress_dict

