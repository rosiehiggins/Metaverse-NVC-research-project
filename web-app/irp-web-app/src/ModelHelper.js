
import * as tf from '@tensorflow/tfjs';
import * as mp_hands from '@mediapipe/hands';

export default class ModelHelper {

    constructor() {
        //
        //load MediaPipe Hands model
        //
        this.hands = new mp_hands.Hands({locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
        }});

        //
        //Load TF models
        //
        this.modelLoaded = false;
        this.model60Loaded = false;
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

    }

    getHands(){
        if(this.hands)
            return this.hands;
    }

    getModel60(){
        if(this.model60)
            return this.model60;
        
        else
            return null;     
    }

    getModel23(){
        if(this.model)
            return this.model;
        
        else
            return null;     
    }

}
