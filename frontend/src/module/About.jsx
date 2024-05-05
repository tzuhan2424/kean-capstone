import React from 'react';
import AboutAppBar from '../module/component/AboutAppBar';
import "./css/about.css"

function About() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', // This will vertically center the text and image in the flex container
          justifyContent: 'center', // This will horizontally center the content in the flex container
          padding: '20px', 
          backgroundColor: '#00305C', 
          textAlign: 'center',
          flexDirection:'column'
        }}>
          <span style={{ fontWeight: 'bold', fontSize: '30px', color:'white'}}>TideTrack</span>
        </div>

        <div className='Intro-main-container'>
          <div className='Intro-content-container'>
            <p className='Intro-content'>
            Automation is used to extract, transform and load (ETL) data into a database. 
            This is done by running an ETL script periodically via a task scheduler on the web server. 
            The script extracts datasets from the National Oceanic and Atmospheric Administration (NOAA) website using 
            each dataset’s respective API or data transfer protocol. 
            The data are then cleaned and transformed into a common format before loading them into the database. 
            </p>
            <p className='Intro-content'>
              The datasets are the following:
              NOAA HABSOS: https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:0120767
              NOAA Global Marine dataset collection: https://www.ncei.noaa.gov/access/search/data-search/global-marine
              NOAA NGOFS2: https://tidesandcurrents.noaa.gov/ofs/ngofs2/ngofs2.html
              NOAA TBOFS: https://tidesandcurrents.noaa.gov/ofs/tbofs/tbofs.html
              NOAA SJROFS: https://tidesandcurrents.noaa.gov/ofs/sjofs/sjofs.html

            </p>
          </div>

        </div>

        




    </div>
  );
}

export default About;
