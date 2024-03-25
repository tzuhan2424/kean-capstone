import React, {useEffect, useState} from 'react'
import { NavBar } from "./NavBar";
import MapComponent  from "./MapComponent";
import "./css/app.css"
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { formatDate, passDateCheck, passDateRangeCheck } from './helper/MainAppHelper';
import areas from './helper/bbox.json'; // Import the JSON file


const MainApp = () => {
  const [results, setResults] = useState([]);
  const [formattedDate, setFormattedDate] = useState({ fromDate: '', toDate: '' });

  const [isLoading, setIsLoading] = useState(false);
  const [recordCount, setRecordCount] = useState(0);

  const [selectedArea, setSelectedArea] = useState(null);
  const handleAreaChange = (event) => {
    const areaName = event.target.value;
    const area = areas.find(a => a.name === areaName);
    setSelectedArea(area);
  };



  const [dates, setDates] = useState({
    startDate: new Date(new Date().setMonth(new Date().getMonth() - 1)),
    endDate: new Date(),
  });
  const [hasFetchedInitialData, setHasFetchedInitialData] = useState(false);

  // console.log('dates',dates)
  // console.log('formattedDate', formattedDate)



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
      // console.log('fetch');
      // console.log(response.data);
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


  const [isPredict, setIsPredict] = useState(false);
  const handleSubmit = () => {
    setIsPredict(false);
    setSelectedArea(null);
    FetchData(formattedDate.fromDate, formattedDate.toDate);
  };

  const PredictBasedOnArea = (selectedArea)=>{
    if (selectedArea) {
      // console.log('selected region', selectedArea.name);
      const url = 'http://localhost:8000/api/fetchPredictResult'; // Change to your actual API URL

      axios.post(url, selectedArea)
          .then(response => {
              // console.log('Prediction response:', response.data);
              setResults(response.data.points);
              setRecordCount(response.data.points.length); // Update record count based on response
              setIsLoading(false); // Stop loading
          })
          .catch(error => {
              console.error('Error making prediction:', error);
              setIsLoading(false); // Stop loading in case of error
          });
    }
    else{
      console.log('you dont select region');
    }
  };




  const handlePredict = () =>{
    setIsPredict(true);
    PredictBasedOnArea(selectedArea);
  };

  


  return (
    <div className='main-app-container'>
        <NavBar 
          onDateChange={handleDateChange} 
          onSubmit={handleSubmit}
          dates={dates}
          areas={areas}
          onAreaChange={handleAreaChange}
          onPredict={handlePredict}
          />

        <div id ='fetch-loading-box'> 
          {isLoading ? (
            <div style={{ color: 'red' }}>Loading... Please wait...</div>
          ) : (
            <div>Fetched {recordCount} records.</div>
          )} 
        </div> 

        <MapComponent 
          points={results} 
          area={selectedArea} 
          isPredict={isPredict}/>
    </div>
  )
}

export default MainApp