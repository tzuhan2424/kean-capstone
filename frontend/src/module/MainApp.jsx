import React, {useEffect, useState} from 'react'
import { NavBar } from "./NavBar";
import MapComponent  from "./MapComponent";
import "./css/app.css"
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { formatDate, passDateCheck, passDateRangeCheck } from './helper/MainAppHelper';

const MainApp = () => {
  // backend testing
  const [results, setResults] = useState([]);
  const [dates, setDates] = useState({ startDate: null, endDate: null });
  const [formattedDate, setFormattedDate] = useState({ fromDate: '', toDate: '' });



  useEffect(() => {
    // Assuming `formatDate` returns a string in 'YYYY-MM-DD' format
    const formattedFromDate = dates.startDate ? formatDate(dates.startDate) : '';
    const formattedToDate = dates.endDate ? formatDate(dates.endDate) : '';
    setFormattedDate({ fromDate: formattedFromDate, toDate: formattedToDate });
  }, [dates]); // Depend on `dates` to trigger this effect
  
  const handleDateChange = (newDate) => {
    setDates(prevDates => ({ ...prevDates, ...newDate }));
  };


  console.log(formattedDate);
  console.log("dates", dates);


  // json object
  const pointsFromBackend = [
    { longitude: -90.171561, latitude: 27.921820 },
    { longitude: -85.172061, latitude: 26.920320 },
    { longitude: -86.170261, latitude: 23.920620 },
    { longitude: -83.170961, latitude: 27.922920 },
    { longitude: -84.171261, latitude: 21.921420 }
  ];



  const handleSubmit = () => {
    const genus = 'Karenia';
    const species = 'brevis';

    axios.post('http://localhost:8000/api/searchHabsosDb', {
      genus,
      species,
      fromDate: formattedDate.fromDate,
      toDate: formattedDate.toDate,
    })
    .then(response => {
      setResults(response.data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
    

    };

  // console.log(results);
  
  


  return (
    <div className='main-app-container'>
        <NavBar 
          onDateChange={handleDateChange} 
          onSubmit={handleSubmit}/>
        <MapComponent points={results}/>
    </div>
  )
}

export default MainApp