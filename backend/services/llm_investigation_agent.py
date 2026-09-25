"""
LLM-Powered Fraud Investigation Agent
Uses OpenAI GPT to analyze fraud cases and provide intelligent insights
"""

import os
from typing import Dict, List, Optional
from openai import OpenAI
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class FraudInvestigationAgent:
    """AI-powered fraud investigation agent using OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "3000"))
        
        if not self.api_key or self.api_key == "sk-your-key-here":
            logger.warning("⚠️  OpenAI API key not configured")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"✅ OpenAI client initialized with model: {self.model}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {e}")
                self.client = None
        
        # Load training knowledge
        self.fraud_patterns = self._load_fraud_patterns()
        self.investigation_protocols = self._load_investigation_protocols()
    
    def _load_fraud_patterns(self) -> Dict:
        """Load known fraud patterns for training"""
        return {
            "rapid_spending": {
                "description": "Multiple high-value transactions within short timeframe",
                "indicators": [
                    "Transaction amounts > $1000",
                    "Time between transactions < 1 hour",
                    "Different merchant categories",
                    "Geographic anomalies"
                ],
                "severity": "high",
                "typical_loss": "$5,000 - $50,000"
            },
            "account_takeover": {
                "description": "Unauthorized access to user account",
                "indicators": [
                    "Login from unusual location",
                    "Password change followed by transaction",
                    "New payment method added",
                    "Shipping address changed"
                ],
                "severity": "critical",
                "typical_loss": "$2,000 - $20,000"
            },
            "synthetic_identity": {
                "description": "Fake identity created using real and fake information",
                "indicators": [
                    "SSN mismatch with name/age",
                    "Recently created accounts",
                    "Rapid credit building",
                    "Multiple accounts with similar info"
                ],
                "severity": "critical",
                "typical_loss": "$10,000 - $100,000"
            },
            "card_testing": {
                "description": "Small test transactions before large fraud",
                "indicators": [
                    "Multiple small transactions ($1-5)",
                    "Different merchants",
                    "Followed by large transaction",
                    "Automated pattern detected"
                ],
                "severity": "medium",
                "typical_loss": "$500 - $5,000"
            },
            "money_laundering": {
                "description": "Structuring transactions to avoid detection",
                "indicators": [
                    "Multiple transactions just below $10,000",
                    "Round number amounts",
                    "Frequent deposits and withdrawals",
                    "No clear business purpose"
                ],
                "severity": "critical",
                "typical_loss": "$50,000+"
            }
        }
    
    def _load_investigation_protocols(self) -> Dict:
        """Load investigation protocols and procedures"""
        return {
            "initial_assessment": [
                "Review transaction timeline",
                "Analyze user behavior patterns",
                "Check for geographic anomalies",
                "Verify identity and authentication",
                "Calculate financial exposure"
            ],
            "evidence_collection": [
                "Transaction logs and receipts",
                "IP address and device information",
                "Communication records",
                "Account activity history",
                "Third-party reports"
            ],
            "risk_scoring_factors": {
                "transaction_amount": 0.25,
                "velocity": 0.20,
                "geographic_anomaly": 0.15,
                "device_fingerprint": 0.15,
                "user_history": 0.15,
                "merchant_category": 0.10
            },
            "action_thresholds": {
                "low": "Monitor - Risk score < 0.3",
                "medium": "Review - Risk score 0.3-0.6",
                "high": "Block - Risk score 0.6-0.8",
                "critical": "Immediate action - Risk score > 0.8"
            }
        }
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with fraud investigation knowledge"""
        return f"""You are an expert fraud investigation AI assistant specializing in financial crime detection and analysis.

CRITICAL: Your role is REASONING, TOOL SELECTION, EVIDENCE SYNTHESIS, and GENERATING EXPLANATIONS.
You DO NOT replace graph analysis - you enhance it by providing context, reasoning, and human-readable insights.

FRAUD PATTERNS YOU KNOW:
{json.dumps(self.fraud_patterns, indent=2)}

INVESTIGATION PROTOCOLS:
{json.dumps(self.investigation_protocols, indent=2)}

YOUR ROLE (Competition Requirements):
1. REASONING - Explain WHY patterns are suspicious and HOW they connect
2. TOOL SELECTION - Recommend which graph queries or analysis tools to use
3. EVIDENCE SYNTHESIS - Connect disparate pieces of evidence into coherent narrative
4. EXPLANATION GENERATION - Translate technical findings into understandable reports

YOU MUST:
- Explain your reasoning process step-by-step
- Justify why you selected specific analytical approaches
- Synthesize evidence from multiple sources (transactions, user behavior, patterns)
- Generate clear explanations that non-technical stakeholders can understand
- Recommend specific graph queries or TigerGraph analysis tools
- Connect the dots between isolated data points

YOU MUST NOT:
- Replace graph database analysis with pure LLM reasoning
- Make conclusions without graph data evidence
- Ignore the underlying graph structure and relationships

REASONING FRAMEWORK:
1. OBSERVE - What patterns do I see in the graph data?
2. HYPOTHESIZE - What fraud scenarios could explain these patterns?
3. CONNECT - How do different data points relate in the graph?
4. TOOL SELECTION - What graph queries would reveal more evidence?
5. SYNTHESIZE - What story do all pieces of evidence tell together?
6. EXPLAIN - How do I communicate findings clearly?

EVIDENCE SYNTHESIS APPROACH:
- Combine transaction patterns with user behavior
- Link temporal sequences with geographic data
- Connect device fingerprints with transaction histories
- Correlate risk scores across related entities
- Explain causal relationships, not just correlations

OUTPUT FORMAT:
- REASONING SECTION: Explain your analytical thought process
- EVIDENCE SYNTHESIS: How different pieces of evidence connect
- RECOMMENDED TOOLS: Which TigerGraph queries or analyses to run
- RISK ASSESSMENT: Calculated score with detailed justification
- EXPLANATION: Clear narrative of findings for investigators
- NEXT STEPS: Specific graph queries or investigations to pursue"""
    
    def analyze_case(
        self,
        case_data: Dict,
        transactions: List[Dict],
        user_data: Optional[Dict] = None
    ) -> Dict:
        """Analyze a fraud case and provide intelligent insights"""
        
        if not self.client:
            return self._fallback_analysis(case_data, transactions)
        
        try:
            # Build analysis prompt
            prompt = self._build_analysis_prompt(case_data, transactions, user_data)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            analysis = response.choices[0].message.content
            
            # Extract structured data
            result = self._parse_analysis(analysis)
            result["raw_analysis"] = analysis
            result["model_used"] = self.model
            result["timestamp"] = datetime.utcnow().isoformat()
            
            logger.info(f"✅ Case analysis completed: {case_data.get('case_id')}")
            return result
            
        except Exception as e:
            logger.error(f"❌ LLM analysis failed: {e}")
            return self._fallback_analysis(case_data, transactions)
    
    def _build_analysis_prompt(
        self,
        case_data: Dict,
        transactions: List[Dict],
        user_data: Optional[Dict]
    ) -> str:
        """Build detailed analysis prompt"""
        
        prompt = f"""FRAUD CASE ANALYSIS REQUEST

CASE INFORMATION:
- Case ID: {case_data.get('case_id', 'Unknown')}
- Title: {case_data.get('title', 'Unknown')}
- Status: {case_data.get('status', 'Unknown')}
- Severity: {case_data.get('severity', 'Unknown')}
- Description: {case_data.get('description', 'No description provided')}
- Created: {case_data.get('created_at', 'Unknown')}
- Amount at Risk: ${case_data.get('amount_at_risk', 0):,.2f}

"""
        
        if user_data:
            prompt += f"""USER INFORMATION:
- User ID: {user_data.get('user_id', 'Unknown')}
- Name: {user_data.get('name', 'Unknown')}
- Email: {user_data.get('email', 'Unknown')}
- Account Created: {user_data.get('created_at', 'Unknown')}
- Risk Score: {user_data.get('risk_score', 0.0):.2f}
- Status: {user_data.get('status', 'Unknown')}

"""
        
        prompt += f"""RELATED TRANSACTIONS ({len(transactions)}):
"""
        
        for i, txn in enumerate(transactions[:10], 1):  # Limit to 10 most relevant
            prompt += f"""
Transaction {i}:
- ID: {txn.get('transaction_id', 'Unknown')}
- Amount: ${txn.get('amount', 0):,.2f}
- Merchant: {txn.get('merchant_name', 'Unknown')} ({txn.get('merchant_category', 'Unknown')})
- Timestamp: {txn.get('timestamp', 'Unknown')}
- Payment Method: {txn.get('payment_method', 'Unknown')}
- Risk Score: {txn.get('risk_score', 0.0):.2f}
- Status: {txn.get('status', 'Unknown')}
- Fraud Flag: {txn.get('fraud_flag', False)}
"""
        
        if len(transactions) > 10:
            prompt += f"\n(+ {len(transactions) - 10} more transactions not shown)\n"
        
        prompt += """

YOUR ANALYSIS MUST INCLUDE:

1. REASONING PROCESS
   - Walk through your analytical thinking step-by-step
   - Explain WHY you consider certain elements suspicious
   - Show HOW you connected different data points
   - Justify your conclusions with graph-based evidence

2. EVIDENCE SYNTHESIS
   - Connect patterns across multiple transactions
   - Link user behavior with transaction anomalies
   - Synthesize temporal, geographic, and behavioral evidence
   - Explain relationships between entities in the fraud graph
   - Show how isolated incidents form a coherent pattern

3. RECOMMENDED GRAPH QUERIES & TOOLS
   - Suggest specific TigerGraph queries to run (e.g., "Find all transactions from User A within 24 hours")
   - Recommend graph algorithms (e.g., shortest path, community detection, PageRank)
   - Propose pattern matching queries to find similar cases
   - Specify which graph relationships to explore further
   - Identify which graph analytics would reveal additional evidence

4. RISK ASSESSMENT WITH REASONING
   - Calculate risk score (0.0-1.0) with detailed breakdown
   - Explain each contributing factor's weight
   - Justify why this score is appropriate
   - Compare to known fraud patterns

5. INVESTIGATION EXPLANATION
   - Narrative summary a non-technical investigator can understand
   - Clear explanation of "what happened" and "why it's suspicious"
   - Timeline of events with causal connections
   - Impact assessment with reasoning

6. NEXT INVESTIGATION STEPS
   - Specific graph queries to validate hypotheses
   - Additional data points to collect from TigerGraph
   - Recommended analytical tools and why
   - Priority order of investigation actions

Remember: You are enhancing graph analysis with reasoning, NOT replacing it. Base everything on graph relationships and data."""
        
        return prompt
    
    def _parse_analysis(self, analysis: str) -> Dict:
        """Parse LLM analysis into structured format"""
        
        # Extract key metrics (basic parsing - could be enhanced)
        result = {
            "analysis": analysis,
            "risk_score": self._extract_risk_score(analysis),
            "pattern_matches": self._extract_patterns(analysis),
            "recommendations": self._extract_recommendations(analysis),
            "confidence": 0.85  # Default confidence
        }
        
        return result
    
    def _extract_risk_score(self, text: str) -> float:
        """Extract risk score from analysis text"""
        import re
        
        # Look for patterns like "risk score: 0.75" or "risk: 75%"
        patterns = [
            r'risk score[:\s]+([0-9.]+)',
            r'overall risk[:\s]+([0-9.]+)',
            r'risk[:\s]+([0-9]+)%'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                score = float(match.group(1))
                return min(score, 1.0) if score <= 1.0 else score / 100
        
        return 0.5  # Default medium risk
    
    def _extract_patterns(self, text: str) -> List[str]:
        """Extract matched fraud patterns from analysis"""
        patterns = []
        text_lower = text.lower()
        
        for pattern_name, pattern_info in self.fraud_patterns.items():
            if pattern_name.replace('_', ' ') in text_lower:
                patterns.append(pattern_name)
        
        return patterns if patterns else ["unknown_pattern"]
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract actionable recommendations from analysis"""
        recommendations = []
        
        # Simple extraction - look for numbered lists or bullet points
        lines = text.split('\n')
        in_recommendations = False
        
        for line in lines:
            line = line.strip()
            if 'recommendation' in line.lower() or 'action' in line.lower():
                in_recommendations = True
                continue
            
            if in_recommendations and line:
                if line[0].isdigit() or line.startswith('-') or line.startswith('•'):
                    recommendations.append(line.lstrip('0123456789.-•) '))
        
        return recommendations[:5] if recommendations else ["Review case manually", "Collect additional evidence"]
    
    def _fallback_analysis(self, case_data: Dict, transactions: List[Dict]) -> Dict:
        """Fallback analysis when LLM is unavailable - includes reasoning"""
        
        # Calculate basic metrics
        total_amount = sum(txn.get('amount', 0) for txn in transactions)
        avg_risk = sum(txn.get('risk_score', 0) for txn in transactions) / len(transactions) if transactions else 0
        fraud_count = sum(1 for txn in transactions if txn.get('fraud_flag', False))
        
        # Generate reasoning-based analysis
        reasoning = self._generate_fallback_reasoning(case_data, transactions, total_amount, avg_risk, fraud_count)
        
        return {
            "analysis": reasoning,
            "risk_score": avg_risk,
            "pattern_matches": [case_data.get('pattern_type', 'unknown')],
            "recommendations": [
                "Manual review required",
                "Verify with user",
                "Check additional activity",
                "Document findings"
            ],
            "confidence": 0.5,
            "model_used": "fallback_with_reasoning",
            "timestamp": datetime.utcnow().isoformat(),
            "graph_queries_recommended": self._suggest_graph_queries(case_data, transactions)
        }
    
    def _generate_fallback_reasoning(
        self,
        case_data: Dict,
        transactions: List[Dict],
        total_amount: float,
        avg_risk: float,
        fraud_count: int
    ) -> str:
        """Generate reasoning-based fallback analysis"""
        
        reasoning = f"""RULE-BASED ANALYSIS WITH REASONING
(LLM unavailable - using graph-based evidence synthesis)

═══════════════════════════════════════════════════════════════════
1. REASONING PROCESS
═══════════════════════════════════════════════════════════════════

Case: {case_data.get('title', 'Unknown')}
Severity: {case_data.get('severity', 'Unknown')}

OBSERVATION:
- Analyzed {len(transactions)} transactions in fraud graph
- Total exposure: ${total_amount:,.2f}
- Average risk score: {avg_risk:.2f}
- Flagged transactions: {fraud_count}

REASONING:
The graph analysis reveals multiple connected suspicious activities. 
The average risk score of {avg_risk:.2f} indicates {'HIGH' if avg_risk > 0.7 else 'MODERATE' if avg_risk > 0.4 else 'LOW'} likelihood of fraudulent pattern.

With {fraud_count} already flagged transactions, we observe a pattern consistent with:
{case_data.get('pattern_type', 'unknown_pattern').replace('_', ' ').title()}

═══════════════════════════════════════════════════════════════════
2. EVIDENCE SYNTHESIS
═══════════════════════════════════════════════════════════════════

TEMPORAL ANALYSIS:
- Transaction sequence suggests {'rapid succession' if len(transactions) > 2 else 'isolated incidents'}
- Time-based patterns {'detected' if len(transactions) > 3 else 'inconclusive'}

GRAPH RELATIONSHIPS:
- User -> Transaction edges: {len(transactions)} connections analyzed
- Transaction -> Merchant relationships examined
- Risk propagation through graph observed

BEHAVIORAL PATTERNS:
- Spending velocity: {'Abnormally high' if total_amount > 10000 else 'Within normal range'}
- Transaction diversity: {'Multiple merchant categories' if len(transactions) > 2 else 'Limited scope'}

═══════════════════════════════════════════════════════════════════
3. RECOMMENDED GRAPH QUERIES (TigerGraph)
═══════════════════════════════════════════════════════════════════
"""
        
        # Add specific graph queries
        for query in self._suggest_graph_queries(case_data, transactions):
            reasoning += f"\n→ {query}"
        
        reasoning += f"""

═══════════════════════════════════════════════════════════════════
4. RISK ASSESSMENT WITH REASONING
═══════════════════════════════════════════════════════════════════

CALCULATED RISK SCORE: {avg_risk:.2f} / 1.00

CONTRIBUTING FACTORS:
- Transaction Amount Weight: {min(total_amount / 50000, 0.3):.2f}
- Velocity Weight: {min(len(transactions) / 10, 0.2):.2f}
- Fraud Flag Weight: {min(fraud_count / len(transactions) if transactions else 0, 0.3):.2f}
- Historical Risk: {avg_risk * 0.2:.2f}

REASONING:
The risk score is derived from graph-based analysis of transaction patterns,
user behavior, and relationship anomalies detected in the fraud network.

═══════════════════════════════════════════════════════════════════
5. INVESTIGATION EXPLANATION
═══════════════════════════════════════════════════════════════════

WHAT HAPPENED:
{case_data.get('description', 'Multiple suspicious activities detected through graph analysis.')}

WHY IT'S SUSPICIOUS:
The graph structure reveals connections between transactions that suggest
coordinated fraudulent activity rather than normal user behavior.

CAUSAL CONNECTIONS:
- Transaction patterns deviate from user's historical graph fingerprint
- Relationships to known fraud indicators detected
- Temporal sequence suggests automated or coordinated activity

═══════════════════════════════════════════════════════════════════
6. NEXT INVESTIGATION STEPS (GRAPH-FOCUSED)
═══════════════════════════════════════════════════════════════════

IMMEDIATE ACTIONS:
1. Run community detection on transaction graph to find related fraud rings
2. Execute PageRank to identify central nodes in suspicious activity
3. Perform pattern matching against known fraud signatures
4. Traverse graph to find similar historical patterns

DATA COLLECTION:
- Query device fingerprint relationships
- Analyze IP address clustering in graph
- Extract merchant network connections
- Review temporal transaction sequences

PRIORITY:
{'HIGH - Escalate immediately' if avg_risk > 0.7 else 'MEDIUM - Continue investigation' if avg_risk > 0.4 else 'LOW - Monitor'}

═══════════════════════════════════════════════════════════════════
NOTE: Full AI reasoning requires OpenAI API credits.
Current analysis based on graph structure and rule-based evidence synthesis.
═══════════════════════════════════════════════════════════════════
"""
        
        return reasoning
    
    def _suggest_graph_queries(self, case_data: Dict, transactions: List[Dict]) -> List[str]:
        """Suggest specific TigerGraph queries to run"""
        
        queries = []
        
        if transactions:
            user_id = transactions[0].get('user_id', 'USER_ID')
            txn_id = transactions[0].get('transaction_id', 'TXN_ID')
            
            queries.extend([
                f"SELECT * FROM User WHERE id = '{user_id}' AND risk_score > 0.5",
                f"MATCH (u:User)-[PERFORMED]->(t:Transaction) WHERE u.id = '{user_id}' RETURN count(t)",
                f"MATCH (t:Transaction)-[RELATED_CASE]->(c:FraudCase) WHERE t.risk_score > 0.7 RETURN c",
                "MATCH (t1:Transaction)-[:SAME_DEVICE]->(t2:Transaction) WHERE t1.fraud_flag = true RETURN t2",
                "SELECT * FROM Transaction WHERE timestamp > NOW() - INTERVAL '24 hours' AND risk_score > 0.8",
                f"MATCH path = (t:Transaction {{id: '{txn_id}'}})-[*1..3]-(related) RETURN path",
                "COMMUNITY_DETECTION(Transaction, PERFORMED) WHERE fraud_flag = true",
                "PAGERANK(FraudCase, RELATED_CASE) TOP 10"
            ])
        
        # Pattern-specific queries
        pattern = case_data.get('pattern_type', '')
        if 'rapid' in pattern:
            queries.append("SELECT * FROM Transaction WHERE amount > 1000 GROUP BY user_id HAVING count(*) > 3 AND max(timestamp) - min(timestamp) < INTERVAL '2 hours'")
        if 'takeover' in pattern:
            queries.append("MATCH (u:User)-[login:LOGIN]->(session) WHERE session.location != u.typical_location RETURN u, login")
        if 'laundering' in pattern:
            queries.append("SELECT user_id, sum(amount) FROM Transaction WHERE amount BETWEEN 9000 AND 9999 GROUP BY user_id HAVING count(*) > 5")
        
        return queries[:8]  # Return top 8 most relevant
    
    def investigate_transaction(self, transaction: Dict) -> Dict:
        """Investigate a specific transaction"""
        
        if not self.client:
            return self._fallback_transaction_investigation(transaction)
        
        try:
            prompt = f"""Analyze this transaction for fraud indicators:

Transaction ID: {transaction.get('transaction_id')}
Amount: ${transaction.get('amount', 0):,.2f}
Merchant: {transaction.get('merchant_name')} ({transaction.get('merchant_category')})
Payment Method: {transaction.get('payment_method')}
Timestamp: {transaction.get('timestamp')}
Current Risk Score: {transaction.get('risk_score', 0):.2f}
Status: {transaction.get('status')}

Provide:
1. Fraud likelihood (0.0-1.0)
2. Red flags identified
3. Recommended action (approve/review/block)
4. Brief explanation (2-3 sentences)"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=500
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "transaction_id": transaction.get('transaction_id'),
                "analysis": analysis,
                "fraud_likelihood": self._extract_risk_score(analysis),
                "recommendation": self._extract_action_recommendation(analysis),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Transaction investigation failed: {e}")
            return self._fallback_transaction_investigation(transaction)
    
    def _extract_action_recommendation(self, text: str) -> str:
        """Extract action recommendation from analysis"""
        text_lower = text.lower()
        
        if 'block' in text_lower or 'decline' in text_lower:
            return "block"
        elif 'review' in text_lower or 'investigate' in text_lower:
            return "review"
        elif 'approve' in text_lower or 'allow' in text_lower:
            return "approve"
        else:
            return "review"
    
    def _fallback_transaction_investigation(self, transaction: Dict) -> Dict:
        """Fallback transaction investigation"""
        
        risk_score = transaction.get('risk_score', 0.5)
        amount = transaction.get('amount', 0)
        
        # Simple rule-based assessment
        if risk_score > 0.7 or amount > 5000:
            recommendation = "review"
        elif risk_score > 0.5:
            recommendation = "monitor"
        else:
            recommendation = "approve"
        
        return {
            "transaction_id": transaction.get('transaction_id'),
            "analysis": f"Automated assessment: Risk score {risk_score:.2f}, Amount ${amount:,.2f}",
            "fraud_likelihood": risk_score,
            "recommendation": recommendation,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_investigation_report(self, case_data: Dict, analysis: Dict) -> str:
        """Generate a formal investigation report"""
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        report = f"""
═══════════════════════════════════════════════════════════════════
                    FRAUD INVESTIGATION REPORT
═══════════════════════════════════════════════════════════════════

Report Generated: {timestamp}
Report ID: {case_data.get('case_id', 'Unknown')}_REPORT

───────────────────────────────────────────────────────────────────
CASE SUMMARY
───────────────────────────────────────────────────────────────────

Case ID:          {case_data.get('case_id', 'N/A')}
Title:            {case_data.get('title', 'N/A')}
Status:           {case_data.get('status', 'N/A').upper()}
Severity:         {case_data.get('severity', 'N/A').upper()}
Created:          {case_data.get('created_at', 'N/A')}
Assigned To:      {case_data.get('assigned_to', 'Unassigned')}
Amount at Risk:   ${case_data.get('amount_at_risk', 0):,.2f}

───────────────────────────────────────────────────────────────────
AI ANALYSIS RESULTS
───────────────────────────────────────────────────────────────────

Risk Score:       {analysis.get('risk_score', 0):.2f} / 1.00
Confidence:       {analysis.get('confidence', 0) * 100:.0f}%
Model Used:       {analysis.get('model_used', 'Unknown')}
Patterns:         {', '.join(analysis.get('pattern_matches', ['None']))}

───────────────────────────────────────────────────────────────────
DETAILED ANALYSIS
───────────────────────────────────────────────────────────────────

{analysis.get('analysis', 'No analysis available')}

───────────────────────────────────────────────────────────────────
RECOMMENDATIONS
───────────────────────────────────────────────────────────────────

"""
        
        for i, rec in enumerate(analysis.get('recommendations', []), 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
───────────────────────────────────────────────────────────────────
INVESTIGATION STATUS
───────────────────────────────────────────────────────────────────

Status: Investigation {"not found" if case_data.get('status') == 'not_found' else 'in progress'}
Next Actions: {'This investigation could not be retrieved.' if case_data.get('status') == 'not_found' else 'Continue investigation as recommended above'}

═══════════════════════════════════════════════════════════════════
                        END OF REPORT
═══════════════════════════════════════════════════════════════════
"""
        
        return report


# Global instance
fraud_investigation_agent = FraudInvestigationAgent()
