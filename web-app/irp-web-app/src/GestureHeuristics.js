//BabylonJs for Vector maths
import {Vector3} from "@babylonjs/core";
import LandmarksHelper from './LandmarksHelper';

export default class GestureHeuristics {
	
	constructor(){
        //variables for previous middle tip position
        this.prevMiddleTipPosLeft = null;
        this.prevMiddleTipPosRight = null;
        //variables for last prediction time
        this.lastPredictionLeft = null;
        this.lastPredictionRight = null;
        //bind predict methods to this class
        this.predictLeft = this.predictLeft.bind(this);
        this.predictRight = this.predictRight.bind(this);

        //landmarks helper
        this.landmarksHelper = new LandmarksHelper();
	}

    //
    //Heuristics methods
    isThumbsUp(fingerStates,thumbTipY,knuckleY){
        if((knuckleY>0.70) && (thumbTipY>0.55) && !fingerStates[1] && !fingerStates[2] && !fingerStates[3] && !fingerStates[4])
            return true;
        
        else 
            return false
    }

    isSwear(fingerStates){
        if(!fingerStates[1] && fingerStates[2] && !fingerStates[3] && !fingerStates[4])
            return true;   
        else 
            return false
    }

    isRaiseHand(fingerStates,knuckleX,palmY,hand="Right",velocity){
        if((palmY>0.85) && 
            ((knuckleX>0.75 && hand ==="Right")||(knuckleX<-0.75 && hand ==="Left")) 
            && fingerStates[1] && fingerStates[2] && fingerStates[3] && fingerStates[4]
            && velocity < 0.01){
                return true;
            }
               
        else 
            return false
    }


    isWave(fingerStates,handVelocity,knuckleX,palmY,hand="Right"){
        //fingers straight
        //palm forward
        //velocity greater than x?     
        let v = handVelocity*1000;
        if((handVelocity>0.1) &&
            (palmY >0.5) &&
            fingerStates[1] && fingerStates[2] && fingerStates[3] && fingerStates[4] &&
            ((knuckleX>0.4 && hand ==="Right")||(knuckleX<-0.4 && hand ==="Left"))){
            return true;
        }          
        else 
            return false
    }

    isOK(fingerStates,distIT,knuckleX,palmY,hand="Right"){
        if((palmY>0.85) && 
            ((knuckleX>0.50 && hand ==="Right")||(knuckleX<-0.50 && hand ==="Left"))
            && distIT<=0.06 && !fingerStates[1] && fingerStates[2] && fingerStates[3] && fingerStates[4])
            return true;
        else 
            return false
    }

    //Predict gesture given landmarks
    predict(landmarks,hand,lastPrediction,middleTip,prevMiddleTipPos){

        //return 0,1,3,4,5,
        const fingerStatesCollinear = this.landmarksHelper.getFingerStatesCollinear(landmarks);
        
        const knuckleDir = this.landmarksHelper.getDirectionVector(landmarks[5],landmarks[17])

        const thumbTipY = this.landmarksHelper.getDirectionVector(landmarks[4],landmarks[3]).y;
        const knuckleX = knuckleDir.x;
        const knuckleY = knuckleDir.y;
        const palmY = this.landmarksHelper.getDirectionVector(landmarks[9],landmarks[0]).y;


        const indexTip = new Vector3(landmarks[8].x,landmarks[8].y,landmarks[8].z);
        const thumbTip = new Vector3(landmarks[4].x,landmarks[4].y,landmarks[4].z);
        
        const distIT = Vector3.Distance(indexTip,thumbTip);
        
        let handVelocity = 0; 

        if(prevMiddleTipPos && lastPrediction){
            let td = Date.now() - lastPrediction;
            handVelocity = this.landmarksHelper.getXVelocity(middleTip,prevMiddleTipPos,td);
        }

        if(this.isThumbsUp(fingerStatesCollinear,thumbTipY,knuckleY)){
            return 0;         
        }
        else if(this.isSwear(fingerStatesCollinear)){
            return 5;         
        }
        else if(this.isWave(fingerStatesCollinear,handVelocity,knuckleX,palmY,hand)){
            return 4;        
        }
        else if(this.isRaiseHand(fingerStatesCollinear,knuckleX,palmY,hand,handVelocity)){
            return 1;                                      
        }
        else if(this.isOK(fingerStatesCollinear,distIT,knuckleX,palmY,hand)){
            return 2;         
        }
        else {
            return 3;        
        }       
    }

    predictLeft(landmarks,hand){
        //set up temporal left hand variables
        const lastPrediction = this.lastPredictionLeft;
        const prevMiddleTipPos = this.prevMiddleTipPosLeft;
        const middleTip = new Vector3(landmarks[12].x,landmarks[12].y,landmarks[12].z);        
        //predict
        const prediction = this.predict(landmarks,hand,lastPrediction,middleTip,prevMiddleTipPos);
        //update temporal right hand variables
        this.prevMiddleTipPosLeft = middleTip;
        this.lastPredictionLeft = Date.now();
        return prediction;
    }

    predictRight(landmarks,hand){
        //set up temporal right hand variables
        const lastPrediction = this.lastPredictionRight;
        const prevMiddleTipPos = this.prevMiddleTipPosRight;
        const middleTip = new Vector3(landmarks[12].x,landmarks[12].y,landmarks[12].z);
        //predict
        const prediction = this.predict(landmarks,hand,lastPrediction,middleTip,prevMiddleTipPos);
        //update temporal right hand variables
        this.prevMiddleTipPosRight = middleTip;
        this.lastPredictionRight = Date.now();
        
        return prediction;
    }
}