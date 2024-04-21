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
      <div>
      {environment === 'production' ? (
        <p>This is running in Production.</p>
      ) : (
        <p>This is running in Development.</p>
      )}
    </div>
      <Header/>
      <MainApp/>
      <Footer/>
    </div>
  );
}

export default App;
