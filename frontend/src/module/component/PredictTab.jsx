import React from 'react'
import "../css/NavBar.css"
const PredictTab = ({areas, onAreaChange, onPredict}) => {
  return (  
    <div>
        <div>Forecast System</div>
        <span id = 'area-picker-title'>Select Area:</span>
        <div className='PredictTab-container'>

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
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <button onClick={onPredict} className="button-56" role="button">Forecast</button>
        </div>
    </div>
  )
}

export default PredictTab