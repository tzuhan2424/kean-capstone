import React from 'react'
import { NavBar } from "./NavBar";
import { Map } from "./Map";
import "./css/app.css"

const MainApp = () => {
  return (
    <div className='main-app-container'>
        <NavBar/>
        <Map/>
    </div>
  )
}

export default MainApp