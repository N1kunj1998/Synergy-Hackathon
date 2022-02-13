import logo from './logo.svg';
import './App.css';
import Home from './components/Home/Home'
import Symptoms from "./components/symptoms/Symptoms.js";
import Post from './components/pdf/Post';
import card from './components/symptoms/Card'
import { BrowserRouter as Router,Routes,Route,Link} from "react-router-dom";

function App() {
  return (
    <div className="App">
<Router>
      <Routes>
        <Route exact path='/' element={<Home />}></Route>
        <Route exact path='/post' element={<Post />}></Route>
        <Route exact path='/symptoms' element={<Symptoms />}></Route>
      </Routes></Router>


    </div>
  );
}

export default App;
