import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import DashboardPage from './pages/DashboardPage'
import CasesPage from './pages/CasesPage'
import CaseDetailPage from './pages/CaseDetailPage'
import NetworkVisualizationPage from './pages/NetworkVisualizationPage'
import ApprovalsPage from './pages/ApprovalsPage'
import TransactionsPage from './pages/TransactionsPage'
import AnalyticsPage from './pages/AnalyticsPage'
import InvestigationsPage from './pages/InvestigationsPage'
import ReportsPage from './pages/ReportsPage'
import SettingsPage from './pages/SettingsPage'
import NotFoundPage from './pages/NotFoundPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-panel">
          <Navbar />
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/transactions" element={<TransactionsPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/investigations" element={<InvestigationsPage />} />
            <Route path="/investigations/:caseId" element={<CaseDetailPage />} />
            <Route path="/investigations/:caseId/network" element={<NetworkVisualizationPage />} />
            <Route path="/investigations/:caseId/approvals" element={<ApprovalsPage />} />
            <Route path="/cases" element={<CasesPage />} />
            <Route path="/cases/:caseId" element={<CaseDetailPage />} />
            <Route path="/cases/:caseId/network" element={<NetworkVisualizationPage />} />
            <Route path="/cases/:caseId/approvals" element={<ApprovalsPage />} />
            <Route path="/approvals" element={<ApprovalsPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
