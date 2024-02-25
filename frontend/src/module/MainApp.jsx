import React, {useEffect, useState} from 'react'
import { NavBar } from "./NavBar";
import MapComponent  from "./MapComponent";
import "./css/app.css"
import axios from 'axios';


const MainApp = () => {
  // json object
  const pointsFromBackend = [
    { longitude: -90.171561, latitude: 27.921820 },
    { longitude: -85.172061, latitude: 26.920320 },
    { longitude: -86.170261, latitude: 23.920620 },
    { longitude: -83.170961, latitude: 27.922920 },
    { longitude: -84.171261, latitude: 21.921420 }
  ];


  // backend testing
  const [results, setResults] = useState([]);



  useEffect(() => {
    const genus = 'Karenia';
    const species = 'brevis';
    const fromDate = '2022-01-01';
    const toDate = '2022-01-04';
    axios.post('http://localhost:8000/api/searchHabsosDb', {
      genus,
      species,
      fromDate,
      toDate
    })
      .then(response => {
        setResults(response.data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);
  console.log(results);
  
  


  return (
    <div className='main-app-container'>
        <NavBar/>
        <MapComponent points={results}/>
    </div>
  )
}

export default MainApp