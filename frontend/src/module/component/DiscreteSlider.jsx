import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';


export default function DiscreteSlider({ intensity, setIntensity }) {
    const handleChange = (event, newValue) => {
        setIntensity(newValue);
    };

  return (
    <Box>
        <Slider
            aria-label="Intensity"
            value={intensity} 
            onChange={handleChange}
            step={10000}
            min={0}
            max={1000000}
            valueLabelDisplay="on"  // Display the value label on the slider thumb
            valueLabelFormat={value => `Cell Counts >= ${value}`}
        />
    </Box>
  );
}
