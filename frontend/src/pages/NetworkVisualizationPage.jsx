import { useEffect, useState, useCallback, useMemo } from 'react'
import { useParams } from 'react-router-dom'
import ReactFlow, {
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { getInvestigation } from '../services/api'
import { Users, Smartphone, Wifi, CreditCard, Building2 } from 'lucide-react'

export default function NetworkVisualizationPage() {
  const { caseId } = useParams()
  const [investigation, setInvestigation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  useEffect(() => {
    async function loadCase() {
      try {
        const response = await getInvestigation(caseId)
        setInvestigation(response.data)
      } catch (err) {
        console.error('Error loading investigation:', err)
        setError('Could not load network visualization data.')
      } finally {
        setLoading(false)
      }
    }

    loadCase()
  }, [caseId])

  // Build graph from investigation data
  useEffect(() => {
    if (!investigation) return

    const newNodes = []
    const newEdges = []
    const nodeMap = new Map()
    let nodeId = 0

    // Helper to create unique node ID and track it
    const addNode = (label, type, data = {}) => {
      const id = `${type}-${nodeId++}`
      nodeMap.set(label, id)
      
      const nodeTypes = {
        customer: { bg: 'rgba(39, 193, 125, 0.2)', icon: '👤', color: '#27c17d' },
        account: { bg: 'rgba(79, 149, 255, 0.2)', icon: '💳', color: '#4f95ff' },
        device: { bg: 'rgba(249, 184, 79, 0.2)', icon: '📱', color: '#f9b84f' },
        ip: { bg: 'rgba(192, 132, 252, 0.2)', icon: '🌐', color: '#c084fc' },
        merchant: { bg: 'rgba(255, 107, 107, 0.2)', icon: '🏪', color: '#ff6b6b' },
        transaction: { bg: 'rgba(148, 163, 184, 0.2)', icon: '💰', color: '#94a3b8' },
      }

      const typeConfig = nodeTypes[type] || nodeTypes.transaction

      newNodes.push({
        id,
        data: {
          label: (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
              <span style={{ fontSize: '20px' }}>{typeConfig.icon}</span>
              <span style={{ fontSize: '11px', maxWidth: '80px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {label}
              </span>
            </div>
          ),
        },
        position: { x: Math.random() * 400, y: Math.random() * 400 },
        style: {
          background: typeConfig.bg,
          border: `2px solid ${typeConfig.color}`,
          borderRadius: '8px',
          padding: '10px',
          width: '100px',
          height: '100px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#e5eefb',
          fontSize: '12px',
          textAlign: 'center',
          fontWeight: '500',
        },
      })

      return id
    }

    // Add primary fraud network entities explicitly
    const customerId = addNode(investigation.customer_id || 'Customer', 'customer')
    const deviceId = addNode(investigation.device_id || 'DEV-1045', 'device')
    const ipId = addNode(investigation.ip_address || '203.0.113.44', 'ip')
    const merchantId = addNode(investigation.merchant || 'Northwind Market', 'merchant')
    const txnId = addNode(investigation.transaction_id || 'TXN-2026-001', 'transaction')
    const accountId = addNode(investigation.account_id || 'ACC-456221', 'account')

    newEdges.push(
      { id: `edge-${customerId}-${deviceId}`, source: customerId, target: deviceId, animated: true, label: 'Uses device', style: { stroke: '#4f95ff' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#4f95ff' } },
      { id: `edge-${customerId}-${ipId}`, source: customerId, target: ipId, animated: true, label: 'Logs in from', style: { stroke: '#c084fc' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#c084fc' } },
      { id: `edge-${customerId}-${merchantId}`, source: customerId, target: merchantId, label: 'Purchases at', style: { stroke: '#ff6b6b' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ff6b6b' } },
      { id: `edge-${customerId}-${txnId}`, source: customerId, target: txnId, label: 'Initiates', style: { stroke: '#94a3b8' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#94a3b8' } },
      { id: `edge-${accountId}-${customerId}`, source: accountId, target: customerId, label: 'Has account', style: { stroke: '#27c17d' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#27c17d' } },
      { id: `edge-${txnId}-${merchantId}`, source: txnId, target: merchantId, label: 'Merchant checkout', style: { stroke: '#f9b84f' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f9b84f' } }
    )

    if (investigation.evidence && Array.isArray(investigation.evidence)) {
      investigation.evidence.forEach((evidence) => {
        if (typeof evidence === 'string' && evidence.includes('VELOCITY')) {
          const patternId = addNode(investigation.suspected_fraud_pattern || 'Velocity anomaly', 'transaction')
          newEdges.push({
            id: `edge-pattern-${customerId}`,
            source: customerId,
            target: patternId,
            label: 'Matches pattern',
            animated: true,
            style: { stroke: '#ff6b6b', strokeWidth: 3 },
            markerEnd: { type: MarkerType.ArrowClosed, color: '#ff6b6b' },
          })
        }
      })
    }

    setNodes(newNodes)
    setEdges(newEdges)
  }, [investigation, setNodes, setEdges])

  if (loading) return <section className="page-panel"><h3>Loading network visualization…</h3></section>
  if (error) return <section className="page-panel error-panel"><h3>Error</h3><p>{error}</p></section>
  if (!investigation) return null

  return (
    <div className="network-container">
      <div className="network-header">
        <div>
          <p className="eyebrow">Fraud network analysis</p>
          <h2>Case {investigation.case_id}</h2>
        </div>
        <div className="legend">
          <div className="legend-item">
            <span className="legend-icon customer">👤</span>
            <span>Customer</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon device">📱</span>
            <span>Device</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon ip">🌐</span>
            <span>IP Address</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon merchant">🏪</span>
            <span>Merchant</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon transaction">💰</span>
            <span>Transaction</span>
          </div>
        </div>
      </div>
      <div className="network-graph-wrap">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          minZoom={0.3}
          maxZoom={1.4}
          defaultEdgeOptions={{ animated: true }}
          style={{ width: '100%', height: '100%', background: '#0b1220' }}
        >
          <Background color="#94a3b8" gap={20} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  )
}
