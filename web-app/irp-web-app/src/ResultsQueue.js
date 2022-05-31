
//https://www.geeksforgeeks.org/implementation-queue-javascript/

export default class ResultsQueue {
	
	constructor(maxLength=10){
        this.maxLength = maxLength;
        this.items = [];
	}
	
    // enqueue function
    enqueue(element)
    {                    
        //handle overflow
        if(this.items.length>=this.maxLength){
            //pop one off the front
            this.items.shift();
        }
        // adding element to the back of queue
        this.items.push(element);
    }

    // dequeue function
    dequeue()
    {
        // removing element from the queue
        // returns underflow when called 
        // on empty queue
        if(this.isEmpty())
            return "Underflow";
        return this.items.shift();
    }
	
    getResult(){
        let modes = this.mode(this.items);
        let front = this.front(this.items);     
        if (modes.length > 1 && modes.includes(front))
            return front;
        else
            return modes[0];       
    }

    // front function
    front()
    {
        // returns the Front element of 
        // the queue without removing it.
        if(this.isEmpty())
            return "No elements in Queue";
        return this.items[0];
    }

    // isEmpty function
    isEmpty()
    {
        // return true if the queue is empty.
        return this.items.length == 0;
    }

    refresh(){
        let arr = Array(this.maxLength);
        arr.fill(3);
        this.items = arr;
    }

    mode(items) {
        // as result can be bimodal or multi-modal,
        // the returned result is provided as an array
        // mode of [3, 5, 4, 4, 1, 1, 2, 3] = [1, 3, 4]
        let modes = [], count = [], i, number, maxIndex = 0;
     
        for (i = 0; i < items.length; i += 1) {
            number = items[i];
            count[number] = (count[number] || 0) + 1;
            if (count[number] > maxIndex) {
                maxIndex = count[number];
            }
        }
     
        for (i in count)
            if (count.hasOwnProperty(i)) {
                if (count[i] === maxIndex) {
                    modes.push(Number(i));
                }
            }
     
        return modes;
    }    
}