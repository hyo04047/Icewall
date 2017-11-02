from PIL import Image

img = Image.open("quest3.png")
result = []

for x in range(img.width):
	for y in range(img.height):
		(r,g,b) = img.getpixel((x,y))
		if (r%2==1 and g%2==0 and b%2==0):
			result.append((x,y))

for (x,y) in result:
	img.putpixel((x,y), (255, 255, 255, 0))

img.save("result.png")
img.close()
