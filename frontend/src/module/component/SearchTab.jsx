import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { formatDate } from '../helper/MainAppHelper';
import { passDateCheck } from '../helper/MainAppHelper';

const SearchTab = ({ onDateChange, onSubmit }) => {
  const [fromDate, setFromDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [formattedDate, setFormattedDate] = useState({ fromDate: '', toDate: '' });
  const [fromDateValidationError, setFromDateValidationError] = useState(''); 
  const [endDateValidationError, setEndDateValidationError] = useState(''); 

  useEffect(() => {
    // Assuming `formatDate` returns a string in 'YYYY-MM-DD' format
    const formattedFromDate = fromDate ? formatDate(fromDate) : '';
    const formattedToDate = endDate ? formatDate(endDate) : '';
    setFormattedDate({ fromDate: formattedFromDate, toDate: formattedToDate });
  }, [fromDate, endDate]);



  useEffect(() => {
    // console.log('fromDate', fromDate);
    // Only run validation if fromDate has been set
    if (fromDate) {
      if (formattedDate.fromDate && !passDateCheck(formattedDate.fromDate)) {
        setFromDateValidationError('Invalid start date: 1955-3000');
      } else {
        setFromDateValidationError('');
      }
    }

    // Only run validation if endDate has been set
    if (endDate) {
      if (formattedDate.toDate && !passDateCheck(formattedDate.toDate)) {
        setEndDateValidationError('Invalid end date: 1955-3000');
      } else {
        setEndDateValidationError('');
      }
    }
  }, [formattedDate, fromDate, endDate]);


  // console.log('searchTab from', fromDate);
  // console.log('searchTab end ', endDate);
  // console.log('seach!!',formattedDate );



  const handleSubmit = () => {
    onSubmit(); // Call the passed onSubmit prop function
  };

  return (
    <div>
        <div className = 'date-range-picker'>
            <div>From:</div>
            <DatePicker
                selected={fromDate}
                onChange={(date) => {
                    onDateChange({ startDate: date });
                    setFromDate(date);
                  }}                
                selectsStart
                startDate={fromDate}
                endDate={endDate}
                dropdownMode="select"
            />
            {fromDateValidationError && <div style={{ color: 'red' }}>{fromDateValidationError}</div>}

            <div>To: </div>
            <DatePicker
                selected={endDate}
                onChange={(date) => {
                    onDateChange({ endDate: date });
                    setEndDate(date);
                  }}                 
                selectsEnd
                startDate={fromDate}
                endDate={endDate}
                minDate={fromDate}
                dropdownMode="select"
            />
            {endDateValidationError && <div style={{ color: 'red' }}>{endDateValidationError}</div>}

        </div>
        <button onClick={handleSubmit}>Submit</button>

      
    </div>
  );
};

export default SearchTab;
