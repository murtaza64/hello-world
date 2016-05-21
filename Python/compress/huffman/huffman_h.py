class node: #huffman tree will be built out of nodes
	str='<branch>' #will be replaced with character if node is endpoint
	freq=0
	branch=0
	encoding=0
	def __init__(self, charkeyval): #initialize node with charkeyval which is a tuple: ('key', val)
		self.str=charkeyval[0]
		self.freq=charkeyval[1]

	def next(self, x, y): #set the next two nodes when building the tree
		self.nextl=x
		self.nextr=y

	def trace(self, n=0): #traverse the tree and print out each branch
		print(">"*n, end='')
		print(self.freq, self.str, sep = ':')
		if hasattr(self, 'nextl') and hasattr(self, 'nextr'):
			self.nextl.trace(n+1)
			self.nextr.trace(n+1)

	def encode(self, enc=''): #set the encoding for each node, branching 1 for right and 0 for left
		self.encoding=enc
		if hasattr(self, 'nextl'):
			self.nextl.encode(enc+'0')
		if hasattr(self, 'nextr'):
			self.nextr.encode(enc+'1')

	def getenc(self): #recursively create a list of encoded characters
		e=[]
		if(self.str!='<branch>'):
			e.append((self.str, self.encoding))
		if hasattr(self, 'nextl'):
			l=self.nextl.getenc()
			for pair in l:
				e.append(pair)
		if hasattr(self, 'nextr'):
			r=self.nextr.getenc()
			for pair in r:
				e.append(pair)
		return e

	def output(self): #print a visual table of characters with encodings and return a dict
		enc=sorted(self.getenc(), key=lambda x: len(x[1]))
		encdict={}
		for pair in enc:
			print('\''+pair[0]+'\': '+pair[1], sep=None)
			encdict[pair[0]]=pair[1]
		return encdict
		
def huff_enc:
	#get frequency of each character
	f = open('huff_in.txt', 'r')
	c=f.read(1)
	freq={}
	while c:
		if c in freq:
			freq[c]+=1
		else:
			freq[c]=1
		c=f.read(1)

	#create node for each character
	nodes=[]
	for char in freq:
		charkeyval=(char, freq[char])
		nodes.append(node(charkeyval))
		print(nodes[-1].str, nodes[-1].freq)

	#build the tree
	while len(nodes)>1:
		nodes=sorted(nodes, key=lambda n: n.freq, reverse=True)
		a=nodes.pop()
		b=nodes.pop()
		n=node(('<branch>',a.freq+b.freq))
		n.next(a,b)
		nodes.append(n)

	#get the encoding of each char
	n.trace()
	root=nodes[0]
	root.encode()
	enc=root.output()

	#build a string of encoded 1s and 0s
	o=''
	charcount=0
	obytes=[]
	f.seek(0,0)
	c=f.read(1)
	while c:
		o+=enc[c]
		c=f.read(1)
		charcount+=1

	#pad the string with 0s to complete the final byte
	if len(o) % 8 != 0:
		o += '0' * (8 - (len(o) % 8))


	#convert each 8 characters in the string to a byte
	for b in range (0, len(o), 8):
		byte=o[b:b+8]
		obytes.append(int(byte, 2))

	outf=open('huff_out.hex', 'wb')

	#write length of encoding information and char count to first two bytes of outfile
	length=(len(enc)*4).to_bytes(2,'big')
	outf.write(length)
	outf.write(charcount.to_bytes(4,'big'))

	#write encoding info to file
	for char in enc:
		outf.write(ord(char).to_bytes(1,'big'))
		ec='1'+enc[char]
		outf.write(int(ec,2).to_bytes(3,'big'))

	#write encoded text data to file
	outf.write(bytes(obytes))
	outf.close
	f.close

	print("written to huff_out.hex")


