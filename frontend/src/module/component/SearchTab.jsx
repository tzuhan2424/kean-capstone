import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { formatDate } from '../helper/MainAppHelper';
import { passDateCheck,passDateRangeCheck } from '../helper/MainAppHelper';

const SearchTab = ({ onDateChange, onSubmit, dates }) => {

  const [formattedDate, setFormattedDate] = useState({ fromDate: '', toDate: '' });
  const [fromDateValidationError, setFromDateValidationError] = useState(''); 
  const [endDateValidationError, setEndDateValidationError] = useState(''); 
  const [DateValidationError, setDateValidationError] = useState(''); 

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
        <div className = 'date-range-picker'>
            <div>From:</div>
            <DatePicker
                selected={dates.startDate}
                onChange={(date) => {
                    onDateChange({ startDate: date });
                  }}                
                selectsStart
                startDate={dates.startDat}
                endDate={dates.endDate}
                dropdownMode="select"
            />
            {fromDateValidationError && <div style={{ color: 'red' }}>{fromDateValidationError}</div>}

            <div>To: </div>
            <DatePicker
                selected={dates.endDate}
                onChange={(date) => {
                    onDateChange({ endDate: date });
                  }}                 
                selectsEnd
                startDate={dates.startDate}
                endDate={dates.endDate}
                minDate={dates.startDate}
                dropdownMode="select"
            />
            {endDateValidationError && <div style={{ color: 'red' }}>{endDateValidationError}</div>}
            {DateValidationError && <div style={{ color: 'red' }}>{DateValidationError}</div>}

        </div>
        <button onClick={handleSubmit}>Submit</button>

      
    </div>
  );
};

export default SearchTab;
