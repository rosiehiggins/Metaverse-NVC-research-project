
import * as tf from '@tensorflow/tfjs';
import GestureClassifier from './GestureClassifier';

export default class ModelHelper {

    constructor() {
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
