import React from "react";
import  Header  from "./module/Header";
import MainApp from "./module/MainApp";
import MainApp2 from "./module/MainApp2";

import Footer from "./module/Footer";
import "./module/css/app.css";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import About from "./module/About";
import { Welcome } from "./Welcome";

function App() {

  const environment = process.env.REACT_APP_APP_ENV;
  return (
    // <div className = 'major-container'>
    //   {/* <Header/> */}
    //   {/* <MainApp/> */}
    //   <MainApp2/>
    //   <Footer/>
    // </div>

    <Router>
      <div className="major-container">
        {/* <Header /> */}
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/tidetrack" element={<MainApp2 />} />
          <Route path="/about" element={<About />} />
          </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
