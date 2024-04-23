import React from 'react'

export const Legend = () => {
  return (
    <div className='Legend-container'>
        <span className='Legend-container legend-title'>Classification of Report Values:</span>
        <table>
            <tbody>
                <tr>
                <td><img src="/assets/kb_NotObserved.png" alt="Description 1" /></td>
                <td>Not Observed</td>
                </tr>
                <tr>
                <td><img src="/assets/kb_VeryLow.png" alt="Description 2" /></td>
                <td>Very Low (1 - 10,000 cells/L)</td>
                </tr>
                <tr>
                <td><img src="/assets/kb_Low.png" alt="Description 3" /></td>
                <td>Low (10,000 - 100,000 cells/L)</td>
                </tr>
                <tr>
                <td><img src="/assets/kb_Medium.png" alt="Description 4" /></td>
                <td>Medium (100,000 - 1,000,000 cells/L)</td>
                </tr>
                <tr>
                <td><img src="/assets/kb_High.png" alt="Description 5" /></td>
                <td>High (1,000,000+ cells/L)</td>
                </tr>
            </tbody>
        </table>



    </div>
  )
}
