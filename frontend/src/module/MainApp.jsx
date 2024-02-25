import React, {useEffect, useState} from 'react'
import { NavBar } from "./NavBar";
import MapComponent  from "./MapComponent";
import "./css/app.css"

const MainApp = () => {
  // json object
  const pointsFromBackend = [
    { longitude: -90.171561, latitude: 27.921820 },
    { longitude: -85.172061, latitude: 26.920320 },
    { longitude: -86.170261, latitude: 23.920620 },
    { longitude: -83.170961, latitude: 27.922920 },
    { longitude: -84.171261, latitude: 21.921420 }
  ];



  const [message, setMessage] = useState('');
  useEffect(() => {
    fetch('http://localhost:8000/api/test')
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => console.error('Error:', error));
  }, []);
  console.log(message);
  
  


  return (
    <div className='main-app-container'>
        <NavBar/>
        {/* <MapComponent points={pointsFromBackend}/> */}
    </div>
  )
}

export default MainApp