from statistics import mode,multimode

# A Sample class with init method
class ResultsQueue:
    items=[]

    def __init__(self, maxLength=3):
        self.maxLength = maxLength
  
    # add element to front of queue
    def enqueue(self,el):
        if len(self.items) >= self.maxLength:
            self.items.pop()
        self.items.insert(0,el)

    # remove element from back of queue
    def dequeue(self):
        if len(self.items) == 0:
            return "overflow"
        return self.items.pop()
    
    #get mode of results and return result
    #if tie break return first mode unless front in modes then return front
    def getResult(self):
        if len(self.items) == 0:
            return 0
        mode_ = mode(self.items)        
        return mode_
        #modes = multimode(self.items)
        #print("modes")
        #print(modes)
        #front = self.front()
        #if len(modes)>1 and front in modes:
            #return front
        #else:
           #return modes[0]

    def front(self):
        if len(self.items) == 0:
            return "empty"
        return self.items[0]

    
    def isEmpty(self):
        return len(self.items) == 0