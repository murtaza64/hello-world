import re
import sys

a = open (sys.argv[1], 'r')
d = open ('decompressed_output.txt', 'w')

atext = a.read()

pat = re.compile(r"([a-z]{3,}|[A-Z][a-z]{2,}|[A-Z]?[a-z]*\'[a-z]+)(:)([@~^|<>][0-9a-zA-Z]|[%_][0-9a-zA-Z]{2})(;)")

ddict = {}

for match in pat.finditer(atext):
	ddict[match.group(1)] = match.group(3)

open('dlog.txt', 'w').write(str(ddict))

dtext = atext

for key in ddict:
	dtext = dtext.replace(ddict[key], key)
	dtext = dtext.replace((key+':'+key+';'), '')
for key in ddict:
	dtext = dtext.replace(ddict[key], key)
	dtext = dtext.replace((key+':'+key+';'), '')
dtext = dtext.replace('@@@', '')

d.write (dtext)
