import React from 'react'
import "./css/NavBar.css"
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import {a11yProps, CustomTabPanel} from "./helper/NavarHelper";
import SearchTab from './component/SearchTab';
import PredictTab from "./component/PredictTab";
CustomTabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};




const NavBar = ({ onDateChange, onSubmit, dates, areas, onAreaChange, onPredict, setCondition}) => {
  const [value, setValue] = React.useState(0);
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div id='navbar-container'>
        <Box sx={{ width: '100%' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
              <Tab label="Item One" {...a11yProps(0)} />
              <Tab label="Item Two" {...a11yProps(1)} />
            </Tabs>
          </Box>
          <CustomTabPanel value={value} index={0}>
            <SearchTab 
              onDateChange={onDateChange}
              onSubmit = {onSubmit}
              dates = {dates}
              setCondition={setCondition}
            />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={1}>
            <PredictTab
              areas={areas}
              onAreaChange={onAreaChange}
              onPredict = {onPredict}
            />
          </CustomTabPanel>
        </Box>
    </div>
  )
}

export {NavBar};