import React, { useEffect,useState } from 'react';
import Calendar from 'react-calendar'

import './css/calendar.css';
import 'react-calendar/dist/Calendar.css'


const CalendarComponent = () => {
    // TODO: dynamic min and max date
    const minDate = new Date(1990, 1, 1)
    const maxDate = new Date(2024, 2, 25)

    // TODO: Propagate onChange event to re-fetch points from server
    return (
        <div id="calendar-app-content">
            <div id="calendar-container" style={{height: '100%', width: '100%'}}>
                <Calendar minDate={minDate} maxDate={maxDate} minDetail="decade" selectRange="true"/>
            </div>
        </div>
    );
};

export default CalendarComponent;
