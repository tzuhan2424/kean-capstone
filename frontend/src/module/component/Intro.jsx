import React from 'react'
import "../css/intro.css"
import { useNavigate } from 'react-router-dom';

export const Intro = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    // Navigate to the path you want the page to go to when the button is clicked
    navigate('/tidetrack');
  };
  return (
    <div className='Intro-main-container'>
        <div className='Intro-title-bar'>
          <span>What is <span id='Intro-TideTrack'>TideTrack</span>?</span>
          <div>
            <button class="button-49" role="button" onClick={handleButtonClick}>Enter</button>

          </div>
        </div>
        
      <div className='Intro-content-container'>
        <p className='Intro-content'>
          This system utilizes an machine learning model to make predictions of HABs in the Gulf of Mexico. 
          In addition it also provides historical instances of HABs in that area. 
          Users can either search by past dates or select an area in the gulf to see predictions up to two days in advance. 
        </p>
      </div>


      <span className='Intro-title'>Information about Project</span>
      <div className='Intro-content-container'>

        <p className='Intro-content'>
          This project was created as part of our Graduate Capstone at Kean University. 
          Our aim is to develop and implement a software system that shows historical information and predictions of Harmful Algae Blooms (HABs) 
          along the US coast of the Gulf of Mexico with a precision rate of at least 80%.
        </p>
      </div>

      <span className='Intro-title'>What is HABs?</span>
      <div className='Intro-content-container'>
        <p className='Intro-content'>
          Harmful Algal Bloom (HABs) of the algae Karenia Brevis, happen seasonally in the Gulf of Mexico under similar circumstances from roughly August to December. 
          This algae releases a neurotoxin into the water it inhabits when it dies, poisoning the ocean life in the area making it unfit for human consumption. 
          This causes these blooms to be particularly damaging, both to people’s health and the economic viability of the areas they occur. 
          We hope that the severity predictions displayed on this system will help people avoid areas where blooms are occurring. 
        </p>
      </div>



      <span className='Intro-title'>Data Extraction</span>
      <div className='Intro-content-container'>
        <p className='Intro-content'>
        Automation is used to extract, transform and load (ETL) data into a centralized database. 
        This is done by running an ETL script periodically via a task scheduler on the web server. 
        The script extracts datasets from the National Oceanic and Atmospheric Administration (NOAA) website using 
        each dataset's respective API or data transfer protocol. 
        The data are then cleaned and transformed into a common format before loading them into the database. 
        </p>
        
      </div>

      <span className='Intro-title'>Resource</span>
      <div className='Intro-content-container'>
        <p className='Intro-content'>
            The datasets are the following:
            <ul>
              <li>
              <a href="https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:0120767" target="_blank" rel="noopener noreferrer">NOAA HABSOS</a>
              </li>
              <li>
              <a href="https://www.ncei.noaa.gov/access/search/data-search/global-marine" target="_blank" rel="noopener noreferrer">NOAA Global Marine dataset collection</a>
              </li>
              <li>
                <a href="https://tidesandcurrents.noaa.gov/ofs/ngofs2/ngofs2.html" target="_blank" rel="noopener noreferrer">NOAA NGOFS2</a>
              </li>
              <li>
                <a href="https://tidesandcurrents.noaa.gov/ofs/tbofs/tbofs.html" target="_blank" rel="noopener noreferrer">NOAA TBOFS</a>
              </li>
              <li>
                <a href="https://tidesandcurrents.noaa.gov/ofs/sjofs/sjofs.html" target="_blank" rel="noopener noreferrer">NOAA SJROFS</a>
              </li>
            </ul>
        </p>
      </div>



      
    </div>
  )
}
