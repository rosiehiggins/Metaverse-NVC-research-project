import * as tf from '@tensorflow/tfjs';
import LandmarksHelper from './LandmarksHelper';

export default class GestureClassifier {
	
	constructor(){
        this.modelLoaded = false;
        //load 23 input model
        tf.loadLayersModel('model/23-input/model.json')
        .then((model)=>{
            this.model = model;
            this.modelLoaded = true;
            console.log("model 23 loaded" + this.modelLoaded );
        })    
        //load 60 input model
        tf.loadLayersModel('model/60-input/model.json')
        .then((model)=>{
            this.model60 = model;
            this.model60Loaded = true;
            console.log("model 60 loaded" + this.model60Loaded);
        })    
        //landmarks helper functions
        this.landmarksHelper = new LandmarksHelper(); 
	}

    //normalise and convert landmarks to list
    convertLandmarks(landmarks,hand,scalelm=9){
        let scalex = 1
        if(hand==="Left")
            scalex = -1       
        //return landmarks in format for model
        //get wrist for origin
        let wrist = landmarks[0]
        //get scale landmark
        let slm = landmarks[scalelm];
        //translate scale landmark
        let slmt = {x: slm.x-wrist.x, y: slm.y-wrist.y, z: slm.z-wrist.z}
        let scalingFactor = 1/(Math.sqrt(Math.pow(slmt.x,2) + Math.pow(slmt.y,2) + Math.pow(slmt.z,2)));
        let lms = []
        let i = 0
        for (const landmark of landmarks){
            if(i!==0){
                lms.push(((landmark.x-wrist.x)*scalingFactor)*scalex);
                lms.push((landmark.y-wrist.y)*scalingFactor);
                lms.push((landmark.z-wrist.z)*scalingFactor);
            }  
            i++;
        }
        let tensor = tf.tensor([lms]);
        return tensor;
    }

    flipLandmarks(landmarks){
        let flippedLandmarks = [];
        for (const landmark of landmarks){
            let newLandmark = {x:landmark.x*-1,y:landmark.y,z:landmark.z};
            flippedLandmarks.push(newLandmark);
        }
        return flippedLandmarks;
    }

    convertLandmarksToFeatures(lms,hand){
        let features = [];

        if(hand==="Left"){
            lms = this.flipLandmarks(lms);
        }

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

        let tensor = tf.tensor([features]);
        return tensor;

    }

    //set the confidence threshold based on gesture
    getConfidenceThreshold(index){
        if(index===0)
            return 0.8
        else if(index === 1)
            return 0.5
        else if (index === 2)
            return 0.3
        else if (index === 3)
            return 0
    }

    //set the confidence threshold based on gesture for 60 input
    getConfidenceThreshold60(index){
        if(index===0)
            return 0.4
        else if(index === 1)
            return 0.8
        else if (index === 2)
            return 0.6
        else if (index === 3)
            return 0
    }

    predict(landmarks,hand){
        if(!this.modelLoaded)
         return Promise.resolve(null);
        //return gesture prediction
        let inputTensor = this.convertLandmarksToFeatures(landmarks,hand);
        let resultTensor = this.model.predict(inputTensor);
        return resultTensor.data()
        .then((result)=>{
           let prediction = Math.max(result[0],result[1],result[2],result[3]);
           //console.log("prediction " + prediction);
           let index = result.indexOf(prediction);
           let value = 3         
           if(prediction> this.getConfidenceThreshold60(index))
               value = index                    
           return value;
        });
    }

    predict60(landmarks,hand){
        if(!this.model60Loaded)
        return Promise.resolve(null);
       //return gesture prediction
       let inputTensor = this.convertLandmarks(landmarks,hand,9);
       let resultTensor = this.model60.predict(inputTensor);
       return resultTensor.data()
       .then((result)=>{
           let prediction = Math.max(result[0],result[1],result[2],result[3]);
           //console.log("prediction " + prediction);
           let index = result.indexOf(prediction);
           let value = 3         
           if(prediction> this.getConfidenceThreshold60(index))
               value = index                    
           return value;
       });
    }
}