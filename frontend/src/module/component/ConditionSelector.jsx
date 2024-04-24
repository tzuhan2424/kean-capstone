import React, { useState, useEffect } from 'react';
import DiscreteSlider from './DiscreteSlider'; // Assuming DiscreteSlider is in the same directory
import "../css/NavBar.css"
const ConditionSelector = ({onConditionChange}) => {
    const [category, setCategory] = useState('');
    const [intensity, setIntensity] = useState(null);
    const [selectionType, setSelectionType] = useState('dropdown');

    // console.log('category', category);
    // console.log('intensity', intensity);

    useEffect(() => {
        const data = {
            category,
            intensity,
        };
        onConditionChange(data);
    }, [category, intensity]);



    const handleSelectionTypeChange = (type) => {
        setSelectionType(type);
        if (type === 'dropdown') {
            setIntensity(null); // Reset intensity when switching to dropdown
        } else {
            setCategory(''); // Reset category when switching to slider
        }
    };


    return (
        <div className="SearchTab-container Intensity-container">
            <React.Fragment>
                <div id = 'intensity-picker-title'>Intensity selector</div>
                <input
                    type="radio"
                    id="dropdown"
                    name="selectorType"
                    value="dropdown"
                    checked={selectionType === 'dropdown'}
                    onChange={() => handleSelectionTypeChange('dropdown')}
                />
                <label htmlFor="dropdown">Category</label>

                <input
                    type="radio"
                    id="slider"
                    name="selectorType"
                    value="slider"
                    checked={selectionType === 'slider'}
                    onChange={() => handleSelectionTypeChange('slider')}
                />
                <label htmlFor="slider">Cell Count</label>
            </React.Fragment>

            {selectionType === 'dropdown' && (
                <select className="custom-select-dropdown" value={category} onChange={(e) => setCategory(e.target.value)}>
                    <option value="">Select Category</option>
                    <option value="all">All</option>
                    <option value="high">High(High (1,000,000+ cells/L))</option>
                    <option value="medium">Medium(100,000 - 1,000,000 cells/L)</option>
                    <option value="low">Low(10,000 - 100,000 cells/L)</option>
                    <option value="very low">Very Low(1 - 10,000 cells/L)</option>
                    <option value="not observed">Not Observed</option>
                </select>
            )}

            {selectionType === 'slider' && (
                <DiscreteSlider
                    intensity={intensity}
                    setIntensity={setIntensity}
                />
            )}
        </div>
    );
};

export default ConditionSelector;
