
//https://medium.com/@venkatperi/javascript-state-machines-a-tutorial-972863e37825
//read this blog
//check out xstate https://www.npmjs.com/package/xstate

export default class WaveMachine {
	
	constructor(callback=null){
        this.state = "idle";
        this.subState = null;
        this.prevSubState = null;
        this.callback = callback
	}
	
    onWaveEvent(event) {
        this.subState = event;
        //clear timer if it exists
        if(this.timer)
			clearTimeout(this.timer)
		//set new timer
        this.timer = setTimeout(() => {
            console.log("time out");
            console.log("wave machine state: idle");
            this.state = "idle"; 
            //fire callback to update react state
            if(this.callback){
                this.callback();
            }
                
            }, 1000);

        if(this.state==="idle"){
            this.state = "waveStart";
        }
        else if(this.state==="waveStart"){
            if(this.wavingTimer)            
                clearTimeout(this.wavingTimer);
            //need wavestart timer to avoid flipping between wave start and none
            if(this.subState !== this.prevSubState)
                this.state = "waving";
            
            if(this.waveStartTimer)            
                clearTimeout(this.waveStartTimer);
            //set new timer
            this.waveStartTimer = setTimeout(() => {
                console.log("wave start time out");    
                this.state="idle"                   
                //fire callback to update react state
                if(this.callback){
                    this.callback();
                }                   
            }, 500);
        }
        else if(this.state==="waving"){
            if(this.waveStartTimer)            
                clearTimeout(this.waveStartTimer);

            if(this.subState !== this.prevSubState)
                this.state = "waving";
            
            if(this.wavingTimer)            
                clearTimeout(this.wavingTimer);
            //set new timer
            this.wavingTimer = setTimeout(() => {
                console.log("waving time out");
                console.log("wave machine state: idle");
                this.state = "idle"; 
                //fire callback to update react state
                if(this.callback){
                    this.callback();
                }                   
            }, 100);
        }

        console.log("wave machine state: " + this.state )
        this.prevSubState=this.subState;  
        return this.state;
    }

    getState(){
        return this.state;
    }

	
}