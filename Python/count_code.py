def count_code(x):
	letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
		'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
		's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	counts=0
	for i in range (0, len(x)-3):
		y = x[i:i+4]
		if y[0:2] == 'co' and y[3] == 'e' and y[2] in letters:
			counts+=1
	return(counts)

print(count_code('abcabccodeco1eabc'))