n=100
factors=[]
for i in range (1,int(n/2+1)):
	if 100%i == 0:
		if( ((i,int(100/i) not in factors) and ((int(100/i),i) not in factors) ) ):
			factors.append((i,int(100/i)))
print(factors)
