import re
import sys

a = open(sys.argv[1],'r')
c = open('compressed_output.txt', 'w')
l = open('log.txt', 'w')
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
				print ('### phase 1: all pointers used ###\n')
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
l.write ('output saved as compressed_output.txt\n'+str(diff)+' bytes ('+str(perc)+'%) compressed\n')
print('output saved as compressed_output.txt\n',diff,' bytes (',perc,'%) compressed\n', sep = '')
l.write('phase 1: '+str(save1)+'\n')
l.write('phase 2: '+str(save2)+'\n\n\n')
l.write(log)