import * as tf from '@tensorflow/tfjs';
import LandmarksHelper from './LandmarksHelper';

export default class GestureClassifier {
	
	constructor(){
        this.modelLoaded = false;
        tf.loadLayersModel('model/v13/model.json')
        .then((model)=>{
            this.model = model;
            this.modelLoaded = true;
            console.log("model loaded" + this.modelLoaded);
        })          
        this.landmarksHelper = new LandmarksHelper(); 
	}

    convertHand(hand){
        if(hand==="Right")
            return 1
        else
            return 0
    }
	
    //normalise and convert landmarks to list
    convertLandmarks(landmarks,hand,trans={x:0,y:0,z:0},scalelm=9){
        //return landmarks in format for model
        let slm = landmarks[scalelm];
        let slmt = {x: slm.x-trans.x, y: slm.y-trans.y, z: slm.z-trans.z}
        let scalingFactor = 1/(Math.sqrt(Math.pow(slmt.x,2) + Math.pow(slmt.y,2) + Math.pow(slmt.z,2)));
        let lms = []
        let i = 0
        for (const landmark of landmarks){
            if(i!==0){
                lms.push((landmark.x-trans.x)*scalingFactor)
                lms.push((landmark.y-trans.y)*scalingFactor)
                lms.push((landmark.z-trans.z)*scalingFactor)
            }  
            i++;
        }
        let handnum = this.convertHand(hand)
        lms.push(handnum)
        let tensor = tf.tensor([lms]);
        return tensor;
    }

    convertLandmarksToFeatures(lms,hand){
        let features = [];
        //thumb 0
        let thumb0 = this.landmarksHelper.getAngleBetweenLandmarks(lms[0],lms[2],lms[3]);
        features.push(thumb0);

        let thumb1 = this.landmarksHelper.getAngleBetweenLandmarks(lms[2],lms[3],lms[4]);
        features.push(thumb1);

        let index0 = this.landmarksHelper.getAngleBetweenLandmarks(lms[0],lms[5],lms[6]);
        features.push(index0);

        let index1 = this.landmarksHelper.getAngleBetweenLandmarks(lms[5],lms[6],lms[7]);
        features.push(index1);

        let index2 = this.landmarksHelper.getAngleBetweenLandmarks(lms[6],lms[7],lms[8]);
        features.push(index2);

        let middle0 = this.landmarksHelper.getAngleBetweenLandmarks(lms[0],lms[9],lms[10]);
        features.push(middle0);

        let middle1 = this.landmarksHelper.getAngleBetweenLandmarks(lms[9],lms[10],lms[11]);
        features.push(middle1);

        let middle2 = this.landmarksHelper.getAngleBetweenLandmarks(lms[10],lms[11],lms[12]);
        features.push(middle2);

        let ring0 = this.landmarksHelper.getAngleBetweenLandmarks(lms[0],lms[13],lms[14]);
        features.push(ring0);

        let ring1 = this.landmarksHelper.getAngleBetweenLandmarks(lms[13],lms[14],lms[15]);
        features.push(ring1);

        let ring2 = this.landmarksHelper.getAngleBetweenLandmarks(lms[14],lms[15],lms[16]);
        features.push(ring2);

        let little0 = this.landmarksHelper.getAngleBetweenLandmarks(lms[0],lms[17],lms[18]);
        features.push(little0);

        let little1 = this.landmarksHelper.getAngleBetweenLandmarks(lms[17],lms[18],lms[19]);
        features.push(little1);

        let little2 = this.landmarksHelper.getAngleBetweenLandmarks(lms[18],lms[19],lms[20]);
        features.push(little2);

        let palmdir =this.landmarksHelper.getDirectionVector(lms[0],lms[9]);
        features.push(palmdir.x);
        features.push(palmdir.y);
        features.push(palmdir.z);

        let knuckledir = this.landmarksHelper.getDirectionVector(lms[17],lms[5]);
        features.push(knuckledir.x);
        features.push(knuckledir.y);
        features.push(knuckledir.z);

        let thumbdir = this.landmarksHelper.getDirectionVector(lms[3],lms[4]);
        features.push(thumbdir.x);
        features.push(thumbdir.y);
        features.push(thumbdir.z);

        let handnum = this.convertHand(hand);
        features.push(handnum);

        let tensor = tf.tensor([features]);
        return tensor;

    }

    predict(landmarks,hand){
        if (this.modelLoaded){
            //return gesture prediction
            let inputTensor = this.convertLandmarksToFeatures(landmarks,hand);
            //console.log(this.model)
            let resultTensor = this.model.predict(inputTensor);
            //data() method is async - will use this in prod version but will stay async for now
            let result = resultTensor.dataSync();
            console.log("result " + result)
            let prediction = Math.max(result[0],result[1],result[2])
            //let prediction = result[0];
            let index = result.indexOf(prediction)
            console.log("prediction " + prediction)
            let value = 0
            ///let prediction = 0           
            if(prediction>0.50){
                value = index + 1
                console.log("value " + value)
            }           
            return value;
        }       
        return "Model not loaded"
    }
}