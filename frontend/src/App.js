import React, { useState } from 'react';
import './App.css';
import HardwareTab from './tabs/HardwareTab';
import SoftwareTab from './tabs/SoftwareTab';
import OptionsTab from './tabs/OptionsTab';

function App() {
  const [tab, setTab] = useState('hardware');

  return (
    <div className="App">
      <nav className="App-nav">
        <div className="App-nav-center">
          <button onClick={() => setTab('hardware')} className={tab === 'hardware' ? 'active' : ''}>
            <span className="tab-icon" aria-label="hardware">
              {/* Іконка мікросхеми */}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{verticalAlign: 'middle', marginRight: 8}}>
                <rect x="7" y="7" width="10" height="10" rx="2"/>
                <path d="M3 9v6M21 9v6M9 3h6M9 21h6M3 9h2M3 15h2M19 9h2M19 15h2M9 3v2M15 3v2M9 21v-2M15 21v-2"/>
              </svg>
            </span>
            Hardware
          </button>
          <button onClick={() => setTab('software')} className={tab === 'software' ? 'active' : ''}>
            <span className="tab-icon" aria-label="software">
              {/* Іконка коду */}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{verticalAlign: 'middle', marginRight: 8}}>
                <polyline points="16 18 22 12 16 6" />
                <polyline points="8 6 2 12 8 18" />
              </svg>
            </span>
            Software
          </button>
        </div>
        <button
          className={"App-nav-options" + (tab === 'options' ? ' active' : '')}
          onClick={() => setTab('options')}
          title="Options"
        >
        {/* Іконка шестерні */}
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{verticalAlign: 'middle', marginRight: 6}}>
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.09A1.65 1.65 0 0 0 11 3.09V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h.09a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.09a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
          </svg>
          Options
        </button>
      </nav>
      <div className="App-main-layout">
        <aside className="App-info-panel">
          <div className="info-title">Info</div>
          <div className="info-divider" />
          {/* Тут буде інформація */}
        </aside>
        <main className="App-main-content">
          {tab === 'hardware' && <HardwareTab />}
          {tab === 'software' && <SoftwareTab />}
          {tab === 'options' && <OptionsTab />}
        </main>
        <aside className="App-menu-panel">
          <div className="menu-title">Menu</div>
          <div className="menu-divider" />
          <ul className="menu-list">
            {[1,2,3,4,5,6].map(i => (
              <li key={i} className="menu-item">
                <input type="checkbox" id={`obj${i}`} />
                <label htmlFor={`obj${i}`}>{`Об'єкт ${i}`}</label>
              </li>
            ))}
          </ul>
        </aside>
      </div>
    </div>
  );
}

export default App;
