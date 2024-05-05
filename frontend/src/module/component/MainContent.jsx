import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import MapComponent from '../MapComponent';

import { drawerWidth } from '../config/drawerConfig'; // Update the path accordingly

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: 0, // Set padding to 0 to remove it
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    marginTop:'60px',
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
      marginTop:'60px',

    }),
  }),
);
// points={results} 
//         area={selectedArea} 
//         isPredict={isPredict}
export default function MainContent({ open, points,area, isPredict  }) {
    const theme = useTheme();  // This line gets the theme from MUI

  return (
    <Main open={open}>
      {/* <div style={{ ...theme.mixins.toolbar}} /> */}
      {/* <div style={{ minHeight: '100px' }} /> */}
      <MapComponent 
          points={points} 
          area={area} 
          isPredict={isPredict}/>
    </Main>
  );
}
