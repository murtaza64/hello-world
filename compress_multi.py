import re
import sys


class node: #huffman tree will be built out of nodes
	str='<branch>' #will be replaced with character if node is endpoint
	freq=0
	branch=0
	encoding=''
	def __init__(self, charkeyval): #initialize node with charkeyval which is a tuple: ('key', val)
		self.str=charkeyval[0]
		self.freq=charkeyval[1]

	def next(self, x, y): #set the next two nodes when building the tree
		self.nextl=x
		self.nextr=y

	def trace(self, n=0): #traverse the tree and print out each branch
		log=''
		a='>'*n
		log+=a
		log+=(self.encoding+': '+self.str+'('+str(self.freq)+')\n')
		if hasattr(self, 'nextl') and hasattr(self, 'nextr'):
			log+=self.nextl.trace(n+1)
			log+=self.nextr.trace(n+1)
		return log

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
			encdict[pair[0]]=pair[1]
		return encdict

def huff_enc(infile, outfile, l):
	log = ''
	#get frequency of each character
	f = open(infile, 'r')
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


	#build the tree
	while len(nodes)>1:
		nodes=sorted(nodes, key=lambda n: n.freq, reverse=True)
		a=nodes.pop()
		b=nodes.pop()
		n=node(('<branch>',a.freq+b.freq))
		n.next(a,b)
		nodes.append(n)

	#get the encoding of each char
	root=nodes[0]
	root.encode()
	enclist=sorted(root.getenc(), key=lambda x: len(x[1]))
	enc={}
	for pair in enclist:
			enc[pair[0]]=pair[1]
	for char in enclist:
		log+=('\''+char[0]+'\' ('+str(freq[char[0]])+'): '+char[1]+'\n')
	log+=n.trace()+'\n'

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

	outf=open(outfile, 'wb')

	#write length of encoding information and char count to first two bytes of outfile
	length=(len(enc)*4).to_bytes(2,'big')
	outf.write(length)
	outf.write(charcount.to_bytes(4,'big'))
	log+='\nencoding length: '+str(len(enc)*4)+'\ncharcount: '+str(charcount)+'\n'

	#write encoding info to file
	for char in enc:
		outf.write(ord(char).to_bytes(1,'big'))
		ec='1'+enc[char]
		outf.write(int(ec,2).to_bytes(3,'big'))
	filesize=2+4+len(enc)*4+len(obytes)
	saved=charcount-filesize
	perc = int((saved/charcount)*100)
	#log data
	
	l.write('@@@huff: compressed to '+outfile+'\nsaved '+str(saved)+' bytes ('+str(perc)+'%)\n')
	print('huff: compressed\nsaved '+str(saved)+' bytes ('+str(perc)+'%)\n')
	l.write(log)
	l.write('\n@@@end huff@@@\n\n')

	#write encoded text data to file
	outf.write(bytes(obytes))
	outf.close
	f.close
	return perc



def huff_dec(infile, outfile):
	f=open(infile, 'rb')

	#read header info
	enclen=int.from_bytes(f.read(2), 'big')
	charcount=int.from_bytes(f.read(4), 'big')

	#construct encoding table
	enc={}
	for c in range(0, enclen, 4):
		ch=chr(int.from_bytes(f.read(1), 'big'))
		bin=int.from_bytes(f.read(3), 'big')
		bstr='{:b}'.format(bin)
		bstr=bstr[1:]
		#print(ch, bstr)
		enc[bstr]=ch
	#print(enc)

	#construct binary string
	ostr=''
	c=f.read(1)
	while c:
		ostr+='{:08b}'.format(int.from_bytes(c, 'big'))
		c=f.read(1)
	offset=0
	runlength=1

	#output decoded text
	o=open(outfile, 'w')
	c=0
	while (offset+runlength)<=len(ostr) and c<charcount:
		selection = ostr[offset:offset+runlength]
		if selection in enc:
			o.write(enc[selection])
			offset+=runlength
			runlength=1
			c+=1
		else:
			runlength+=1
	o.close
	f.close
	


def dict_enc(infile, outfile, l):

	a = open(infile,'r')
	c = open(outfile, 'w')
	log = ''
	a.seek(0,0)
	atext = a.read()
	pat = re.compile(r"([a-z]{3,}|[A-Z][a-z]{2,}|[A-Z]?[a-z]*\'[a-z]+)( |$|\.|\!|\?|\,|\(|\)|\/|\\|\"|\-)")

	#matches = []
	freq = {}
	cdict = {}

	for match in pat.finditer(atext): #created freq dict for words
		#matches.append((i, match.group(1), match.start(), match.end()-match.start()-1))
		if match.group(1) not in freq:
			freq[match.group(1)] = 0
		freq[match.group(1)] += 1

	freqli = [(k,freq[k]) for k in (sorted(freq, key=freq.get, reverse=True))] #creates sorted dict


	chars=['0','1','2','3','4','5','6','7','8','9',
		'a','b','c','d','e','f','g','h','i','j',
		'k','l','m','n','o','p','q','r','s','t',
		'u','v','w','x','y','z','A','B','C','D',
		'E','F','G','H','I','J','K','L','M','N',
		'O','P','Q','R','S','T','U','V','W','X','Y','Z']
	pointers=['@','~','^','|','<','>']
	pointers2=['_','%']

	repl=0
	replp=0
	save1=0
	for word, freq in freqli: #create lookup table for words that appear 4x or more
		#print (word, freq) 
		if ( (2*freq+len(word)+4) < freq * (len(word)) ): #2f+l+4 < fl -- checks if substituting this word will save space
			cdict[word] = (pointers[replp]+chars[repl])
			save1 +=( freq * len(word) - (2*freq + len(word) +4) ) #keeps track of bytes saved
			log += ('phase 1: '+str(word)+' l='+str(len(word))+' f='+str(freq)+' c='+cdict[word]+' saved: '+
				str(( freq * len(word) - (2*freq + len(word) +4) ))+'\n')
			
			repl+= 1 #deals with pointer naming system
			if (repl==62):
				replp+=1
				repl=0
				if (replp==len(pointers)):
					break
	log += ('\n\n### end of phase 1 - saved '+str(save1)+' ###\n\n\n')

	repl=0
	repl2=0
	replp=0
	save2=0
	for word, freq in freqli: #create lookup table for words that are 5 chars or longer 
		if ((3*freq+len(word)+5) < freq * (len(word)) and word not in cdict): #3f+l+5 < fl
			cdict[word] = (pointers2[replp]+chars[repl2]+chars[repl])
			save2 +=( freq * len(word) - (3*freq + len(word) +4) )
			log += ('phase 2: '+str(word)+' l='+str(len(word))+' f='+str(freq)+' c='+cdict[word]+' saved: '+
				str(( freq * len(word) - (3*freq + len(word) +4) ))+'\n')
			
			repl +=1
			if (repl==62):
				repl2 += 1
				repl = 0
				if (repl2==62):
					replp += 1
					repl2 = 0
					if (replp==2):
						print ('### phase 2: all pointers used ###')
						break

	log += ('\n\n### end of phase 2 - saved '+str(save2)+' ###\n\n\n')


	ctext = atext

	for key in cdict: #replace text with compressed text
		ctext = ctext.replace(key, cdict[key])
	ctext += '\n@@@\n'
	for key in cdict:
		ctext += (key+':'+cdict[key]+';')

	c.write(ctext)
	diff=int(len(atext)-len(ctext))
	perc=int((diff/len(atext))*100)
	l.write ('@@@dict: compressed to '+outfile+'\n'+str(diff)+' bytes ('+str(perc)+'%) compressed\n')
	print('dict: compressed \nsaved '+str(diff)+' bytes ('+str(perc)+'%)\n', sep = '')
	l.write('phase 1: '+str(save1)+'\n')
	l.write('phase 2: '+str(save2)+'\n\n\n')
	l.write(log)
	l.write('\n@@@end dict@@@\n\n')
	c.close
	a.close
	return perc

def dict_dec(infile, outfile):
	a = open (infile, 'r')
	d = open (outfile, 'w')

	atext = a.read()

	pat = re.compile(r"([a-z]{3,}|[A-Z][a-z]{2,}|[A-Z]?[a-z]*\'[a-z]+)(:)([@~^|<>][0-9a-zA-Z]|[%_][0-9a-zA-Z]{2})(;)")

	ddict = {}

	for match in pat.finditer(atext):
		ddict[match.group(1)] = match.group(3)

	dtext = atext

	for key in ddict:
		dtext = dtext.replace(ddict[key], key)
		dtext = dtext.replace((key+':'+key+';'), '')
	for key in ddict:
		dtext = dtext.replace(ddict[key], key)
		dtext = dtext.replace((key+':'+key+';'), '')
	dtext = dtext.replace('@@@', '')

	d.write (dtext)

i='in_multi.txt'
o='out_multi.hex'
di=o
do='out_multi_dec.txt'

if(len(sys.argv)==5):
	i = sys.argv[3]
	o = sys.argv[4]
	di=i
	do=o

if(len(sys.argv)==3):
	if sys.argv[1] == 'encode':
		log=open('log.txt', 'w')
		if sys.argv[2]=='huff':
			fin=i
			fout=o
			huff_enc(fin, fout, log)
			print ('saved to', o)
		elif sys.argv[2]=='dict':
			fin=i
			fout=o
			dict_enc(fin, fout, log)
			print ('saved to', o)
		elif sys.argv[2]=='multi':
			fin=i
			fout='out_dict.hex'
			p1=dict_enc(fin, fout, log)
			fin='out_dict.hex'
			fout=o
			p2=huff_enc(fin, fout, log)
			tp=int((1-(1-(p1/100))*(1-(p2/100)))*100)
			print ('saved to ', o, '\ntotal compression: ', tp, '%', sep='')
		else:
			print('usage: python3 compress_multi.py encode|decode huff|dict|multi [infile outfile]')
	elif sys.argv[1] == 'decode':
		if sys.argv[2]=='huff':
			fin=di
			fout=do
			huff_dec(fin, fout)
			print ('saved to', do)
		elif sys.argv[2]=='dict':
			fin=di
			fout=do
			dict_dec(fin, fout)
			print ('saved to', do)
		elif sys.argv[2]=='multi':
			fin=di
			fout='out_dehuff.hex'
			huff_dec(fin, fout)
			fin='out_dehuff.hex'
			fout=do
			dict_dec(fin, fout)
			print ('saved to', do)
		else:
			print('usage: python3 compress_multi.py encode|decode huff|dict|multi [infile outfile]')
	else:
		print('usage: python3 compress_multi.py encode|decode huff|dict|multi [infile outfile]')
else:
	print('usage: python3 compress_multi.py encode|decode huff|dict|multi [infile outfile]')

