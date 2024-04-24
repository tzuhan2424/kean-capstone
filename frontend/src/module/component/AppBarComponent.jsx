import * as React from 'react';
import { styled } from '@mui/material/styles';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import Box from '@mui/material/Box';
import '../css/NavBar.css'
import { drawerWidth } from '../config/drawerConfig'; // Update the path accordingly


const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

export default function AppBarComponent({ open, handleDrawerOpen }) {
  return (
    <AppBar position="fixed" open={open} >
      <Toolbar sx={{
        display: 'flex',      // Ensures flexbox layout
        alignItems: 'center', // Aligns items vertically at the center
        justifyContent: 'flex-start', // Adjusts items to start of the toolbar
        backgroundColor: '#5B96CB'
      }}>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          onClick={handleDrawerOpen}
          edge="start"
          sx={{ mr: 2, ...(open && { display: 'none' }) }}
        >
          <MenuIcon />
        </IconButton>

        <Box sx={{
          display: 'flex',
          alignItems: 'center',
          flexGrow: 1, // Allows box to take up remaining space
          ml: 2 // Gives some margin left for spacing after the icon
          }}>
          <img src="/assets/KU_Logo.svg.png" alt="Kean University Logo" className="appBarLogo" />
          <Typography variant="h6" noWrap component="div" className="AppBarHeader">
            TideTrack System
          </Typography>

        </Box>
      </Toolbar>
    </AppBar>
  );
}
