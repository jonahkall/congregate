def proper_name(senator):
	senator = senator.split(",")
	first_name = senator[1][1:]
	last_name = senator[0][3:]
	return first_name+last_name


assert(proper_name("Sen Humphrey, Gordon J.") == "Gordon J. Humphrey")
assert(proper_name("Sen Roth Jr., William V.") == "William V. Roth Jr.")