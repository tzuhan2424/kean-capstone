import React from 'react'
import CarouselFade from './component/Carousel'
import { Intro } from './component/Intro'

export const Welcome = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* <div style={{ flex: 0, padding: '20px', backgroundColor: '#4da1fba8', textAlign: 'center' }}> */}
      <div style={{ 
          display: 'flex', 
          alignItems: 'center', // This will vertically center the text and image in the flex container
          justifyContent: 'center', // This will horizontally center the content in the flex container
          padding: '20px', 
          backgroundColor: '#4da1fba8', 
          textAlign: 'center',
          flexDirection:'column'
        }}>
          <span style={{ fontWeight: 'bold', fontSize: '30px'}}>TideTrack</span>
          {/* <img src="/favicon.ico" alt="Descriptive text" style={{ maxHeight: '100px' }} /> Set a max height for your image */}
        </div>
      <div>
        <CarouselFade />
      </div>

      <div>
        <Intro/>
      </div>

    </div>
  )
}
