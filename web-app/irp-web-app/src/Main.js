//React
import * as React from 'react';

//Material UI
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

//MediaPipe
import * as mp_hands from '@mediapipe/hands';
import * as drawing_utils from '@mediapipe/drawing_utils';
import * as camera_utils from '@mediapipe/camera_utils';

//FPS meter
import FPSStats from "react-fps-stats";

//Babylon
import { Vector3, 
    HemisphericLight, 
    DirectionalLight,
    Color4,
    ArcRotateCamera} from "@babylonjs/core";

//Is
import is from 'is_js'

//App
import ResultsQueue from './ResultsQueue';
import GestureClassifier from './GestureClassifier';
import GestureHeuristics from './GestureHeuristics';
import ModelContext from './ModelContext';
import BabylonSceneComponent from './BabylonSceneComponent';
import Character from './Character'

//Loading Ring
import "./LoadingRing.css";

class Main extends React.Component {
    static contextType = ModelContext;

	constructor(props){	
		super(props);
		this.state = {
            displayLandmarks:true,
            selfieMode:true,
            modeltype:"NeuralNetwork60",
            availableGestures:"Gestures: 👍👌✋",
            leftGesture:"None",
            rightGesture:"None",
            frameSkip:1,
            loading:true
        };

        //references html video and canvas elements
        this.videoRef = React.createRef();
        this.canvasRef = React.createRef();

        //bind UI methods to main class
        this.toggleDisplayLandmarks = this.toggleDisplayLandmarks.bind(this);
        this.handleModelChange = this.handleModelChange.bind(this);
        this.handleUpdateFrameskip = this.handleUpdateFrameskip.bind(this);
        this.onSceneReady = this.onSceneReady.bind(this);
		this.onRender = this.onRender.bind(this);

        //buffer to hold results for each hand
        this.resultsQueueLeft = new ResultsQueue(8);
        this.resultsQueueRight = new ResultsQueue(8);

        //classifier models
        this.GestureClassifier = new GestureClassifier();
        this.GestureHeuristics = new GestureHeuristics();

        //initialise state timers
        this.leftHandTimer = null;
        this.rightHandTimer = null;
        
        //map model outputs to render states
        this.statesMap = {0:"thumbsup",1:"raisehand",2:"ok",3:"none",4:"wave",5:"swear"};

        //animation states
        this.currentAnimHandstate = 3;

        //hand API
        this.handAPI = {"Left":{
                            "resetTimer":this.leftHandTimer,
                            "resultsQueue":this.resultsQueueLeft,
                            "setHandState":(state) =>{if (state !== this.state.leftGesture) {this.setState({leftGesture:state});}},
                            "predictHeuristics": this.GestureHeuristics.predictLeft,

                        },
                        "Right":{
                            "resetTimer":this.rightHandTimer,
                            "resultsQueue":this.resultsQueueRight,
                            "setHandState":(state) =>{if (state !== this.state.rightGesture) {this.setState({rightGesture:state});}},
                            "predictHeuristics": this.GestureHeuristics.predictRight,
                        }};


	}	


    componentDidMount(){
        const modelHelper = this.context;

        //get video html element
        let videoRef = this.videoRef.current
        
        //
        //Real time performance variables
        //
        this.handstimes = [];
        
        //
        //get MP hands from context
        //
        this.hands = modelHelper.getHands();

        //configure hands model
        this.hands.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5,
            selfieMode:true,
        });

        let wasmcounter = 0;
        //set results call back function
        this.hands.onResults((results)=>{
            if(wasmcounter<1){
                wasmcounter ++;
                this.setState({loading:false});
            }           
            //predict results
            this.predictResults(results)
        });

        //Variable to keep count of frameskip
        this.frameCount = 0;

        //
        //Camera
        //
        this.camera = new camera_utils.Camera(videoRef, {
            onFrame: async () => {  
                if (this.frameCount > this.state.frameSkip)
                    this.frameCount = 0

                if (this.frameCount===0){
                    this.t0 =  performance.now();      
                    await this.hands.send({image: videoRef});                
                    let t1 = performance.now();
    
                    let tdiffHands = t1-this.t0;
                    this.handstimes.push(tdiffHands);             
                    if(this.handstimes.length > 100){
                        let averageHandsTime = Math.round(this.handstimes.reduce((a,b) => a + b, 0) / this.handstimes.length);
                        this.setState({averageHandsms:averageHandsTime});
                        this.handstimes = [];
                    }
                }
                this.frameCount ++;
            },
            width: 720,
            height: 438
        });

        this.camera.start();
    }

    componentWillUnmount(){
        this.camera.stop();
    }

	onSceneReady(scene) {
		
		let DEGTORAD = 0.01745329251; 
		this.scene = scene; 
		this.scene.clearColor = new Color4(0, 0, 0, 0);
		this.camera = new ArcRotateCamera("maincamera", -90* DEGTORAD, 70*DEGTORAD, 3, new Vector3(0, 1, 0), scene);
        const light = new HemisphericLight("light", new Vector3(1, 1, 0), scene);			
        this.sunlight = new DirectionalLight("sunlight", new Vector3(-0.5, -1, 0), scene);
        this.sunlight.position = new Vector3(20, 40, 20);
        this.sunlight.intensity = 0.5
        
        //load character asset
		this.character = new Character(this,()=>{this.setState({assetsLoaded:true})});
        this.scene.getEngine().resize();
	}

    onRender(scene) {
		if(this.state.assetsLoaded){		
            this.character.update()	
		}
		scene.render();
	}


    //Given MediaPipe results predict gesture output
    predictResults(results){

        const modelHelper = this.context;

        //get html5 canvas element
        let canvasRef = this.canvasRef.current
        let canvasCtx = canvasRef.getContext('2d');  
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasRef.width, canvasRef.height);

        let image = null;
        if(results.image)
            image = results.image;
        
        if(!image){
            return
        }
        
        //draw video image onto canvas
        canvasCtx.drawImage(
            image, 0, 0, canvasRef.width, canvasRef.height);
        
        //If landmark results are present
        if(results){
            if (results.multiHandWorldLandmarks) {    
                let i = 0;    
                //iterate over world space landmarks    
                for (const landmarks of results.multiHandWorldLandmarks) {
                    const hand = results.multiHandedness[i].label
                    
                    //clear and reset hand timers
                    if(this.handAPI[hand].resetTimer)
                        clearTimeout(this.handAPI[hand].resetTimer);
                    
                    this.handAPI[hand].resetTimer = setTimeout(()=>{
                            this.setAnimationState(3);
                            this.handAPI[hand].setHandState("None");
                            this.handAPI[hand].resultsQueue.refresh();},500);
                    
                    const t0 = performance.now(); 
                    const modelType = this.state.modeltype;

                    //run gesture predictions
                    new Promise ((resolve,reject) => {
                        //predict gesture based on chosen model
                        if(modelType === "Heuristic"){
                            let prediction = this.handAPI[hand].predictHeuristics(landmarks,hand);
                            resolve(prediction)
                        }
                        else if(modelType === "NeuralNetwork"){
                            resolve(this.GestureClassifier.predict(landmarks,hand,modelHelper.getModel23()))
                        }
                        else if(modelType === "NeuralNetwork60"){
                            resolve(this.GestureClassifier.predict60(landmarks,hand,modelHelper.getModel60()))
                        }
                    })
                    .then((prediction) => {
                        if(prediction!==null){
                            //set result states to render gesture
                            this.handAPI[hand].resultsQueue.enqueue(prediction);
                            const handstate = this.handAPI[hand].resultsQueue.getResult();
                            this.handAPI[hand].setHandState(this.statesMap[handstate]);  
                            this.setAnimationState(handstate,hand);                       
                        }                       
                    })
                    .catch((error)=>{
                        console.log(error)
                    })
                    i++;
                }
            }
            //render landmarks over video
            if(this.state.displayLandmarks){
            //use screen space landmarks to render hand keypoints on screen with MediaPipe
            if (results.multiHandLandmarks) {            
                    for (const landmarks of results.multiHandLandmarks) {
                        drawing_utils.drawConnectors(canvasCtx, landmarks, mp_hands.HAND_CONNECTIONS,
                                        {color: '#00FF00', lineWidth: 1});
                        drawing_utils.drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', width: 0.5});
                    }
                }
            }
        }
        
        canvasCtx.restore();
        return
    }

    //set animation name based on state and hand
    setAnimName(handState,hand){
        if(handState===0)
            return "jump";
        else if(handState === 1 && hand === "Right")
            return "raisehandL";
        else if(handState === 1 && hand === "Left")
            return "raisehandR";  
        else if(handState === 1 && hand === "none")
            return "raisehandL";      
        else if(handState === 2)
            return "agreement";  
        else if(handState === 3)
            return "idle";    
        else if(handState === 4 && hand === "Right")
            return "wavingL"; 
        else if(handState === 4 && hand === "Left")
            return "wavingR"; 
        else if(handState === 4 && hand === "none")
            return "wavingR"; 
        else if(handState === 5)
            return "idle";  
    }

    //set animation state of character
    setAnimationState(handstate,hand="none"){
        const anim = this.setAnimName(handstate,hand)
        const state = this.statesMap[handstate];
        this.character.setEmoteBoard(state);
        const closeEyes = handstate === 2 ? true : false;
        if(this.character.animationState === "running"){
            this.character.setAnimationState("transitioning");
            this.character.startAnimationTransition(anim,5,closeEyes);  
        }                    
    }

    //method to toggle the display of hand landmarks
    toggleDisplayLandmarks(){
        let state = this.state.displayLandmarks;
        state = !state
        this.setState({displayLandmarks:state}) 
    }

    //update model type selected
    handleModelChange(val){
        let availGesturesTxt = "Gestures: 👍👌✋"
        if(val==="Heuristic")
            availGesturesTxt = "Gestures: 👍👌✋👋";
        //refresh results buffers
        this.resultsQueueLeft.refresh();
        this.resultsQueueRight.refresh();
        //set model state
        this.setState({modeltype:val,availableGestures:availGesturesTxt})
    }

    //update n frames to be skipped and update length of results queue to reduce latency
    handleUpdateFrameskip(val){
        if(val<2){
            this.resultsQueueLeft.setMaxLength(8);
            this.resultsQueueRight.setMaxLength(8);           
        }
        else{
            this.resultsQueueLeft.setMaxLength(6);
            this.resultsQueueRight.setMaxLength(6); 
        }      
        this.setState({frameSkip:val})
    }



    //Render UI components
	render() {	

		return (
            <Box sx={{ position: "relative", display:'flex', height:"100%", justifyContent:"center",alignItems:"center",flexDirection:"column"}}>

                {this.state.loading && 
                 <Box sx={{display:"flex", alignItems:"center", justifyContent:"center",flexDirection:"column", position:"fixed",width:"100%",height:"100%",top:0,left:0,zIndex:10,backgroundColor:"rgba(0, 0, 0, 0.8)"}}>
                        <Typography align="center" sx={{mb:"10px",color:"#fff"}}>Make sure you have a web cam connected!</Typography>
                        <Typography align="center" sx={{mb:"25px",color:"#fff"}}>This demo performs best in a well lit room!</Typography>
						<Box maxWidth="md" sx={{}}>                          
							<div className="lds-ring"><div></div><div></div><div></div><div></div></div>                           
						</Box>
                 </Box>
                }
                
                <FPSStats top={"auto"} bottom={0} left={0}/>

                <Button 
                    target='_blank' 
                    href='https://thegrapevine.tech/' 
                    variant='contained' 
                    sx={{position:"fixed",bottom:{xs:0,sm:"auto"},top:{sm:"5px"},right:{sm:"5px"},backgroundColor:"#4326B8",'&:hover': {backgroundColor: "#2C119B"}}}>
                        Try Grapevine!
                </Button>
                
                <Typography align="center" variant="h5" sx={{m:{xs:"5px",sm:"20px"}}}>Grapevine gestures prototype</Typography>               
                
                <Box sx={{display:"flex", flexDirection:{xs:"column",sm:"row"},alignItems:"center"}}>
                <Box sx={{position:'relative', width:{xs:"219px",sm:"420px",lg:"720px"}, height:{xs:"360px",sm:"256px",lg:"438px"}, m:"5px", border: '3px solid #333',borderRadius:"10px"}}>
                    <video ref={this.videoRef} style={{position:'absolute',width:"100%",height:"100%", transform: this.state.selfieMode ? "scale(-1, 1)" : "scale(1,1)"}}/>               
                    <canvas ref={this.canvasRef} width={720} height={438} style={{position:'absolute',width:"100%",height:"100%"}}/>                   
                </Box>
                <Box sx={{
                        position:"relative",
                        width:{xs:"360px",sm:"420px",lg:"720px"},
                        height:{xs:"219px",sm:"256px",lg:"438px"},
                        m:"5px",
                        border: '3px solid #333333',
                        borderRadius:"10px"}}
                >
                    <Box sx={{
                            display:"flex",
                            alignItems:"center",
                            position:"absolute",
                            bottom:0,
                            left:0,
                            backgroundColor:"#333",
                            width: this.state.availableGestures ==="Gestures: 👍👌✋👋" ? "180px" : "160px",
                            height:"25px",
                            borderRadius:"0px 5px 0px 0px"}}
                    >
                        <Typography sx={{ml:"5px",color:"#fff"}}>{this.state.availableGestures}</Typography>

                    </Box>
                    <Box sx={{
                            display:"flex",
                            alignItems:"center",
                            position:"absolute",
                            top:0,
                            left:0,
                            backgroundColor:"#333",
                            width: "150px",
                            height:"25px",
                            borderRadius:"0px 0px 5px 0px"}}
                    >
                        <Typography sx={{ml:"5px",color:"#fff"}}>Left:{this.state.leftGesture}</Typography>

                    </Box>
                    <Box sx={{
                            display:"flex",
                            alignItems:"center",
                            position:"absolute",
                            top:0,
                            right:0,
                            backgroundColor:"#333",
                            width: "150px",
                            height:"25px",
                            borderRadius:"0px 0px 0px 5px"}}
                    >
                        <Typography sx={{ml:"5px",color:"#fff"}}>Right:{this.state.rightGesture}</Typography>

                    </Box>
                    <Box sx={{position: 'absolute',width: '100%', height: '100%',zIndex: -1}}>
                        <BabylonSceneComponent antialias onSceneReady={this.onSceneReady} onRender={this.onRender} id="my-canvas" />
                    </Box>
                </Box>
                </Box>
                
                <Box sx={{
                        borderStyle:"solid", 
                        display:'flex',
                        p:{xs:"2px",sm:"16px"},
                        borderRadius:"10px",
                        borderColor:"#333333",
                        justifyContent:{md:"center"},
                        alignItems:{xs:"stretch",md:"center"},
                        flexDirection:{xs:"column",md:"row"}, 
                        width:{xs:"360px",md:"720px"},
                        m:{xs:"5px",md:"10px"}}}
                >
                    <Button 
                        sx={{flex:1,m:"5px",backgroundColor:"#4326B8",'&:hover': {backgroundColor: "#2C119B"}}} 
                        onClick = {()=>{this.toggleDisplayLandmarks()}} 
                        variant="contained"
                    >
                        {this.state.displayLandmarks ? "Hide landmarks" : "Show landmarks"}
                    </Button>
                    <FormControl sx={{flex:1, m:"5px"}}>
                        <InputLabel id="frame-skip">Frame skip</InputLabel>
                        <Select
                        labelId="frame-skip"
                        id="frame-skip"
                        value={this.state.frameSkip}
                        label="Frame skip"
                        variant="standard"
                        onChange={(e)=>this.handleUpdateFrameskip(e.target.value)}                       
                        >
                            <MenuItem value={0}>0</MenuItem>
                            <MenuItem value={1}>1</MenuItem>
                            <MenuItem value={2}>2</MenuItem>
                            <MenuItem value={3}>3</MenuItem>
                            <MenuItem value={4}>4</MenuItem>
                        </Select>
                    </FormControl>  
                    <FormControl sx={{flex:1,m:"5px"}}>
                        <InputLabel id="model-select-label">Model type</InputLabel>
                        <Select
                        labelId="model-select-label"
                        id="model-select"
                        value={this.state.modeltype}
                        label="Select model"
                        variant="standard"                        
                        onChange={(e)=>this.handleModelChange(e.target.value)}
                        >
                            <MenuItem value={"Heuristic"}>Heuristic</MenuItem>
                            <MenuItem value={"NeuralNetwork"}>ANN 23 input</MenuItem>
                            <MenuItem value={"NeuralNetwork60"}>ANN 60 input</MenuItem>
                        </Select>
                    </FormControl>                    
                    <Box sx={{flex:1, m:"5px", display:'flex',justifyContent:"center",alignItems:"center",flexDirection:"column", }}>
                        <Typography variant="body" sx={{}}>Av. hands inference time (ms):</Typography>
                        <Typography variant="body2" sx={{}}>{this.state.averageHandsms?this.state.averageHandsms:""}</Typography>
                    </Box>              
                </Box>
            </Box>            
        )		
	}	
}

export default Main; 