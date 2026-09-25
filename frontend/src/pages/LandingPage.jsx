import { ArrowRight, ShieldCheck, BrainCircuit, DatabaseZap, ChevronRight, Radar, Workflow, Sparkles, BarChart3, Search, Link2, CheckCircle2 } from 'lucide-react'
import { Link } from 'react-router-dom'

const featureCards = [
  {
    icon: BrainCircuit,
    title: 'Intelligent Routing',
    text: 'LangGraph agents automatically investigate transactions, create cases, and recommend actions based on risk assessment.'
  },
  {
    icon: DatabaseZap,
    title: 'Graph Analytics',
    text: 'Trace money flows, connect accounts, and identify relationships using TigerGraph’s high-performance query engine.'
  },
  {
    icon: Search,
    title: 'Pattern Detection',
    text: 'Detect account takeover, money laundering, synthetic identity, card testing, and merchant fraud with GSQL pattern logic.'
  },
  {
    icon: Workflow,
    title: 'GraphRAG',
    text: 'Retrieve connected evidence, prior cases, policies, and typologies before calling the LLM for context-aware decisions.'
  },
  {
    icon: Radar,
    title: 'Confidence Scoring',
    text: 'Uncertainty engine provides confidence metrics and requests additional evidence when the signal is insufficient.'
  },
  {
    icon: ShieldCheck,
    title: 'Case Memory',
    text: 'Store every investigation, decision, and outcome in TigerGraph for future retrieval and continuous learning.'
  }
]

const architectureSteps = [
  'Setup TigerGraph',
  'Import Dataset',
  'Build GSQL Queries',
  'Expose TigerGraph MCP',
  'Deploy & Monitor'
]

const stackItems = [
  'React Dashboard',
  'FastAPI',
  'LangGraph',
  'GPT-5.1 Mini / Gemini 2.5',
  'TigerGraph Savanna',
  'TigerGraph MCP',
  'GraphRAG + Vector DB',
  'HHGOA IEEE Dataset'
]

const workflowSteps = [
  'Trigger Investigation',
  'Graph Search',
  'Pattern Detection',
  'Risk Assessment',
  'Evidence Gathering',
  'Action Recommendation',
  'Memory Update'
]

const premiumFeatures = [
  'Dynamic confidence meter with adaptive thresholds and uncertainty explanations',
  'Interactive relationship graph with node highlighting and pattern overlays',
  'Case replay mode for historical investigations and model calibration'
]

const timeline = [
  ['Hours 0-3', 'Set up TigerGraph instance and create FraudInvestigation graph'],
  ['Hours 3-6', 'Import HHGOA IEEE dataset and configure data models'],
  ['Hours 6-9', 'Build GSQL queries for relationship discovery'],
  ['Hours 9-12', 'Install TigerGraph MCP and create LangGraph workflow'],
  ['Hours 12-18', 'Build GraphRAG integration and dashboard components'],
  ['Hours 18-24', 'Create mock APIs, record demo, and publish to GitHub']
]

export default function LandingPage() {
  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="brand-row">
          <div className="brand-mark">FG</div>
          <span>FraudGuard AI</span>
        </div>
        <nav className="landing-nav">
          <a href="#features">Features</a>
          <a href="#architecture">Architecture</a>
          <a href="#workflow">Workflow</a>
          <a href="#timeline">Timeline</a>
        </nav>
        <div className="landing-actions">
          <Link to="/cases" className="secondary-btn">View Dashboard</Link>
          <Link to="/investigations" className="primary-btn">Start Investigation</Link>
        </div>
      </header>

      <main className="landing-main">
        <section className="hero-section">
          <div className="hero-copy">
            <span className="eyebrow">Next-Generation Fraud Detection</span>
            <h1>Fraud Detection with AI & Graph Intelligence</h1>
            <p>
              Harness the power of TigerGraph’s agentic AI to investigate suspicious transactions,
              detect fraud patterns, and protect your customers in real time.
            </p>
            <div className="hero-actions">
              <Link to="/investigations" className="primary-btn large">Start Investigation <ArrowRight size={18} /></Link>
              <a href="#features" className="secondary-btn large">View Documentation</a>
            </div>
            <div className="hero-metrics">
              <div>
                <strong>95%</strong>
                <span>Detection Accuracy</span>
              </div>
              <div>
                <strong>5</strong>
                <span>Fraud Pattern Types</span>
              </div>
              <div>
                <strong>Real-Time</strong>
                <span>Investigation Speed</span>
              </div>
              <div>
                <strong>GraphRAG</strong>
                <span>Evidence Retrieval</span>
              </div>
            </div>
          </div>

          <div className="hero-panel">
            <div className="score-card premium">
              <div className="score-row">
                <span className="mini-label">Current Risk</span>
                <span className="risk-pill">High</span>
              </div>
              <div className="score-value">92%</div>
              <div className="confidence-bar">
                <span style={{ width: '92%' }} />
              </div>
              <div className="score-meta">
                <span>Confidence</span>
                <strong>95%</strong>
              </div>
            </div>

            <div className="mini-grid">
              <div className="mini-card">
                <ShieldCheck size={18} />
                <span>Account Takeover</span>
              </div>
              <div className="mini-card">
                <Link2 size={18} />
                <span>Money Laundering</span>
              </div>
              <div className="mini-card">
                <BarChart3 size={18} />
                <span>Card Testing</span>
              </div>
              <div className="mini-card">
                <Sparkles size={18} />
                <span>Synthetic Identity</span>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="feature-section">
          <div className="section-head">
            <span className="eyebrow">Powerful Features</span>
            <h2>Comprehensive fraud detection and investigation capabilities</h2>
          </div>

          <div className="feature-grid">
            {featureCards.map(({ icon: Icon, title, text }) => (
              <article key={title} className="feature-card">
                <div className="feature-icon"><Icon size={22} /></div>
                <h3>{title}</h3>
                <p>{text}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="architecture" className="architecture-section">
          <div className="section-head narrow">
            <span className="eyebrow">System Architecture</span>
            <h2>End-to-end AI-powered fraud investigation platform</h2>
          </div>

          <div className="architecture-box">
            <div className="architecture-labels">
              <span>React Dashboard</span>
              <ChevronRight size={15} />
              <span>LangGraph Agent</span>
              <ChevronRight size={15} />
              <span>TigerGraph MCP</span>
              <ChevronRight size={15} />
              <span>TigerGraph</span>
            </div>
            <p>
              Transactions, Accounts, Devices, Cases, Memory with GraphRAG and mock banking APIs.
            </p>
          </div>

          <div className="step-grid">
            {architectureSteps.map((step, index) => (
              <div key={step} className="step-item">
                <span className="step-number">{index + 1}</span>
                <strong>{step}</strong>
              </div>
            ))}
          </div>
        </section>

        <section className="stack-section">
          <div className="section-head narrow">
            <span className="eyebrow">Technology Stack</span>
            <h2>Built with cutting-edge AI and graph database technologies</h2>
          </div>

          <div className="stack-grid">
            {stackItems.map(item => (
              <div key={item} className="stack-pill">{item}</div>
            ))}
          </div>
        </section>

        <section id="workflow" className="workflow-section">
          <div className="section-head narrow">
            <span className="eyebrow">Investigation Workflow</span>
            <h2>Automated end-to-end fraud investigation process</h2>
          </div>

          <div className="workflow-list">
            {workflowSteps.map((step, index) => (
              <div key={step} className="workflow-item">
                <span className="workflow-index">0{index + 1}</span>
                <div>
                  <strong>{step}</strong>
                  <p>{index === 0 && 'Suspicious transaction detected and flagged for investigation.'}</p>
                  <p>{index === 1 && 'Query TigerGraph for related accounts, transactions, and devices.'}</p>
                  <p>{index === 2 && 'Analyze signal against fraud typologies and GSQL patterns.'}</p>
                  <p>{index === 3 && 'Calculate fraud probability and confidence scores.'}</p>
                  <p>{index === 4 && 'Request more evidence when confidence falls below threshold.'}</p>
                  <p>{index === 5 && 'Recommend an action such as freeze, OTP, monitor, or escalate.'}</p>
                  <p>{index === 6 && 'Write investigation results back to TigerGraph for future reference.'}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="preview-section">
          <div className="section-head narrow">
            <span className="eyebrow">Interactive Dashboard</span>
            <h2>Real-time fraud investigation management</h2>
          </div>

          <div className="dashboard-preview">
            <div className="preview-card large">
              <div className="preview-header">
                <span className="mini-label">Risk Score Display</span>
                <span className="risk-pill danger">Critical</span>
              </div>
              <div className="preview-score">92%</div>
              <div className="confidence-bar"><span style={{ width: '92%' }} /></div>
            </div>

            <div className="preview-card">
              <div className="mini-label">Relationship Graph</div>
              <div className="graph-node-layout">
                <span className="node primary">Customer</span>
                <span className="node secondary">Device</span>
                <span className="node danger">Txn</span>
              </div>
            </div>

            <div className="preview-card">
              <div className="mini-label">Evidence Panel</div>
              <ul className="evidence-list">
                <li><CheckCircle2 size={14} /> Device mismatch detected</li>
                <li><CheckCircle2 size={14} /> Velocity anomaly</li>
                <li><CheckCircle2 size={14} /> Known fraud pattern</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="premium-section">
          <div className="section-head narrow">
            <span className="eyebrow">Premium Features</span>
            <h2>What makes FraudGuard AI stand out</h2>
          </div>

          <div className="premium-grid">
            {premiumFeatures.map((feature) => (
              <div key={feature} className="premium-item">
                <CheckCircle2 size={18} />
                <span>{feature}</span>
              </div>
            ))}
          </div>
        </section>

        <section id="timeline" className="timeline-section">
          <div className="section-head narrow">
            <span className="eyebrow">Implementation Timeline</span>
            <h2>Complete setup in 24 hours</h2>
          </div>

          <div className="timeline-grid">
            {timeline.map(([time, item]) => (
              <div key={time} className="timeline-item-card">
                <span className="time-badge">{time}</span>
                <p>{item}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}
