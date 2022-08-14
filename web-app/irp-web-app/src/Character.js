import { SceneLoader, AssetsManager, Color3, 
    Mesh, AbstractMesh, StandardMaterial, 
    TransformNode, MeshBuilder, CurrentScreenBlock} from "@babylonjs/core";

import "@babylonjs/loaders/glTF";


export default class Character{

    constructor(app, onCharacterLoaded){

        this.app = app;

        
        //
		//Create the asset manager
		//		
        this.assetsManager = new AssetsManager(this.app.scene);
		this.assetsManager.useDefaultLoadingScreen = false;

        //
        //Create emote texture tasks
        //
        this.thumbsupTask = this.assetsManager.addTextureTask("thumbsuptask", "assets/thumbsup.png");
		this.thumbsupTask.onSuccess = (task) => {this.thumbsupTex = task.texture;}

        this.okTask = this.assetsManager.addTextureTask("oktask", "assets/ok.png");
		this.okTask.onSuccess = (task) => {this.okTex = task.texture; }

        this.waveTask = this.assetsManager.addTextureTask("wavetask", "assets/wave.png");
		this.waveTask.onSuccess = (task) => {this.waveTex = task.texture; }

        this.raisehandTask = this.assetsManager.addTextureTask("raisehandtask", "assets/raisehand.png");
		this.raisehandTask.onSuccess = (task) => {this.raisehandTex = task.texture; }

        //
        //Create face texture tasks (for blink)
        //
        this.eyesOpenTask = this.assetsManager.addTextureTask("eyesOpenTask", "assets/charEyeOpen.png",false,false);
		this.eyesOpenTask.onSuccess = (task) => {this.eyesOpenTex = task.texture; console.log(this.eyesOpenTex)}

        this.eyesClosedTask = this.assetsManager.addTextureTask("eyesClosedTask", "assets/charEyeClosed.png",false,false);
		this.eyesClosedTask.onSuccess = (task) => {this.eyesClosedTex = task.texture;}
        
        //Import character meshes
        SceneLoader.ImportMeshAsync("", "assets/", "character.glb", this.app.scene)
        .then((characterMeshes)=>{
            this.characterModel = characterMeshes;
            console.log(characterMeshes);
			
			this.currentAnim = this.characterModel.animationGroups.find((el)=>{return el.name == "idle"});
            this.startBlink()

            //create emote pivot
            this.emoteBillboardPivot = new TransformNode("emote pivot", this.app.scene);
            this.emoteBillboardPivot.position.y = 1.9; 
            this.emoteBillboardPivot.parent = characterMeshes[0]; 

			onCharacterLoaded();

        })

		this.transitioning = false;

        //load textures with asset manager
        this.assetsManager.load();

        //rotate camera round to face character
        this.app.scene.activeCamera.alpha += Math.PI;
    }

    //
	//function sets the animation of the character model
	//
	setAnimation(name){
		
		let found = false; 
		
		for(let group of this.characterModel.animationGroups){
			if(group.name === name || group.name === ('clone_' + name)){
				found = true; 
				if(!group.isPlaying){
					group.reset(); 
					group.play(true); 
					this.currentAnim = group;
				}
			}
			else{
				if(group.isPlaying){
					group.pause();
				}
			}
		}
		
		if(!found){
			console.log("Problem: could not find animation named:" + name); 
		}
		
	}

	transitionAnimation(name,speed=1,onExit){

		
		this.prevAnim = this.currentAnim;

		this.currentAnim = this.characterModel.animationGroups.find((el)=>{return el.name == name});

		this.currentAnim.play(true);

		this.transitioning = true;

		this.transitionSpeed = speed;

		this.transitionCounter = 0;

		this.onExitTransition = onExit;

	}

	//update loop for character
	update(){
		let dT = this.app.scene.getEngine().getDeltaTime()/1000;

		if(this.transitioning){
			if (this.transitionCounter<1){
				this.transitionCounter += dT * this.transitionSpeed;
				const weightTo = Math.max(0 + this.transitionCounter,1);
				const weightFrom = Math.max(1 - this.transitionCounter,0);
				this.prevAnim.setWeightForAllAnimatables(weightFrom);
				this.currentAnim.setWeightForAllAnimatables(weightTo);				
			}
			else{
				this.transitioning = false;
				if(this.onExitTransition){
					this.onExitTransition()
				}
			}
				
		}		
	}

    setEmoteBoard(name){

        if(!this.emoteBillboard){
			this.emoteTexture = {}
			this.emoteTexture['thumbsup'] = this.thumbsupTex;
			this.emoteTexture['ok'] = this.okTex;
			this.emoteTexture['raisehand'] = this.raisehandTex;
			this.emoteTexture['wave'] = this.waveTex;
			
			let size = 0.5;
			this.emoteBillboard = new MeshBuilder.CreatePlane("emote plane", {width:size, height:size}, this.app.scene, false);
			this.emoteBillboard.renderingGroupId = 2;
			this.emoteBillboard.billboardMode = AbstractMesh.BILLBOARDMODE_Y;

			this.emoteBillboard.parent = this.emoteBillboardPivot; 		
			this.emoteBillboard.material = new StandardMaterial("emote material", this.app.scene);
			this.emoteBillboard.material.specularColor = new Color3(0, 0, 0);
			this.emoteBillboard.material.useAlphaFromDiffuseTexture = true;
		}
		
		if(name === 'thumbsup'){
			this.emoteBillboardPivot.setEnabled(true);
			this.emoteBillboard.material.emissiveTexture = this.emoteTexture[name];
			this.emoteBillboard.material.opacityTexture = this.emoteTexture[name];
			this.emoteBillboard.material.diffuseTexture = this.emoteTexture[name];
			
		}
		else if(name === 'ok'){
			this.emoteBillboardPivot.setEnabled(true);
			this.emoteBillboard.material.emissiveTexture = this.emoteTexture[name];
			this.emoteBillboard.material.opacityTexture = this.emoteTexture[name];
			this.emoteBillboard.material.diffuseTexture = this.emoteTexture[name];
		}
		
		else if(name === 'wave'){
			this.emoteBillboardPivot.setEnabled(true);
			this.emoteBillboard.material.emissiveTexture = this.emoteTexture[name];
			this.emoteBillboard.material.opacityTexture = this.emoteTexture[name];
			this.emoteBillboard.material.diffuseTexture = this.emoteTexture[name];
		}		

		else if(name === 'raisehand'){
			this.emoteBillboardPivot.setEnabled(true);
			this.emoteBillboard.material.emissiveTexture = this.emoteTexture[name];
			this.emoteBillboard.material.opacityTexture = this.emoteTexture[name];
			this.emoteBillboard.material.diffuseTexture = this.emoteTexture[name];
		}
		
		else{
			this.emoteBillboardPivot.setEnabled(false);
		}
	}

	startBlink(){			
		
		this.faceMesh = this.characterModel.meshes.find((el)=>{return el.name == "head"})
		
		if(this.faceMesh){
			//clear timers if already running
			if(typeof this.blinkTimer !== "undefined")
				clearInterval(this.blinkTimer); 
			
			//Run blink animation
			let RandomInRange = (min, max) => {return (Math.random() * (max - min) ) + min; };
			this.blinkTimer = setInterval(()=>{				
				this.faceMesh.material.albedoTexture= this.eyesClosedTex;				
				setTimeout(()=>{				
					this.faceMesh.material.albedoTexture = this.eyesOpenTex;					
				}, 200);
			}, RandomInRange(3000, 6000) ); 
			
		}
		 		
	}
   

}