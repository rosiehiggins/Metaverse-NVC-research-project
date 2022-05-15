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

//custom
import ResultsQueue from './ResultsQueue';
import GestureClassifier from './GestureClassifier';
import GestureHeuristics from './GestureHeuristics';

//useful blog https://itnext.io/accessing-the-webcam-with-javascript-and-react-33cbe92f49cb

class Main extends React.Component {

	constructor(props){	
		super(props);
		this.state = {
            inferring:false,
            selfieMode:true,
            modeltype:"Heuristic",
            leftGesture:"none",
            rightGesture:"none",
        };

        this.leftHandState = "idle";
        this.rightHandState = "idle";

        this.videoRef = React.createRef();
        this.canvasRef = React.createRef();
        this.canvasFaceRef = React.createRef();

        this.toggleInference = this.toggleInference.bind(this);
        this.handleModelChange = this.handleModelChange.bind(this);

        //buffer to hold results
        this.resultsQueue = new ResultsQueue(10)
        //classifier models
        this.GestureClassifier = new GestureClassifier();
        this.GestureHeuristics = new GestureHeuristics();
        
        //map model outputs to render states
        this.statesMap = {0:"None",1:"Thumbs up",2:"Raise hand",3:"OK",4:"Wave",5:">:-("}
	}	

    componentDidMount(){
        //need video element and canvas element
        let videoRef = this.videoRef.current
        
        //
        //load MediaPipe hands model
        //
        this.hands = new mp_hands.Hands({locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
        }});

        this.hands.setOptions({
            maxNumHands: 2,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5,
            selfieMode:true,
        });

        this.hands.onResults((results)=>{this.predictResults(results)});

        //
        //Preformance variables
        //
        this.times = [];
        this.handstimes = [];
        
        //
        //Camera
        //
        this.camera = new camera_utils.Camera(videoRef, {
            onFrame: async () => {  
                
                //reset state for hand results
                if(this.lastHandResults){
                    let delta = Date.now() - this.lastHandResults;
                    if((delta>500)){
                        this.setState({leftGesture:"none"})
                    }
                }              
                   
                let t0 =  performance.now();      
                await this.hands.send({image: videoRef});                
                let t1 = performance.now();


                let tdiffHands = t1-t0;
                this.handstimes.push(tdiffHands);             
                if(this.handstimes.length > 100){
                    let averageHandsTime = Math.round(this.handstimes.reduce((a,b) => a + b, 0) / this.handstimes.length);
                    this.setState({averageHandsms:averageHandsTime});
                    this.handstimes = [];
                }
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

        if(this.state.inferring){
            canvasCtx.drawImage(
                image, 0, 0, canvasRef.width, canvasRef.height);

            if(results){
                if (results.multiHandWorldLandmarks) {    
                    let i = 0;        
                    for (const landmarks of results.multiHandWorldLandmarks) {
                        const hand = results.multiHandedness[i].label

                        let prediction = 0
                        
                        //predict gesture based on chosen model
                        if(this.state.modeltype === "Heuristic"){
                            prediction = this.GestureHeuristics.predict(landmarks,hand);
                        }
                        else if(this.state.modeltype === "NeuralNetwork"){
                            //todo make this an async function so prediction can happen async and improve performance
                            prediction = this.GestureClassifier.predict(landmarks,hand);
                        }

                        //add latest prediction to queue
                        this.resultsQueue.enqueue(prediction);
                      
                        //add state to queue and get result
                        this.leftHandState = this.resultsQueue.getResult();

                        //set render state
                        this.setState({leftGesture:this.statesMap[this.leftHandState]});  

                        //get time for last results
                        this.lastHandResults = Date.now();
                        i++;
                    }
                }

                //use screen space landmarks to render hand keypoints on screen with media pipe
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

    toggleInference(){
        let state = this.state.inferring;
        state = !state
        this.setState({inferring:state}) 
    }

    handleModelChange(val){
        //refresh results buffer
        this.resultsQueue.refresh();
        //set model state
        this.setState({modeltype:val})
    }

	render() {		
		return (
            <Box sx={{ p: 2, display:'flex',justifyContent:"center",alignItems:"center",flexDirection:"column"}}>
                <div style={{position:'relative', width:"720px", height:"438px", margin:10 ,border: '1px solid grey'}}>
                    <video ref={this.videoRef} style={{position:'absolute',width:"100%",height:"100%", transform: this.state.selfieMode ? "scale(-1, 1)" : "scale(1,1)"}}/>               
                    <canvas ref={this.canvasRef} width={720} height={438} style={{position:'absolute',width:"100%",height:"100%"}}/>
                </div>
                <Box sx={{display:'flex',justifyContent:"center",alignItems:"center",flexDirection:"row"}}>
                    <Button sx={{mx:2}} onClick = {()=>{this.toggleInference()}} variant="contained">{this.state.inferring ? "Hide keypoints" : "Show keypoints"}</Button>
                    <FormControl >
                        <InputLabel id="model-select-label">Model type</InputLabel>
                        <Select
                        labelId="model-select-label"
                        id="model-select"
                        value={this.state.modeltype}
                        label="Select model"
                        onChange={(e)=>this.handleModelChange(e.target.value)}
                        >
                            <MenuItem value={"Heuristic"}>Heuristic</MenuItem>
                            <MenuItem value={"NeuralNetwork"}>Neural network</MenuItem>
                        </Select>
                    </FormControl>                    
                    <Box sx={{display:'flex',justifyContent:"center",alignItems:"center",flexDirection:"column"}}>
                        <Typography variant="body" sx={{mx:1}}>Average hands inference time (Ms):</Typography>
                        <Typography variant="body" sx={{mx:1}}>{this.state.averageHandsms?this.state.averageHandsms:""}</Typography>
                    </Box>              
                </Box>
                <Box sx={{display:'flex',justifyContent:"center",alignItems:"center",flexDirection:"row"}}>
                    <Typography sx={{mx:1}}>{this.state.leftGesture}</Typography>
                </Box>
            </Box>            
        )		
	}	
}

export default Main; 