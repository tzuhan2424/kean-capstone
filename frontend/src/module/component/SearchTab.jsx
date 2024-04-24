import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import '../css/NavBar.css'
import '../css/component.css'

import 'react-datepicker/dist/react-datepicker.css';
import { formatDate } from '../helper/MainAppHelper';
import { passDateCheck,passDateRangeCheck } from '../helper/MainAppHelper';
import ConditionSelector from './ConditionSelector';
import { Legend } from './Legend';
const SearchTab = ({ onDateChange, onSubmit, dates, setCondition}) => {
  const [formattedDate, setFormattedDate] = useState({ fromDate: '', toDate: '' });
  const [fromDateValidationError, setFromDateValidationError] = useState(''); 
  const [endDateValidationError, setEndDateValidationError] = useState(''); 
  const [DateValidationError, setDateValidationError] = useState(''); 


  const onConditionChange = (data) => {
    setCondition(data);
    console.log('Updated condition:', data);
  };

  useEffect(() => {
    // Assuming `formatDate` returns a string in 'YYYY-MM-DD' format
    const formattedFromDate = dates.startDate ? formatDate(dates.startDate) : '';
    const formattedToDate = dates.endDate ? formatDate(dates.endDate) : '';
    setFormattedDate({ fromDate: formattedFromDate, toDate: formattedToDate });
  }, [dates]);



  useEffect(() => {
    if (dates.startDate) {
      if (formattedDate.fromDate && !passDateCheck(formattedDate.fromDate)) {
        setFromDateValidationError('Invalid start date: 1955-3000');
      } else {
        setFromDateValidationError('');
      }
    }
    if (dates.endDate) {
      if (formattedDate.toDate && !passDateCheck(formattedDate.toDate)) {
        setEndDateValidationError('Invalid end date: 1955-3000');
      } else {
        setEndDateValidationError('');
      }
    }
  }, [formattedDate]);

  const handleSubmit = () => {
    if (passDateCheck(formattedDate.fromDate) && passDateCheck(formattedDate.toDate) 
        && passDateRangeCheck(formattedDate.fromDate, formattedDate.toDate)) {
          onSubmit(); // Call the passed onSubmit prop function
          setDateValidationError('');

    }else{

        setDateValidationError('invalid input range');
    }
  };

  return (
    <div>
      <div>Search historical data from 1955 to present</div>

      <div className = 'SearchTab-container'>
            <div id = "date-range-picker-title">Select Date Range</div>
            <table colSpan='2'>
              <tbody>
              <tr>
                <td><span>From:</span></td>
                <td> <DatePicker
                    className='date-range-picker-input'
                    selected={dates.startDate}
                    onChange={(date) => {
                        onDateChange({ startDate: date });
                      }}                
                    selectsStart
                    startDate={dates.startDat}
                    endDate={dates.endDate}
                    dropdownMode="select"
                /></td>
              </tr>
              <tr>
                <td><span>To: </span></td>
                <td><DatePicker
                    className='date-range-picker-input'
                    selected={dates.endDate}
                    onChange={(date) => {
                        onDateChange({ endDate: date });
                      }}                 
                    selectsEnd
                    startDate={dates.startDate}
                    endDate={dates.endDate}
                    minDate={dates.startDate}
                    dropdownMode="select"
                /></td>
              </tr>
              </tbody>
            </table>

          
            {fromDateValidationError && <div style={{ color: 'red' }}>{fromDateValidationError}</div>}
            {endDateValidationError && <div style={{ color: 'red' }}>{endDateValidationError}</div>}
            {DateValidationError && <div style={{ color: 'red' }}>{DateValidationError}</div>}

      </div>


      <ConditionSelector onConditionChange={setCondition}/>



      {/* <button onClick={handleSubmit}>Submit</button> */}
      
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <button onClick={handleSubmit} className="button-56" role="button">Submit</button>
      </div>
      
      <Legend/>       
      
    </div>
  );
};

export default SearchTab;
