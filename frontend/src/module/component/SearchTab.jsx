import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const SearchTab = ({ onDateChange, onSubmit }) => {
  const [fromDate, setFromDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  
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
        </div>
        <button onClick={handleSubmit}>Submit</button>

      
    </div>
  );
};

export default SearchTab;
