//BabylonJs for Vector maths
import {Vector3} from "@babylonjs/core";

export default class LandmarksHelper {
	
	constructor(){

	}

    landmarkToVector(landmark){
        return new Vector3(landmark.x,landmark.y,landmark.z);
    }
	
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

    getDirectionVector(lm0,lm1){
        let A = this.landmarkToVector(lm0);
        let B = this.landmarkToVector(lm1);

        let BA = B.subtract(A);
        let BAnorm = BA.normalize();
        return BAnorm
    }
  
}