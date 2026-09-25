import axios from 'axios'

const API = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Health
export const getHealth = () => API.get('/health')

// Cases (now using investigations endpoints)
export const getCases = () => API.get('/api/v1/investigations')
export const getCase = (caseId) => API.get(`/api/v1/investigations/${caseId}`)
export const createCase = (payload) => API.post('/api/v1/investigations/start', payload)

// Investigations (correct endpoints)
export const listInvestigations = () => API.get('/api/v1/investigations')
export const getInvestigation = (caseId) => API.get(`/api/v1/investigations/${caseId}`)
export const getInvestigationDetails = (caseId) => API.get(`/api/v1/investigations/${caseId}/details`)
export const startInvestigation = (payload) => API.post('/api/v1/investigations/start', payload)
export const runInvestigation = (caseId) => API.post(`/api/v1/investigations/${caseId}/run`)
export const getRecommendation = (caseId) => API.get(`/api/v1/investigations/${caseId}/recommendation`)
export const recordOutcome = (caseId, payload) => 
  API.post(`/api/v1/investigations/${caseId}/outcome`, payload)
export const submitAdditionalEvidence = (caseId, payload) => 
  API.post(`/api/v1/investigations/${caseId}/outcome`, payload)
export const getMetrics = () => API.get('/api/v1/investigations/analytics/metrics')

export default API
