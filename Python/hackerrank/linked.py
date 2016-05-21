class Node(object):
	def __init__(self, data=None, next_node=None):
		self.data = data
		self.next = next_node


h = Node()

def print_list(head):
	
	n = head
	while True:
		d = n.data
		print(d, '\n')
		if n.next == None: break
		n = n.next

arr=input().split('->')
x=h
for n in arr:
	if n!='NULL':
		x.data=n
		x=x.next
	if n=='NULL':
		x.next=None
print(arr)
print_list(h)
