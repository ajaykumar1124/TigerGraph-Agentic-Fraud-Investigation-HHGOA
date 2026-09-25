import { useState } from 'react';
import { Save, Bell, Shield, Database, Users, Sliders, Eye, EyeOff } from 'lucide-react';
import '../styles/banking.css';

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [showApiKey, setShowApiKey] = useState(false);

  const [settings, setSettings] = useState({
    // General Settings
    systemName: 'TigerGraph Agentic Fraud Investigation',
    timezone: 'Asia/Kolkata',
    language: 'en',
    dateFormat: 'DD/MM/YYYY',
    
    // Notifications
    emailNotifications: true,
    criticalAlerts: true,
    dailySummary: true,
    weeklyReport: false,
    
    // Fraud Detection
    criticalThreshold: 80,
    highThreshold: 60,
    mediumThreshold: 40,
    autoBlockCritical: false,
    requireApprovalAmount: 50000,
    
    // Security
    sessionTimeout: 30,
    mfaEnabled: true,
    passwordExpiry: 90,
    apiKey: 'tg_xxxxxxxxxxxxxxxxxxxxxxxxxx',
    
    // Database
    tigergraphHost: 'https://tigergraph.example.com',
    tigergraphPort: 9000,
    graphName: 'FraudGraph',
    autoBackup: true
  });

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    alert('Settings saved successfully!');
  };

  const tabs = [
    { id: 'general', name: 'General', icon: <Sliders size={18} /> },
    { id: 'notifications', name: 'Notifications', icon: <Bell size={18} /> },
    { id: 'fraud-detection', name: 'Fraud Detection', icon: <Shield size={18} /> },
    { id: 'security', name: 'Security', icon: <Shield size={18} /> },
    { id: 'database', name: 'Database', icon: <Database size={18} /> },
    { id: 'users', name: 'Users & Roles', icon: <Users size={18} /> }
  ];

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px', color: 'white' }}>
          System Settings
        </h1>
        <p style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
          Configure fraud detection system preferences and parameters
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '250px 1fr', gap: '24px' }}>
        {/* Sidebar Tabs */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '12px',
          padding: '16px',
          height: 'fit-content'
        }}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                width: '100%',
                padding: '12px 16px',
                background: activeTab === tab.id ? 'rgba(102, 126, 234, 0.2)' : 'transparent',
                border: activeTab === tab.id ? '1px solid #667eea' : '1px solid transparent',
                borderRadius: '8px',
                color: activeTab === tab.id ? '#667eea' : 'rgba(255, 255, 255, 0.7)',
                fontSize: '14px',
                fontWeight: activeTab === tab.id ? '600' : '400',
                cursor: 'pointer',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                transition: 'all 0.2s'
              }}
            >
              {tab.icon}
              {tab.name}
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '12px',
          padding: '32px'
        }}>
          {/* General Settings */}
          {activeTab === 'general' && (
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '24px', color: 'white' }}>
                General Settings
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <div>
                  <label htmlFor="systemName" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    System Name
                  </label>
                  <input
                    id="systemName"
                    name="systemName"
                    type="text"
                    value={settings.systemName}
                    onChange={(e) => handleSettingChange('systemName', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      fontSize: '14px'
                    }}
                  />
                </div>

                <div>
                  <label htmlFor="timezone" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    Timezone
                  </label>
                  <select
                    id="timezone"
                    name="timezone"
                    value={settings.timezone}
                    onChange={(e) => handleSettingChange('timezone', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      fontSize: '14px'
                    }}
                  >
                    <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                    <option value="America/New_York">America/New_York (EST)</option>
                    <option value="Europe/London">Europe/London (GMT)</option>
                    <option value="Asia/Singapore">Asia/Singapore (SGT)</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="dateFormat" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    Date Format
                  </label>
                  <select
                    id="dateFormat"
                    name="dateFormat"
                    value={settings.dateFormat}
                    onChange={(e) => handleSettingChange('dateFormat', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      fontSize: '14px'
                    }}
                  >
                    <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                    <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                    <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Notifications */}
          {activeTab === 'notifications' && (
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '24px', color: 'white' }}>
                Notification Preferences
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {[
                  { key: 'emailNotifications', label: 'Email Notifications', desc: 'Receive email notifications for system events' },
                  { key: 'criticalAlerts', label: 'Critical Alerts', desc: 'Immediate notifications for critical fraud cases' },
                  { key: 'dailySummary', label: 'Daily Summary', desc: 'Daily summary report of fraud activity' },
                  { key: 'weeklyReport', label: 'Weekly Report', desc: 'Comprehensive weekly analytics report' }
                ].map((item) => (
                  <div key={item.key} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '16px',
                    background: 'rgba(0, 0, 0, 0.2)',
                    borderRadius: '8px'
                  }}>
                    <div>
                      <div style={{ fontWeight: '500', marginBottom: '4px' }}>{item.label}</div>
                      <div style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)' }}>{item.desc}</div>
                    </div>
                    <label htmlFor={item.key} style={{ position: 'relative', display: 'inline-block', width: '50px', height: '26px' }}>
                      <input
                        id={item.key}
                        name={item.key}
                        type="checkbox"
                        checked={settings[item.key]}
                        onChange={(e) => handleSettingChange(item.key, e.target.checked)}
                        style={{ opacity: 0, width: 0, height: 0 }}
                      />
                      <span style={{
                        position: 'absolute',
                        cursor: 'pointer',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: settings[item.key] ? '#667eea' : 'rgba(255, 255, 255, 0.2)',
                        borderRadius: '26px',
                        transition: '0.3s'
                      }}>
                        <span style={{
                          position: 'absolute',
                          content: '',
                          height: '20px',
                          width: '20px',
                          left: settings[item.key] ? '27px' : '3px',
                          bottom: '3px',
                          background: 'white',
                          borderRadius: '50%',
                          transition: '0.3s'
                        }} />
                      </span>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Fraud Detection */}
          {activeTab === 'fraud-detection' && (
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '24px', color: 'white' }}>
                Fraud Detection Parameters
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <div>
                  <label htmlFor="criticalThreshold" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    Critical Risk Threshold: {settings.criticalThreshold}%
                  </label>
                  <input
                    id="criticalThreshold"
                    name="criticalThreshold"
                    type="range"
                    min="70"
                    max="100"
                    value={settings.criticalThreshold}
                    onChange={(e) => handleSettingChange('criticalThreshold', parseInt(e.target.value))}
                    style={{ width: '100%' }}
                  />
                  <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', marginTop: '4px' }}>
                    Transactions above this threshold are flagged as critical
                  </div>
                </div>

                <div>
                  <label htmlFor="highThreshold" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    High Risk Threshold: {settings.highThreshold}%
                  </label>
                  <input
                    id="highThreshold"
                    name="highThreshold"
                    type="range"
                    min="50"
                    max="80"
                    value={settings.highThreshold}
                    onChange={(e) => handleSettingChange('highThreshold', parseInt(e.target.value))}
                    style={{ width: '100%' }}
                  />
                </div>

                <div>
                  <label htmlFor="mediumThreshold" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    Medium Risk Threshold: {settings.mediumThreshold}%
                  </label>
                  <input
                    id="mediumThreshold"
                    name="mediumThreshold"
                    type="range"
                    min="30"
                    max="60"
                    value={settings.mediumThreshold}
                    onChange={(e) => handleSettingChange('mediumThreshold', parseInt(e.target.value))}
                    style={{ width: '100%' }}
                  />
                </div>

                <div>
                  <label htmlFor="requireApprovalAmount" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    Auto-block Amount Threshold (₹)
                  </label>
                  <input
                    id="requireApprovalAmount"
                    name="requireApprovalAmount"
                    type="number"
                    value={settings.requireApprovalAmount}
                    onChange={(e) => handleSettingChange('requireApprovalAmount', parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      fontSize: '14px'
                    }}
                  />
                  <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.5)', marginTop: '4px' }}>
                    Transactions above this amount require manual approval
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Security */}
          {activeTab === 'security' && (
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '24px', color: 'white' }}>
                Security Settings
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <div>
                  <label htmlFor="sessionTimeout" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    Session Timeout (minutes)
                  </label>
                  <input
                    id="sessionTimeout"
                    name="sessionTimeout"
                    type="number"
                    value={settings.sessionTimeout}
                    onChange={(e) => handleSettingChange('sessionTimeout', parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      fontSize: '14px'
                    }}
                  />
                </div>

                <div style={{
                  padding: '16px',
                  background: 'rgba(0, 0, 0, 0.2)',
                  borderRadius: '8px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <div>
                    <div style={{ fontWeight: '500', marginBottom: '4px' }}>Two-Factor Authentication</div>
                    <div style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.6)' }}>
                      Require 2FA for all users
                    </div>
                  </div>
                  <label htmlFor="mfaEnabled" style={{ position: 'relative', display: 'inline-block', width: '50px', height: '26px' }}>
                    <input
                      id="mfaEnabled"
                      name="mfaEnabled"
                      type="checkbox"
                      checked={settings.mfaEnabled}
                      onChange={(e) => handleSettingChange('mfaEnabled', e.target.checked)}
                      style={{ opacity: 0, width: 0, height: 0 }}
                    />
                    <span style={{
                      position: 'absolute',
                      cursor: 'pointer',
                      top: 0,
                      left: 0,
                      right: 0,
                      bottom: 0,
                      background: settings.mfaEnabled ? '#667eea' : 'rgba(255, 255, 255, 0.2)',
                      borderRadius: '26px'
                    }}>
                      <span style={{
                        position: 'absolute',
                        height: '20px',
                        width: '20px',
                        left: settings.mfaEnabled ? '27px' : '3px',
                        bottom: '3px',
                        background: 'white',
                        borderRadius: '50%',
                        transition: '0.3s'
                      }} />
                    </span>
                  </label>
                </div>

                <div>
                  <label htmlFor="apiKey" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    API Key
                  </label>
                  <div style={{ position: 'relative' }}>
                    <input
                      id="apiKey"
                      name="apiKey"
                      type={showApiKey ? 'text' : 'password'}
                      value={settings.apiKey}
                      readOnly
                      style={{
                        width: '100%',
                        padding: '12px',
                        paddingRight: '48px',
                        background: 'rgba(255, 255, 255, 0.1)',
                        border: '1px solid rgba(255, 255, 255, 0.2)',
                        borderRadius: '8px',
                        color: 'white',
                        fontSize: '14px'
                      }}
                    />
                    <button
                      onClick={() => setShowApiKey(!showApiKey)}
                      style={{
                        position: 'absolute',
                        right: '12px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        background: 'none',
                        border: 'none',
                        color: 'rgba(255, 255, 255, 0.6)',
                        cursor: 'pointer'
                      }}
                    >
                      {showApiKey ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  <button
                    className="action-button"
                    style={{ marginTop: '12px', padding: '8px 16px', fontSize: '13px', background: 'rgba(255, 71, 87, 0.2)', color: '#ff4757' }}
                    onClick={() => alert('API key regenerated successfully!')}
                  >
                    Regenerate API Key
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Database */}
          {activeTab === 'database' && (
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '24px', color: 'white' }}>
                Database Configuration
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <div>
                  <label htmlFor="tigergraphHost" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    TigerGraph Host
                  </label>
                  <input
                    id="tigergraphHost"
                    name="tigergraphHost"
                    type="text"
                    value={settings.tigergraphHost}
                    onChange={(e) => handleSettingChange('tigergraphHost', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      fontSize: '14px'
                    }}
                  />
                </div>

                <div>
                  <label htmlFor="graphName" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
                    Graph Name
                  </label>
                  <input
                    id="graphName"
                    name="graphName"
                    type="text"
                    value={settings.graphName}
                    onChange={(e) => handleSettingChange('graphName', e.target.value)}
                    style={{
                      width: '100%',
                      padding: '12px',
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white',
                      fontSize: '14px'
                    }}
                  />
                </div>

                <div style={{
                  padding: '16px',
                  background: 'rgba(38, 222, 129, 0.1)',
                  border: '1px solid rgba(38, 222, 129, 0.3)',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px'
                }}>
                  <Shield size={24} color="#26de81" />
                  <div>
                    <div style={{ fontWeight: '500', color: '#26de81', marginBottom: '4px' }}>
                      Connection Status: Active
                    </div>
                    <div style={{ fontSize: '13px', color: 'rgba(255, 255, 255, 0.7)' }}>
                      Last connected: 2 minutes ago
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '12px' }}>
                  <button className="action-button primary">
                    Test Connection
                  </button>
                  <button className="action-button" style={{ background: 'rgba(255, 255, 255, 0.1)' }}>
                    Backup Database
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Users */}
          {activeTab === 'users' && (
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '24px', color: 'white' }}>
                Users & Roles
              </h2>

              <div style={{
                padding: '60px 20px',
                textAlign: 'center',
                background: 'rgba(0, 0, 0, 0.2)',
                borderRadius: '8px',
                color: 'rgba(255, 255, 255, 0.6)'
              }}>
                <Users size={48} style={{ marginBottom: '16px', opacity: 0.3 }} />
                <p>User management feature coming soon</p>
              </div>
            </div>
          )}

          {/* Save Button */}
          <div style={{
            marginTop: '32px',
            paddingTop: '24px',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '12px'
          }}>
            <button
              className="action-button"
              style={{ background: 'rgba(255, 255, 255, 0.1)' }}
              onClick={() => alert('Changes discarded')}
            >
              Cancel
            </button>
            <button
              className="action-button primary"
              onClick={handleSave}
            >
              <Save size={16} style={{ marginRight: '8px' }} />
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
