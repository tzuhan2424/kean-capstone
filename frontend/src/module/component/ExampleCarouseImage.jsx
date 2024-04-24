import React from 'react';

// Assuming you're passing an 'src' prop for the image source and 'text' for alternative text
function ExampleCarouselImage({ src, text }) {
    return <img src={src} alt={text} style={{ width: '100%', height: '600px', objectFit: 'cover' }} />
}
export default ExampleCarouselImage;