import React from "react";
import  Header  from "./module/Header";
import MainApp from "./module/MainApp";
import Footer from "./module/Footer";
import "./module/css/app.css";
function App() {
  return (
    <div className = 'major-container'>
      <Header/>
      <MainApp/>
      <Footer/>
    </div>
  );
}

export default App;
