import React, {useEffect, useState} from 'react'
import CssBaseline from '@mui/material/CssBaseline';
import AppBarComponent from './component/AppBarComponent';
import DrawerComponent from './component/DrawerComponent';
import MainContent from './component/MainContent';



import "./css/app.css"
import axios from 'axios';
import 'react-datepicker/dist/react-datepicker.css';
import { formatDate, passDateCheck, passDateRangeCheck } from './helper/MainAppHelper';
import areas from './helper/bbox.json'; // Import the JSON file
import FloatingActionButton from './component/FloatingActionButton';
import Footer from './Footer';

const MainApp2 = () =>{
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };



  // start from here
  const apiUrl = process.env.REACT_APP_API_BASE_URL;
//   console.log(`API base URL is: ${apiUrl}`);  // This will show the current environment's base URL

  const [results, setResults] = useState([]);
  const [formattedDate, setFormattedDate] = useState({ fromDate: '', toDate: '' });

  const [isLoading, setIsLoading] = useState(false);
  const [recordCount, setRecordCount] = useState(0);

  const [selectedArea, setSelectedArea] = useState(null);
  const [isPredict, setIsPredict] = useState(false);
  const [condition, setCondition] = useState({}); //conditional search

  const handleAreaChange = (event) => {
    const areaName = event.target.value;
    const area = areas.find(a => a.name === areaName);
    setSelectedArea(area);
  };
  // console.log('result', results);


  const [dates, setDates] = useState({
    startDate: new Date(new Date().setMonth(new Date().getMonth() - 1)),
    endDate: new Date(),
    // startDate: new Date('2015-10-15'),  // Hardcoded start date
    // endDate: new Date('2015-10-16')     // Hardcoded end date

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

  //dev
  const sampleData = [
    {
      "id": 900809,
      "state_id": "FL",
      "description": "Marco Island Beach",
      "latitude": 25.9441,
      "longitude": -81.74501,
      "category": "not observed",
      "cellcount": 0,
      "cellcount_qa": 1,
      "cellcount_unit": "cells/L",
      "genus": "Karenia",
      "species": "brevis",
      "sample_date": "2024-03-24T06:50:00Z",
      "sample_datetime": "2024-03-24T06:50:00Z",
      "sample_depth": 0.1,
      "salinity": null,
      "salinity_qa": 9,
      "salinity_unit": null,
      "water_temp": null,
      "water_temp_qa": 9,
      "water_temp_unit": null,
      "wind_dir": null,
      "wind_dir_qa": 9,
      "wind_dir_unit": null,
      "wind_speed": null,
      "wind_speed_qa": 9,
      "wind_speed_unit": null
    },
    {
      "id": 900810,
      "state_id": "FL",
      "description": "Marco Island Beach",
      "latitude": 25.9441,
      "longitude": -81.74501,
      "category": "not observed",
      "cellcount": 10,  // Different cell count value
      "cellcount_qa": 1,
      "cellcount_unit": "cells/L",
      "genus": "Karenia",
      "species": "brevis",
      "sample_date": "2024-03-25T07:30:00Z",  // Different sample datetime
      "sample_datetime": "2024-03-25T07:30:00Z",  // Different sample datetime
      "sample_depth": 0.1,
      "salinity": null,
      "salinity_qa": 9,
      "salinity_unit": null,
      "water_temp": null,
      "water_temp_qa": 9,
      "water_temp_unit": null,
      "wind_dir": null,
      "wind_dir_qa": 9,
      "wind_dir_unit": null,
      "wind_speed": null,
      "wind_speed_qa": 9,
      "wind_speed_unit": null
    }
    // Add other objects here...
  ];
  // for frontend dev
  // const FetchData = (fromDate, toDate) => {
  //   setIsLoading(true); // Start loading
  
  //   // Filter data based on fromDate and toDate
  //   const filteredData = sampleData.filter(item => {
  //     const sampleDate = new Date(item.sample_datetime);
  //     const from = new Date(fromDate);
  //     const to = new Date(toDate);
  //     return sampleDate >= from && sampleDate <= to;
  //   });
  
  //   // Simulate a delay to mimic async data fetching
  //   setTimeout(() => {
  //     setResults(sampleData);
  //     setRecordCount(sampleData.length); // Update record count based on filtered data
  //     setIsLoading(false); // Stop loading
  //   }, 300); // Delay of 1 second
  // };








  // production db fetch
  const FetchData = (fromDate, toDate) => {
    setIsLoading(true); // Start loading
    const genus = 'Karenia';
    const species = 'brevis';
    axios.post(`${apiUrl}/api/searchHabsosDb`, {
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

  const FetchDatafromCondition = (searchParams) => {
    setIsLoading(true); // Start loading
    console.log(searchParams);
    axios.post(`${apiUrl}/api/searchHabsosDbCondition`, searchParams)
    .then(response => {
      setResults(response.data);
      setRecordCount(response.data.length); // Update record count based on response
      setIsLoading(false); // Stop loading
    })
    .catch(error => {
      console.error('Error:', error);
      setIsLoading(false); // Stop loading in case of error
    });
}


  useEffect(() => {
    if (!hasFetchedInitialData && formattedDate.fromDate && formattedDate.toDate) {
      FetchData(formattedDate.fromDate, formattedDate.toDate);
      setHasFetchedInitialData(true);
    }
  }, [formattedDate, hasFetchedInitialData]);




  const handleSubmit = () => {
    setIsPredict(false);
    setSelectedArea(null);
    console.log('mainapp,',condition);
    // fetch based on condition
    FetchDatafromCondition({
      genus: 'Karenia',
      species: 'brevis',
      fromDate: formattedDate.fromDate,
      toDate: formattedDate.toDate,
      ...condition // assuming condition is an object containing additional search parameters
    });
  };
   
  const PredictBasedOnArea = (selectedArea)=>{
    if (selectedArea) {
      // setResults(d);
      // setRecordCount(d.length); 
      // console.log('selected region', selectedArea.name);
      const url = `${apiUrl}/api/fetchForecastPredict`; 
      axios.post(url, selectedArea)
          .then(response => {
              console.log('Prediction response:', response.data);
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
    <div className='main-app-container-drawer'>
      <CssBaseline />
      <AppBarComponent open={open} handleDrawerOpen={handleDrawerOpen} />
      <DrawerComponent 
        open={open} 
        onDateChange={handleDateChange} 
        onSubmit={handleSubmit}
        dates={dates}
        areas={areas}
        onAreaChange={handleAreaChange}
        onPredict={handlePredict}
        setCondition={setCondition}
        handleDrawerClose={handleDrawerClose} />


      <div id ='fetch-loading-box'> 
          {isLoading ? (
            <div style={{ color: 'red' }}>Loading... Please wait...</div>
          ) : (
            <div>Fetched {recordCount} records.</div>
          )} 
      </div> 

      
      <MainContent 
        points={results} 
        area={selectedArea} 
        isPredict={isPredict}
        open={open} />
      <FloatingActionButton/>
      <Footer/>
    </div>
  );
}
export default MainApp2