import React from 'react'

const PredictTab = ({areas, onAreaChange, onPredict}) => {
  return (  
    <div>
        <div>Forecast System</div>
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

        <button onClick={onPredict}>Predict</button>

    </div>
  )
}

export default PredictTab