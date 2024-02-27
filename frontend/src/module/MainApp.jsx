import React, {useEffect, useState} from 'react'
import { NavBar } from "./NavBar";
import MapComponent  from "./MapComponent";
import "./css/app.css"
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { formatDate, passDateCheck, passDateRangeCheck } from './helper/MainAppHelper';

const MainApp = () => {
  const [results, setResults] = useState([]);
  // const [dates, setDates] = useState({ startDate: null, endDate: null });
  const [formattedDate, setFormattedDate] = useState({ fromDate: '', toDate: '' });

  const [isLoading, setIsLoading] = useState(false);
  const [recordCount, setRecordCount] = useState(0);

  const [dates, setDates] = useState({
    startDate: new Date(new Date().setMonth(new Date().getMonth() - 1)),
    endDate: new Date(),
  });
  const [hasFetchedInitialData, setHasFetchedInitialData] = useState(false);

  useEffect(() => {
    const formattedFromDate = dates.startDate ? formatDate(dates.startDate) : '';
    const formattedToDate = dates.endDate ? formatDate(dates.endDate) : '';
    setFormattedDate({ fromDate: formattedFromDate, toDate: formattedToDate });
  }, [dates]); // Depend on `dates` to trigger this effect
  
  const handleDateChange = (newDate) => {
    setDates(prevDates => ({ ...prevDates, ...newDate }));
  };


  const FetchData = (fromDate, toDate) => {
    setIsLoading(true); // Start loading
    const genus = 'Karenia';
    const species = 'brevis';
    axios.post('http://localhost:8000/api/searchHabsosDb', {
      genus,
      species,      
      fromDate,
      toDate,
    })
    .then(response => {
      setResults(response.data);
      setRecordCount(response.data.length); // Update record count based on response
      setIsLoading(false); // Stop loading
    })
    .catch(error => {
      console.error('Error:', error);
      setIsLoading(false); // Stop loading in case of error
    });
  };

  useEffect(() => {
    if (!hasFetchedInitialData && formattedDate.fromDate && formattedDate.toDate) {
      FetchData(formattedDate.fromDate, formattedDate.toDate);
      setHasFetchedInitialData(true);
    }
  }, [formattedDate, hasFetchedInitialData]);

  const handleSubmit = () => {
    FetchData(formattedDate.fromDate, formattedDate.toDate);
  };

  // console.log(results);
  
  


  return (
    <div className='main-app-container'>
        <NavBar 
          onDateChange={handleDateChange} 
          onSubmit={handleSubmit}
          dates={dates}/>
    {/* <div style={{ position: 'relative', zIndex: 9999 }}> 
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <p>Fetched {recordCount} records.</p>
      )} 
    </div>  */}
        <MapComponent points={results}/>
    </div>
  )
}

export default MainApp