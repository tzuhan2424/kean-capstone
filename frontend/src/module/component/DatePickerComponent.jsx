// DatePickerComponent.js
import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const DatePickerComponent = ({ onDateChange }) => {
  // Handler for date change specifically for this DatePicker
  const handleChange = (dates) => {
    const [start, end] = dates;
    onDateChange(start, end); // This calls the handler in MainApp
  };

  return (
    <DatePicker
      onChange={handleChange}
      selectsRange={true}
      startDate={null} // You might want to control these from MainApp as well
      endDate={null}
      inline
    />
  );
};

export default DatePickerComponent;
