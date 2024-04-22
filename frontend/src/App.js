import React from "react";
import  Header  from "./module/Header";
import MainApp from "./module/MainApp";
import Footer from "./module/Footer";
import "./module/css/app.css";
function App() {

  const environment = process.env.REACT_APP_APP_ENV;
  console.log(environment)
  return (
    <div className = 'major-container'>
      <Header/>
      <MainApp/>
      <Footer/>
    </div>
  );
}

export default App;
