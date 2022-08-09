import './App.css';
import Main from './Main';
import ModelContext from "./ModelContext"; 
import ModelHelper from "./ModelHelper"; 

function App() {
  return (
    <ModelContext.Provider value= {new ModelHelper()}>
        <Main/>
    </ModelContext.Provider>  
  );
}

export default App;
