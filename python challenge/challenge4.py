import urllib2

number = 63579

while 1:
	req = urllib2.Request('http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='+str(number))
	res = urllib2.urlopen(req)
	reads = res.read()
	print reads
	if reads.find('is') == -1:
		break
	number = int(reads[reads.find('is')+3:])