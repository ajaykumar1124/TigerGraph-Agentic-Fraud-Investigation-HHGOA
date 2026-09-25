import { Activity, Search, Bell, Settings, User } from 'lucide-react'

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-left">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Activity size={24} className="gradient-text" />
            <h2 className="navbar-title">Fraud Investigation Command Center</h2>
          </div>
          <p className="navbar-subtitle">Real-time risk intelligence and investigation workflows</p>
        </div>
      </div>
      
      <div className="navbar-right">
        <div className="navbar-search">
          <Search size={18} />
          <input 
            type="text" 
            placeholder="Search cases, transactions..."
            aria-label="Search"
          />
        </div>
        
        <div className="navbar-icons">
          <button className="navbar-icon-btn has-notification" aria-label="Notifications">
            <Bell size={20} />
          </button>
          <button className="navbar-icon-btn" aria-label="Settings">
            <Settings size={20} />
          </button>
        </div>
        
        <div className="navbar-user">
          <div className="navbar-avatar">
            <User size={18} />
          </div>
          <div className="navbar-user-info">
            <div className="navbar-user-name">Fraud Analyst</div>
            <div className="navbar-user-role">Senior Investigator</div>
          </div>
        </div>
      </div>
    </header>
  )
}
