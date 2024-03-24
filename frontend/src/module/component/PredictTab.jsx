import React from 'react'

const PredictTab = ({areas, onAreaChange }) => {
  return (  
    <div>
        {areas.map(area => (
            <div key={area.name}>
                <input
                    type="radio"
                    id={area.name}
                    name="area"
                    value={area.name}
                    onChange={onAreaChange}
                />
                <label htmlFor={area.name}>{area.name}</label>
            </div>
        ))}

        <button>Predict</button>

    </div>
  )
}

export default PredictTab