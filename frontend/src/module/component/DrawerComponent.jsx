import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';

import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';

import { NavBar } from '../NavBar';
const drawerWidth = 300;

export default function DrawerComponent({ open, handleDrawerClose, onDateChange, onSubmit, dates, areas, onAreaChange, onPredict, setCondition }) {
  const theme = useTheme();

  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
      variant="persistent"
      anchor="left"
      open={open}
    >
      <div style={{ display: 'flex', alignItems: 'center', padding: theme.spacing(0, 1), ...theme.mixins.toolbar, justifyContent: 'flex-end' }}>
        <IconButton onClick={handleDrawerClose}>
          {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
        </IconButton>
      </div>
      <NavBar 
          onDateChange={onDateChange} 
          onSubmit={onSubmit}
          dates={dates}
          areas={areas}
          onAreaChange={onAreaChange}
          onPredict={onPredict}
          setCondition={setCondition}
      />



     
    </Drawer>
  );
}
