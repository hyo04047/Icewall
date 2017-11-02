import pickle

file = open('banner.p','rb')
data = pickle.load(file)
file.close()
print data

for i in data:
	line = ""
	for x,y in i:
		line += x*y
	print line