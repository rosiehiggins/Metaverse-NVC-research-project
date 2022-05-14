//BabylonJs for Vector maths
import {Vector3} from "@babylonjs/core";

export default class GestureHeuristics {
	
	constructor(){
        this.prevMiddleTipPos = null;
        this.lastPrediction = null;
	}

    //
    //helper methods
    getFingerStatesAngle(landmarks){
        const getFingerAngle= (landmarks) =>{
            //approach from mp paper max angle of finger segment
            //wrist
            let w = new Vector3(landmarks[0].x,landmarks[0].y,landmarks[0].z);
            //knuckle
            let mcp = new Vector3(landmarks[1].x,landmarks[1].y,landmarks[1].z);
            //next joint
            let pip = new Vector3(landmarks[2].x,landmarks[2].y,landmarks[2].z);
            //next joint after that
            let dip = new Vector3(landmarks[3].x,landmarks[3].y,landmarks[3].z);
            //tip
            let t = new Vector3(landmarks[4].x,landmarks[4].y,landmarks[4].z);

            //first segment
            let seg1 = mcp.subtract(w);
            let seg1Norm = seg1.normalize();

            //second segment 
            let seg2 = pip.subtract(mcp);
            let seg2Norm = seg2.normalize();

            //third segment
            let seg3 = dip.subtract(pip);
            let seg3Norm = seg3.normalize();

            //fourth segment
            let seg4 = t.subtract(dip);
            let seg4Norm = seg4.normalize();
            
            //angle 1
            let cosAlpha = Vector3.Dot(seg1Norm,seg2Norm);
            let alphaRad = Math.acos(cosAlpha);
            let alpha = ((180/Math.PI)*alphaRad);
            //angle 2 
            let cosBeta = Vector3.Dot(seg1Norm,seg3Norm);
            let betaRad = Math.acos(cosBeta);
            let beta = ((180/Math.PI)*betaRad);
            //angle 3
            let cosGamma = Vector3.Dot(seg1Norm,seg4Norm);
            let gammaRad = Math.acos(cosGamma);
            let gamma = ((180/Math.PI)*gammaRad);

            //max angle
            let max = Math.max(alpha,beta,gamma);
            return max;
        }
       
        const getFingerStraight = (finger,angle) => {
            if(finger==="thumb")
                return angle < 45;
            else if(finger === "index")
                return angle < 80;
            else if(finger === "middle")
                return angle < 70;
            else if(finger === "ring")
                return angle < 60;
            else if(finger === "little")
                return angle < 60;
        }

        let thumbAngle = getFingerAngle([landmarks[0],landmarks[1],landmarks[2],landmarks[3],landmarks[4]])
        let thumb = getFingerStraight("thumb",thumbAngle);

        let indexAngle = getFingerAngle([landmarks[0],landmarks[5],landmarks[6],landmarks[7],landmarks[8]])
        let index = getFingerStraight("index",indexAngle);

        let middleAngle = getFingerAngle([landmarks[0],landmarks[9],landmarks[10],landmarks[11],landmarks[12]])
        let middle = getFingerStraight("middle",middleAngle);

        let ringAngle = getFingerAngle([landmarks[0],landmarks[13],landmarks[14],landmarks[15],landmarks[16]])
        let ring = getFingerStraight("ring",ringAngle);

        let littleAngle = getFingerAngle([landmarks[0],landmarks[17],landmarks[18],landmarks[19],landmarks[20]])
        let little = getFingerStraight("little",littleAngle);

        let states = [thumb,index,middle,ring,little];

        return states;
    }

	getFingerStatesCollinear(landmarks){
        //input array of landmarks [A,B,C,D]
        const getFingerStraight = (landmarks) =>{
            let A = new Vector3(landmarks[0].x,landmarks[0].y,landmarks[0].z);
            let B = new Vector3(landmarks[1].x,landmarks[1].y,landmarks[1].z);
            let C = new Vector3(landmarks[2].x,landmarks[2].y,landmarks[2].z);
            let D = new Vector3(landmarks[3].x,landmarks[3].y,landmarks[3].z);
            
            let distAB = Vector3.Distance(A,B);
            let distBC = Vector3.Distance(B,C);
            let distCD = Vector3.Distance(C,D);
            let distAD = Vector3.Distance(A,D);
            let sumDists = distAB+distBC+distCD
            let absdiff = Math.abs(sumDists-distAD)
            if(absdiff<=0.009){
                return true
            }
            else{
                return false
            }
        }

        const getThumbAngle = (landmarks) =>{
            let A = new Vector3(landmarks[0].x,landmarks[0].y,landmarks[0].z);
            let B = new Vector3(landmarks[1].x,landmarks[1].y,landmarks[1].z);
            let C = new Vector3(landmarks[2].x,landmarks[2].y,landmarks[2].z);

            let BA = A.subtract(B);
            let BC = C.subtract(B);

            let BAnorm = BA.normalize();
            let BCnorm = BC.normalize();

            let cos = Vector3.Dot(BAnorm,BCnorm);

            let angleRad = Math.acos(cos);
            let angleDeg = (180/Math.PI)*angleRad;

            if(angleDeg>60)
                return true;            
            else   
                return false;
        }
        
        let fingerStates = []
        let index = getFingerStraight([landmarks[5],landmarks[6],landmarks[7],landmarks[8]]);       
        let middle = getFingerStraight([landmarks[9],landmarks[10],landmarks[11],landmarks[12]]);
        let ring = getFingerStraight([landmarks[13],landmarks[14],landmarks[15],landmarks[16]]);
        let little = getFingerStraight([landmarks[17],landmarks[18],landmarks[19],landmarks[20]]);
        
        let thumb = getThumbAngle([landmarks[6],landmarks[2],landmarks[4]]);
        
        fingerStates.push(thumb)
        fingerStates.push(index)
        fingerStates.push(middle)
        fingerStates.push(ring)
        fingerStates.push(little)
        return fingerStates;
    }

    getDirection(lA,lB,dir){
        let A = new Vector3(lA.x,lA.y,lA.z)
        let B = new Vector3(lB.x,lB.y,lB.z)
        let AB = A.subtract(B).normalize()
        let direction = Vector3.Dot(AB,dir)
        return direction
    }

    getAngleBetweenVectors(A,B){
        let Anorm = A.normalize()
        let Bnorm = B.normalize()
        let cos = Vector3.Dot(Anorm,Bnorm);
        let angleRad = Math.acos(cos)
        let angleDeg = (180/Math.PI)*angleRad;
        return angleDeg;
    }

    getVelocity(currentPos,prevPos,timeDiffMs){
        if(timeDiffMs===0)
            return 0
        let D = currentPos.subtract(prevPos);
        //return v on the x axis
        let velocity = D.x/timeDiffMs
        return Math.abs(velocity);
    }

    //
    //Heuristics methods
    isThumbsUp(fingerStates,thumbDirection,knucklesYDirection){
        if((knucklesYDirection>0.70) && (thumbDirection>0.65) && !fingerStates[1] && !fingerStates[2] && !fingerStates[3] && !fingerStates[4])
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

    isRaiseHand(fingerStates,knucklesXDirection,knucklesYDirection,hand="Right",velocity){
        if((knucklesYDirection<0.60 && knucklesYDirection >-0.20 && hand ) && 
            ((knucklesXDirection>0.8 && hand ==="Right")||(knucklesXDirection<-0.8 && hand ==="Left")) 
            && fingerStates[1] && fingerStates[2] && fingerStates[3] && fingerStates[4]
            && velocity < 0.01){
                return true;
            }
               
        else 
            return false
    }

    isWave(fingerStates,handVelocity,knucklesXDirection,knucklesYDirection,hand="Right"){
        //fingers straight
        //palm forward
        //velocity greater than x?        
        let v = handVelocity*1000;
        if((v>0.1) &&
            (knucklesYDirection<0.80 && knucklesYDirection >-0.30 && hand ) &&
            fingerStates[1] && fingerStates[2] && fingerStates[3] && fingerStates[4] &&
            ((knucklesXDirection>0.7 && hand ==="Right")||(knucklesXDirection<-0.7 && hand ==="Left"))){
            return true;
        }          
        else 
            return false
    }

    isOK(fingerStates,distIT){
        if(distIT<=0.06 && !fingerStates[1] && fingerStates[2] && fingerStates[3] && fingerStates[4])
            return true;
        else 
            return false
    }

    //Predict gesture given landmarks
    predict(landmarks,hand){
        //return 0,1,3,4,5,
        const fingerStatesCollinear = this.getFingerStatesCollinear(landmarks);
        
        const thumbDirection = this.getDirection(landmarks[3],landmarks[4],new Vector3(0,1,0))
        const knuckleDirection = this.getDirection(landmarks[17],landmarks[5],new Vector3(0,1,0))
        const palmDirection = this.getDirection(landmarks[17],landmarks[5],new Vector3(1,0,0))

        const indexTip = new Vector3(landmarks[8].x,landmarks[8].y,landmarks[8].z);
        const thumbTip = new Vector3(landmarks[4].x,landmarks[4].y,landmarks[4].z);
        const distIT = Vector3.Distance(indexTip,thumbTip);
        
        const middleTip = new Vector3(landmarks[12].x,landmarks[12].y,landmarks[12].z);
        let handVelocity = 0;                          
        if(this.prevMiddleTipPos && this.lastPrediction){
            let td = Date.now() - this.lastPrediction;
            handVelocity = this.getVelocity(middleTip,this.prevMiddleTipPos,td);
        }

        this.prevMiddleTipPos = middleTip;
        this.lastPrediction = Date.now();

        if(this.isThumbsUp(fingerStatesCollinear,thumbDirection,knuckleDirection)){
            return 1;         
        }
        else if(this.isSwear(fingerStatesCollinear)){
            return 5;         
        }
        else if(this.isWave(fingerStatesCollinear,handVelocity,palmDirection,knuckleDirection,hand)){
            return 4;        
        }
        else if(this.isRaiseHand(fingerStatesCollinear,palmDirection,knuckleDirection,hand,handVelocity)){
            return 2;                                      
        }
        else if(this.isOK(fingerStatesCollinear,distIT)){
            return 3;         
        }
        else {
            return 0;        
        }       
    }
}