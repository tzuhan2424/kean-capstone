import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import '../css/FloatingActionButton.css'; // Ensure the CSS is imported

function FloatingActionButton() {
    const [isOpen, setIsOpen] = useState(false);
    const navigate = useNavigate();
    const handleAction1Click = () => {
        navigate('/');
    };


    return (
        <div className="fab-container">
            <button className="fab-main-button" onClick={() => setIsOpen(!isOpen)}>
                {/* {isOpen ? '×' : '+'} */}
                <img src="/favicon.ico" alt="Menu" style={{ width: '100%', height: '100%' }} />
            </button>
            <div className={`fab-item ${isOpen ? 'fab-item-visible' : ''}`} style={{ '--i': 1 }} onClick={handleAction1Click}>
                <img src='/assets/homepage.svg' style={{}}></img>
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
