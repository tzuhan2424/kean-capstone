import React, { useState } from 'react';
import '../css/FloatingActionButton.css'; // Ensure the CSS is imported

function FloatingActionButton() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="fab-container">
            <button className="fab-main-button" onClick={() => setIsOpen(!isOpen)}>
                {/* {isOpen ? '×' : '+'} */}
                <img src="/favicon.ico" alt="Menu" style={{ width: '100%', height: '100%' }} />
            </button>
            <div className={`fab-item ${isOpen ? 'fab-item-visible' : ''}`} style={{ '--i': 1 }}>
                Action 1
            </div>
            <div className={`fab-item ${isOpen ? 'fab-item-visible' : ''}`} style={{ '--i': 2 }}>
                Action 2
            </div>
            <div className={`fab-item ${isOpen ? 'fab-item-visible' : ''}`} style={{ '--i': 3 }}>
                Action 3
            </div>
        </div>
    );
}

export default FloatingActionButton;
