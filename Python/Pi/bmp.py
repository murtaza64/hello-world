from struct import *
matrix = [
	[(0,255,255), (255,255,255), (255,255,255), (255,255,255)],
	[(255,255,255), (255,255,255), (255,255,255), (255,255,255)],
	[(255,255,255), (255,255,255), (255,255,255), (255,255,255)],
	[(255,255,255), (255,255,255), (255,255,255), (255,255,255)]
]

h=4
w=4
depth = 24
padding = int(4 - (w*(depth/8) %4)) if (w*(depth/8) % 4 != 0) else 0
bytes_per_row = int (w*(depth/8) + padding) 
bytes_in_image = h*bytes_per_row

size = 54 + bytes_in_image
unused = 0
offset = 54
BITMAPFILEHEADER = pack('<hihhi',0x4D42, size, 0, 0, 54)
print(BITMAPFILEHEADER)

numbytes = 40
colorplanes = 1
resolution_vert = 2835
resolution_hor = 2835
BITMAPINFOHEADER = pack('<iiihhiiiiii', 40, w, -h, 1, depth, 0, bytes_in_image, 2835, 2835, 0, 0)
print(BITMAPINFOHEADER)

imagebytes = []

for row in matrix:
	for cell in row:
		red=cell[0].to_bytes(1, byteorder='little')
		green=cell[2].to_bytes(1, byteorder='little')
		blue=cell[1].to_bytes(1, byteorder='little')

		imagebytes.append(blue)
		imagebytes.append(green)
		imagebytes.append(red)
		
	for i in range(0, padding):
		imagebytes.append((0).to_bytes(1, byteorder='little'))

print (imagebytes)

image=open('output.bmp', 'wb')
image.write(BITMAPFILEHEADER)
image.write(BITMAPINFOHEADER)
for byte in imagebytes:
	image.write(byte)