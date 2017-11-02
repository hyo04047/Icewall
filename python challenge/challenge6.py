import os, sys, re
import zipfile

next_number = "90052"
comment = ""

zipf = zipfile.ZipFile("channel.zip","r")

while 1:
	data = zipf.read(next_number+".txt")
	find = re.findall(r"[0-9]+",data)

	if not find:
		print data
		break;
	else:
		print data
		comment += zipf.getinfo(next_number+".txt").comment
		next_number = find[0]

print comment