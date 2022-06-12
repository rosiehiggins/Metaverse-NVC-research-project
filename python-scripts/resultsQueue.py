from statistics import mode,multimode

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

    #return front of queue
    def front(self):
        if len(self.items) == 0:
            return "empty"
        return self.items[0]

    
    def isEmpty(self):
        return len(self.items) == 0