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

//App
import ResultsQueue from './ResultsQueue';
import GestureClassifier from './GestureClassifier';
import GestureHeuristics from './GestureHeuristics';

//useful blog https://itnext.io/accessing-the-webcam-with-javascript-and-react-33cbe92f49cb

class Main extends React.Component {

	constructor(props){	
		super(props);
		this.state = {
            displayLandmarks:false,
            selfieMode:true,
            modeltype:"Heuristic",
            leftGesture:"None",
            rightGesture:"None",
            availableGestures:{"Heuristic":["Thumbs up","Raise hand","OK","Wave"],"Neural network":["Thumbs up","Raise hand","OK"]}
        };

        //references html video and canvas elements
        this.videoRef = React.createRef();
        this.canvasRef = React.createRef();

        //bind UI methods to main class
        this.toggleDisplayLandmarks = this.toggleDisplayLandmarks.bind(this);
        this.handleModelChange = this.handleModelChange.bind(this);
        this.stopCamera = this.stopCamera.bind(this);
        this.startCamera = this.startCamera.bind(this);

        //buffer to hold results for each hand
        this.resultsQueueLeft = new ResultsQueue(6);
        this.resultsQueueRight = new ResultsQueue(6);

        //classifier models
        this.GestureClassifier = new GestureClassifier();
        this.GestureHeuristics = new GestureHeuristics();

        //initialise state timers
        this.leftHandTimer = null;
        this.rightHandTimer = null;
        
        //map model outputs to render states
        this.statesMap = {0:"Thumbs up",1:"Raise hand",2:"OK",3:"None",4:"Wave",5:">:-("};

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
        //get video html element
        let videoRef = this.videoRef.current
        
        //
        //Real time performance variables
        //
        this.handstimes = [];

        this.benchmarks = {
            "MPTimes": [],
            "Heuristic":[],
            "NeuralNetwork":[],
            "NeuralNetwork60":[]
        }
        
        //
        //load MediaPipe Hands model
        //
        this.hands = new mp_hands.Hands({locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
        }});
        //configure hands model
        this.hands.setOptions({
            maxNumHands: 2,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5,
            selfieMode:true,
        });
        //set results call back function
        this.hands.onResults((results)=>{
            //add to benchmarks
            if(this.t0){
                const t1 = performance.now();
                let diff = t1 - this.t0;
                this.benchmarks["MPTimes"].push(diff)
                if(this.benchmarks["MPTimes"].length>100)
                    this.benchmarks["MPTimes"].shift();                
            }    
            //predict results
            this.predictResults(results)
        });

        //Frameskip variables
        this.framesToSkip = 1;
        this.frameCount = 0;

        //
        //Camera
        //
        this.camera = new camera_utils.Camera(videoRef, {
            onFrame: async () => {  
                if (this.frameCount > this.framesToSkip)
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

        this.camera.start()
    }

    componentWillUnmount(){
        this.camera.stop();
    }

    predictResults(results){
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
        
        canvasCtx.drawImage(
            image, 0, 0, canvasRef.width, canvasRef.height);

        if(results){
            if (results.multiHandWorldLandmarks) {    
                let i = 0;        
                for (const landmarks of results.multiHandWorldLandmarks) {
                    const hand = results.multiHandedness[i].label
                    
                    //clear and reset hand timers
                    if(this.handAPI[hand].resetTimer)
                        clearTimeout(this.handAPI[hand].resetTimer);
                    
                    this.handAPI[hand].resetTimer = setTimeout(()=>{
                            this.handAPI[hand].setHandState("None");
                            this.handAPI[hand].resultsQueue.refresh();},500);
                    
                    const t0 = performance.now(); 
                    const modelType = this.state.modeltype;
                    new Promise ((resolve,reject) => {
                        //predict gesture based on chosen model
                        if(modelType === "Heuristic"){
                            let prediction = this.handAPI[hand].predictHeuristics(landmarks,hand);
                            resolve(prediction)
                        }
                        else if(modelType === "NeuralNetwork"){
                            resolve(this.GestureClassifier.predict(landmarks,hand))
                        }
                        else if(modelType === "NeuralNetwork60"){
                            resolve(this.GestureClassifier.predict60(landmarks,hand))
                        }
                    })
                    .then((prediction) => {
                        if(prediction!==null){
                            //calculate benchmarks
                            if(t0){
                                const t1 = performance.now();
                                let diff = t1 - t0;
                                this.benchmarks[modelType].push(diff);
                                if(this.benchmarks[modelType].length>100)
                                    this.benchmarks[modelType].shift();
                            }
                            //set states
                            this.handAPI[hand].resultsQueue.enqueue(prediction);
                            const handstate = this.handAPI[hand].resultsQueue.getResult();
                            this.handAPI[hand].setHandState(this.statesMap[handstate]);                            
                        }                       
                    })
                    .catch((error)=>{
                        console.log(error)
                    })
                    i++;
                }
            }
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

    toggleDisplayLandmarks(){
        let state = this.state.displayLandmarks;
        state = !state
        this.setState({displayLandmarks:state}) 
    }

    handleModelChange(val){
        //refresh results buffers
        this.resultsQueueLeft.refresh();
        this.resultsQueueRight.refresh();
        //set model state
        this.setState({modeltype:val})
    }

    renderGestureImage(gesture,flip=false){        
        let img = (<Box sx={{height:"256px"}}/>);
        if(gesture==="Thumbs up")
            img = (<Box component="img" src="./assets/thumbsup.jpg" sx={{transform:((flip) ? "scaleX(-1)" :"")}}/>);
        else if(gesture==="Raise hand")
            img = (<Box component="img" src="./assets/raisehand.jpg" sx={{transform:((flip) ? "scaleX(-1)" :"")}}/>);
        else if(gesture==="OK")
            img = (<Box component="img" src="./assets/ok.jpg" sx={{ transform:((flip) ? "scaleX(-1)" :"")}}/>);
        else if(gesture==="Wave")
            img = (<Box component="img" src="./assets/wave.jpg" sx={{transform:((flip) ? "scaleX(-1)" :"")}}/>);
        return img;
    }

    stopCamera(){
        this.camera.stop();
    }

    startCamera(){
        this.camera.start()
    }

	render() {		
		return (
            <Box sx={{ p: 2, display:'flex',justifyContent:"center",alignItems:"center",flexDirection:"column"}}>
                <FPSStats  top={10} left={10}/>
                <Typography variant="h5" sx={{mx:1}}>Non verbal communication in 3D virtual worlds prototype 👍👌✋👋</Typography>               
                <div style={{position:'relative', width:"720px", height:"438px", margin:10 ,border: '1px solid grey'}}>
                    <video ref={this.videoRef} style={{position:'absolute',width:"100%",height:"100%", transform: this.state.selfieMode ? "scale(-1, 1)" : "scale(1,1)"}}/>               
                    <canvas ref={this.canvasRef} width={720} height={438} style={{position:'absolute',width:"100%",height:"100%"}}/>                   
                </div>
                <Box sx={{display:'flex',justifyContent:"space-around",alignItems:"center",flexDirection:"row", width:"720px", marginTop:1}}>
                    <Button sx={{mx:2}} onClick = {()=>{this.toggleDisplayLandmarks()}} variant="contained">{this.state.displayLandmarks ? "Hide keypoints" : "Show keypoints"}</Button>
                    {/*<Button sx={{mx:2}} onClick = {()=>{console.log(JSON.stringify(this.benchmarks))}} variant="contained">log benchmarks</Button>*/}
                    {/*<Button sx={{mx:2}} onClick = {()=>{this.stopCamera()}} variant="contained">stop cam</Button>
                    <Button sx={{mx:2}} onClick = {()=>{this.startCamera()}} variant="contained">start cam</Button>*/}
                    <FormControl >
                        <InputLabel id="model-select-label">Model type</InputLabel>
                        <Select
                        labelId="model-select-label"
                        id="model-select"
                        value={this.state.modeltype}
                        label="Select model"
                        variant="outlined"
                        onChange={(e)=>this.handleModelChange(e.target.value)}
                        >
                            <MenuItem value={"Heuristic"}>Heuristic</MenuItem>
                            <MenuItem value={"NeuralNetwork"}>Neural net 23 input</MenuItem>
                            <MenuItem value={"NeuralNetwork60"}>Neural net 60 input</MenuItem>
                        </Select>
                    </FormControl>                    
                    <Box sx={{display:'flex',justifyContent:"center",alignItems:"center",flexDirection:"column", }}>
                        <Typography variant="body" sx={{mx:1}}>Average hands inference time (ms):</Typography>
                        <Typography variant="body2" sx={{mx:1}}>{this.state.averageHandsms?this.state.averageHandsms:""}</Typography>
                    </Box>              
                </Box>
                <Box sx={{display:'flex',justifyContent:"space-around",alignItems:"center",flexDirection:"row",marginTop:2, width:"720px"}}>
                    <Box>
                        <Typography variant="body2" sx={{mx:1}}>Left hand prediction: {this.state.leftGesture}</Typography>
                        {this.renderGestureImage(this.state.leftGesture)}
                    </Box>
                    <Box sx={{display:'flex',justifyContent:"space-between",alignItems:"space-between",flexDirection:"column"}}>
                        <Typography variant="body2" sx={{mx:1}}>Right hand prediction: {this.state.rightGesture}</Typography>
                        {this.renderGestureImage(this.state.rightGesture,true)}
                    </Box>
                    
                </Box>
            </Box>            
        )		
	}	
}

export default Main; 