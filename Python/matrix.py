from time import sleep
import sys
testMatrix=[
	[1,1,1,1],
	[1,1,1,1],
	[1,1,1,1],
	[1,1,1,1]
]

scrollAlphabet={
	'E':[
		[0,0,0,0,0,0],
		[1,1,1,1,1,1],
		[1,0,0,0,0,0],
		[1,1,1,1,0,0],
		[1,0,0,0,0,0],
		[1,0,0,0,0,0],
		[1,1,1,1,1,1],
		[0,0,0,0,0,0]
		],
	'H':[
		[0,0,0,0,0,0],
		[1,0,0,0,0,1],
		[1,0,0,0,0,1],
		[1,1,1,1,1,1],
		[1,0,0,0,0,1],
		[1,0,0,0,0,1],
		[1,0,0,0,0,1],
		[0,0,0,0,0,0]
		],
	'L':[
		[0,0,0,0,0,0],
		[1,0,0,0,0,0],
		[1,0,0,0,0,0],
		[1,0,0,0,0,0],
		[1,0,0,0,0,0],
		[1,0,0,0,0,0],
		[1,1,1,1,1,1],
		[0,0,0,0,0,0]
		],
	'O':[
		[0,0,0,0,0,0],
		[1,1,1,1,1,1],
		[1,0,0,0,0,1],
		[1,0,0,0,0,1],
		[1,0,0,0,0,1],
		[1,0,0,0,0,1],
		[1,1,1,1,1,1],
		[0,0,0,0,0,0]
		],
	' ':[
		[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0],
		[0,0,0,0,0]
		],
}

EMPTYTRIPLE=(0,0,0)
WHITE=(255,255,255)
def monochrome(inMatrix):
	matrix=[]
	for row in inMatrix:
		matrix.append([])
		for cell in row:
			if cell==1:
				matrix[-1].append(WHITE)
			else:
				matrix[-1].append(EMPTYTRIPLE)
	return matrix

class pixelmatrix:
	matrix=[]
	ylen=0
	xlen=0
	def __init__(self, dims=(8,8)):
		y=dims[0]
		x=dims[1]
		self.ylen=y
		self.xlen=x
		for i in range (y):
			row=[EMPTYTRIPLE for k in range (x)]
			self.matrix.append(row)
	def __getitem__(self, key):
		return self.matrix[key]
	def show(self):
		for row in self.matrix:
			print('[', end='')
			for cell in row:
				if cell == EMPTYTRIPLE:
					print(' ', end ='')
				else:
					print('X', end ='')
			print(']\n', end='')
		print('\n')
		sleep(0.1)

	def update(self, inMatrix, coords=(0,0)):
		y,x=coords
		ylen=len(inMatrix)
		xlen=len(inMatrix[0])
		for i, row in enumerate(inMatrix):
			for j, cell in enumerate(row):
				self.matrix[y+i][x+j] = cell
	def newRow(self):
		return [EMPTYTRIPLE for k in range (self.xlen)]
	def newCol(self):
		return [EMPTYTRIPLE for k in range (self.ylen)]
	def pushRow(self, row, side='bottom'):
		xin = len(row)
		if side == 'bottom':
			del self.matrix[0]
			self.matrix.append(self.newRow())
			for i in range (xin):
				self.matrix[-1][i]=row[i]
		if side == 'top':
			del self.matrix[-1]
			self.matrix.insert(0, self.newRow())
			for i in range (xin):
				self.matrix[0][i]=row[i]
	def pushCol(self, col, side='right'):
		yin = len(col)
		if side == 'right':
			for row in self.matrix:
				row.pop(0)
			for i in range (yin):
				self.matrix[i].append(col[i])
			for j in range (i+1, self.ylen):
				self.matrix[j].append(EMPTYTRIPLE)
		if side == 'left':
			for row in self.matrix:
				row.pop()
			for i in range (yin):
				self.matrix[i].insert(0, col[i])
			for j in range (i+1, self.ylen):
				self.matrix[j].insert(0, EMPTYTRIPLE)
	def scroll(self, inMatrix):
		width=len(inMatrix[0])
		for i in range (width):
			col=[]
			for row in inMatrix:
				col.append(row[i])
			self.pushCol(col)
			self.show()
	def scrollText(self, str):
		for char in str:
			chargrid=monochrome(scrollAlphabet[char])
			self.scroll(chargrid)
			self.pushCol(self.newCol())
			self.show()
		for i in range (self.xlen):
			self.pushCol(self.newCol())
			self.show()


testStr='OO'

#scrollMatrix(testStr)

#updateMatrix(testMatrix, (4,4))
#showMatrix()

screen = pixelmatrix(dims=(8,16))
screen.show()
screen.scrollText(sys.argv[1])
screen.update(monochrome(testMatrix), (4,4))
screen.show()