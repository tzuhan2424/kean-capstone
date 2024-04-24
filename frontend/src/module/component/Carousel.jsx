import Carousel from 'react-bootstrap/Carousel';
import { useState } from 'react';

import ExampleCarouselImage from '../component/ExampleCarouseImage'
import 'bootstrap/dist/css/bootstrap.min.css';
import { badgeClasses } from '@mui/material';

function CarouselFade() {

    const [index, setIndex] = useState(0);

    const handleSelect = (selectedIndex) => {
        setIndex(selectedIndex);
    };
  return (
    <Carousel activeIndex={index} onSelect={handleSelect}>
        <Carousel.Item>
        <ExampleCarouselImage src="/assets/rt1.jpg" text="First slide" />
            <Carousel.Caption>
            <div style={{backgroundColor:"black"}}>
                <h3>What is a red tide?</h3>
                <p>A "red tide" is a common term used for a harmful algal bloom</p>
            </div>
            </Carousel.Caption>
        </Carousel.Item>      
        <Carousel.Item>
            <ExampleCarouselImage src="/assets/rt2.jpg" text="First slide" />
            <Carousel.Caption>
            <h3>Karenia brevis</h3>
            <p>found in the Gulf of Mexico along the west coast of Florida</p>
            </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
            <ExampleCarouselImage src="/assets/rt3.jpg" text="First slide" />
            <Carousel.Caption>
            <h3>How Are Red Tides Harmful?</h3>
            <p>
                Red tide algae make potent natural toxins. It is unknown why these toxins are created, but some can be hazardous to larger organisms through the processes of biomagnification and bioaccumulation.
            </p>
            </Carousel.Caption>
        </Carousel.Item>


    </Carousel>
  );
}

export default CarouselFade;