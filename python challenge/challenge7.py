import Image

img = Image.open("oxygen.png")
string = ""
imgx = img.size[0]

for x in range(0,imgx):
	rgb_im = img.convert('RGB')
	r,g,b = rgb_im.getpixel((x,45))
	if r==g==b:
		print r,g,b