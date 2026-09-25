export default function StatCard({ title, value, tone = 'neutral' }) {
  return (
    <div className={`stat-card ${tone}`}>
      <div className="stat-title">{title}</div>
      <div className="stat-value">{value}</div>
    </div>
  )
}
