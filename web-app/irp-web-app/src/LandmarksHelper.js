//BabylonJs for Vector maths
import {Vector3} from "@babylonjs/core";

//
// Helper class for calculating properties from MediaPipe hand landmarks
//

export default class LandmarksHelper {
	
	constructor(){

	}

    //Converts MediaPipe landmark object to BabylonJs Vector 3
    landmarkToVector(landmark){
        return new Vector3(landmark.x,landmark.y,landmark.z);
    }
	
    //Given three landmarks calculate the angle between them
    getAngleBetweenLandmarks(lm0,lm1,lm2){
        let A = this.landmarkToVector(lm0);
        let B = this.landmarkToVector(lm1);
        let C = this.landmarkToVector(lm2);

        let BA = B.subtract(A);
        let CB = C.subtract(B);

        let BAnorm = BA.normalize()
        let CBnorm = CB.normalize()

        let cos = Vector3.Dot(BAnorm,CBnorm);
        let angleNorm = Math.acos(cos)/Math.PI;
        return angleNorm;
    }

    //given 2 landmarks calculate directional vector
    getDirectionVector(lm0,lm1){
        let A = this.landmarkToVector(lm0);
        let B = this.landmarkToVector(lm1);

        let BA = B.subtract(A);
        let BAnorm = BA.normalize();
        return BAnorm
    }

    //Given current position and previous position of a landmark
    //and a time diff in ms, calculate the velocity on the x axis
    getXVelocity(currentPos,prevPos,timeDiffMs){
        if(timeDiffMs===0)
            return 0
        let D = currentPos.subtract(prevPos);
        //convert to seconds
        let s = timeDiffMs/1000
        //return v on the x axis
        let velocity = D.x/s;
        return Math.abs(velocity);
    }
    
    //
    //methods for getting finger states: angle and collinear variants
    //

    //calculate finger states given array of landmarks : angle variant
    //returns boolean array containing 4 finger states [index,middle,ring,little]
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

    //calculate finger states given array of landmarks : collinear variant
    //returns boolean array containing 4 finger states [index,middle,ring,little]
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
  
}