f=open('huff_out.hex', 'rb')

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
print(enc)

#construct binary string
ostr=''
c=f.read(1)
while c:
	ostr+='{:08b}'.format(int.from_bytes(c, 'big'))
	c=f.read(1)
offset=0
runlength=1

#output decoded text
o=open('huff_decode_out.txt', 'w')
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