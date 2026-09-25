import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  FolderOpen,
  Shield,
  CheckCircle,
  BarChart3,
  Settings,
  Zap,
  CreditCard,
  TrendingUp,
} from 'lucide-react'

const menu = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Transactions', path: '/transactions', icon: CreditCard },
  { name: 'Analytics', path: '/analytics', icon: TrendingUp },
  { name: 'Cases', path: '/cases', icon: FolderOpen },
  { name: 'Investigations', path: '/investigations', icon: Shield },
  { name: 'Approvals', path: '/approvals', icon: CheckCircle },
  { name: 'Reports', path: '/reports', icon: BarChart3 },
  { name: 'Settings', path: '/settings', icon: Settings },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <Zap size={20} />
        <span>TigerGraph HHGOA</span>
      </div>
      <nav>
        {menu.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}
            >
              <Icon size={20} strokeWidth={1.5} />
              <span>{item.name}</span>
            </NavLink>
          )
        })}
      </nav>
    </aside>
  )
}
