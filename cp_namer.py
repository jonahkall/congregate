# Module for extracting proper names of congresspersons

def proper_name(congressperson):
	congressperson = congressperson.split(",")
	first_name = congressperson[1][1:]
	last_name = congressperson[0][3:]
	return first_name+last_name

assert(proper_name("Sen Humphrey, Gordon J.") == "Gordon J. Humphrey")
assert(proper_name("Sen Roth Jr., William V.") == "William V. Roth Jr.")