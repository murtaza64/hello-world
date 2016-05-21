import copy

data1 = {'murtaza':('ohjun','chloe','sophie'),
        'chloe':('ohjun','arnav','murtaza'),
        'hugo':('ohjun', 'murtaza', 'sophie'),
        'sophie':('murtaza',),
        'arnav':('hugo', 'murtaza', 'ohjun'),
        'ohjun':('murtaza', 'arnav')
        }
data = {'murtaza':('arnav', 'ohjun'),
        'ohjun':('arnav', 'murtaza'),
        'arnav':('ohjun', 'murtaza')}

class node:
    predecessors=None
    nexts=None
    student=''
    def __init__(self, student='', predecessors=None):
        self.student=student
        self.nexts=[]
        if predecessors is None:
            self.predecessors = []
        else:
            self.predecessors=copy.deepcopy(predecessors)
    def grow(self, max=6, depth=0):
        if not self.student in self.predecessors:
            self.predecessors.append(self.student)
            for pref in data[self.student]:
                next=node(pref, self.predecessors)
                print(depth, self.predecessors, self.student, pref)
                next.grow(max, depth=depth+1)
                self.nexts.append(next)
        else:
            return
    def crawl(self, preds=[]):
        preds.append(self.student)
        if self.nexts:
            for next in self.nexts:
                next.crawl(preds)
        else:
            print(preds)
#Parsing of files needed + Write to file.
#Iterating multiple times over same data and calculating precentage match.
#Might be interesting to see if there is another approach than recursive method
#Eg taking common occurences of friends eg Josh comes 12 time Oh jun comes 17 times
#In list and use them as the seeds... If you get what I mean.
# Hugo
        
forms = [] #You need to figure out how to define form
           #capacities as variable and be able to display teacher names etc
           #Class structure? or struct.
mort = node()
mort.student='murtaza'
mort.grow()
#mort.crawl()