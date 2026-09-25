# TigerGraph GSQL Queries for Fraud Investigation

## Overview

This directory contains GSQL queries for the fraud investigation agent. These queries analyze the knowledge graph to uncover fraud patterns, identify suspicious relationships, and gather evidence for investigation decisions.

## Queries

### 1. find_shared_devices.gsql
**Purpose:** Identify customers who share devices (potential fraud network)

**Parameters:**
- `customer_id` (STRING): Customer to investigate
- `device_threshold` (INT): Minimum number of customers to flag (default: 1)

**Returns:**
- List of connected customers
- Device IDs and types
- Transaction counts per customer
- Risk assessment

**Example:**
```
find_shared_devices("C000001", 2)
```

**Use Case:**
- When a new device is detected on an account
- To discover coordinated fraud accounts
- To identify device recycling patterns

---

### 2. find_shared_ips.gsql
**Purpose:** Identify customers who share IP addresses

**Parameters:**
- `customer_id` (STRING): Customer to investigate
- `ip_threshold` (INT): Minimum number of customers per IP (default: 1)

**Returns:**
- List of connected customers
- IP addresses used
- Customer count per IP
- Risk classification (HIGH/MEDIUM/LOW)

**Example:**
```
find_shared_ips("C000001", 3)
```

**Use Case:**
- Detecting multiple accounts from same geolocation
- Identifying datacenter/proxy usage
- Finding mule accounts operated from same location

---

### 3. detect_transaction_velocity.gsql
**Purpose:** Detect unusual transaction patterns and velocity anomalies

**Parameters:**
- `customer_id` (STRING): Customer to analyze
- `time_window_minutes` (INT): Look-back window (default: 60)

**Returns:**
- Transaction count in window
- Total and average amount
- Maximum transaction amount
- Number of unique merchants
- Velocity anomaly score (0.0-1.0)
- Risk level classification

**Example:**
```
detect_transaction_velocity("C000001", 120)
```

**Anomaly Scoring:**
- +0.3: > 10 transactions in window
- +0.2: Average amount > $500
- +0.3: > 5 unique merchants
- +0.2: Single transaction > $10,000

**Use Case:**
- Identifying rapid-fire transaction patterns
- Detecting unusual spending sprees
- Finding account takeover indicators

---

### 4. find_fraud_network.gsql
**Purpose:** Identify connected fraud networks around a customer

**Parameters:**
- `customer_id` (STRING): Starting point
- `max_hops` (INT): Degree of separation (default: 2)

**Returns:**
- All customers in network
- Centrality scores (node importance)
- Risk ranking (CRITICAL/HIGH/MEDIUM/LOW)
- Connected devices, IPs, merchants

**Example:**
```
find_fraud_network("C000001", 2)
```

**Centrality Scoring:**
- Count of connected devices (0-40 possible)
- Count of connected IPs (0-40 possible)
- Count of transactions (0-unlimited)

**Risk Ranking:**
- CRITICAL: Centrality > 50
- HIGH: Centrality > 20
- MEDIUM: Centrality > 5
- LOW: Centrality ≤ 5

**Use Case:**
- Discovering coordinated fraud rings
- Finding mule accounts
- Identifying account takeover networks

---

### 5. find_similar_historical_cases.gsql
**Purpose:** Find past fraud cases with similar characteristics

**Parameters:**
- `fraud_pattern` (STRING): Fraud type (ACCOUNT_TAKEOVER, PAYMENT_FRAUD, CARD_FRAUD, FRAUD_NETWORK, VELOCITY_ANOMALY)
- `min_risk` (DOUBLE): Minimum risk score (default: 0.5)
- `max_risk` (DOUBLE): Maximum risk score (default: 1.0)

**Returns:**
- Similar closed cases (up to 5)
- Similarity score for each case
- Outcome of each case (CONFIRMED_FRAUD, FALSE_POSITIVE, PENDING)
- Recommended actions from similar cases
- Evidence collected in similar cases

**Example:**
```
find_similar_historical_cases("ACCOUNT_TAKEOVER", 0.7, 0.95)
```

**Similarity Scoring:**
- +0.2: Pattern matches exactly
- -0.1 per 0.1 difference in risk score
- Max score: 1.0

**Use Case:**
- Finding precedent cases for decision support
- Learning from past investigation outcomes
- Building case memory and institutional knowledge

---

### 6. get_investigation_context.gsql
**Purpose:** Retrieve comprehensive context for a fraud case

**Parameters:**
- `case_id` (STRING): Case to investigate

**Returns:**
- Complete case details
- All related transactions
- Customer information
- Devices and IPs used
- Merchants involved
- Fraud patterns matched
- Collected evidence
- Recommended actions
- Related/similar cases

**Example:**
```
get_investigation_context("CASE000001")
```

**Output Structure:**
```json
{
  "case_details": {
    "case_id": "CASE000001",
    "customer_id": "C000001",
    "case_status": "OPEN",
    "fraud_pattern_detected": "ACCOUNT_TAKEOVER",
    "initial_risk_score": 0.82,
    "current_risk_score": 0.87,
    "confidence_score": 0.65
  },
  "transactions": [...],
  "customers": [...],
  "devices": [...],
  "ips": [...],
  "merchants": [...],
  "patterns": [...],
  "evidence": [...],
  "actions": [...],
  "related_cases": [...]
}
```

**Use Case:**
- Populating the investigation UI with full context
- Agent gathering evidence for decision-making
- Analyst review of complete case file

---

## Integration with Agent

### Query Execution Flow

```
Agent Investigation Loop:
    ↓
Trigger received (high-risk transaction, case opened)
    ↓
get_investigation_context(case_id)
    ↓
Execute parallel queries:
    - find_shared_devices(customer_id)
    - find_shared_ips(customer_id)
    - detect_transaction_velocity(customer_id)
    - find_fraud_network(customer_id)
    - find_similar_historical_cases(fraud_pattern)
    ↓
Aggregate results
    ↓
Calculate evidence confidence
    ↓
Update risk score
    ↓
Determine if additional evidence needed
    ↓
Recommend action
```

### Python Integration

Use the `QueryExecutor` class in `query_executor.py`:

```python
from tigergraph.query_executor import QueryExecutor

executor = QueryExecutor(use_simulation=False)  # Live TigerGraph

# Find shared devices
result = executor.find_shared_devices("C000001", device_threshold=2)
print(f"Connected customers: {result['shared_customers']}")

# Detect velocity
velocity = executor.detect_transaction_velocity("C000001", time_window_minutes=60)
print(f"Velocity anomaly score: {velocity['velocity_anomaly_score']}")

# Get context
context = executor.get_investigation_context("CASE000001")
print(f"Investigation has {len(context['evidence'])} pieces of evidence")
```

---

## Performance Considerations

### Query Optimization

1. **Indexing:** Ensure these are indexed in TigerGraph:
   - Customer.customer_id (PRIMARY_ID)
   - Transaction.transaction_id (PRIMARY_ID)
   - Device.device_id (PRIMARY_ID)
   - IPAddress.ip_address (PRIMARY_ID)
   - FraudCase.case_id (PRIMARY_ID)

2. **Query Limits:**
   - Each query limited to reasonable result sets
   - Network query limited to 2 hops for performance
   - Similar cases query limited to 5 results

3. **Parallel Execution:**
   - All queries can run in parallel
   - Combine results after all complete
   - Cache results for repeated lookups

### Expected Response Times (TigerGraph)

- **find_shared_devices:** 50-200ms (depending on network size)
- **find_shared_ips:** 30-100ms
- **detect_transaction_velocity:** 100-300ms (large time windows)
- **find_fraud_network:** 200-500ms (larger hops)
- **find_similar_historical_cases:** 50-150ms (indexed search)
- **get_investigation_context:** 300-800ms (most comprehensive)

---

## Development & Testing

### Running Queries in GSQL Console

```gsql
USE fraud_investigation

// Test find_shared_devices
RUN QUERY find_shared_devices("C000001", 2)

// Test find_shared_ips
RUN QUERY find_shared_ips("C000001", 3)

// Test velocity detection
RUN QUERY detect_transaction_velocity("C000001", 60)

// Test fraud network
RUN QUERY find_fraud_network("C000001", 2)

// Test similar cases
RUN QUERY find_similar_historical_cases("ACCOUNT_TAKEOVER", 0.7, 0.95)

// Test investigation context
RUN QUERY get_investigation_context("CASE000001")
```

### Simulation Mode (No TigerGraph Needed)

For testing without TigerGraph, use simulation mode:

```python
executor = QueryExecutor(use_simulation=True)

# Returns realistic sample data for testing agent logic
result = executor.find_shared_devices("C000001")
```

---

## Future Enhancements

1. **Additional Patterns:**
   - Circular payment loops detection
   - Beneficiary network analysis
   - Merchant risk clustering
   - Geographic anomaly detection

2. **Real-Time Processing:**
   - Stream transaction events
   - Update scores incrementally
   - Real-time network detection

3. **Machine Learning Integration:**
   - Learn which query combinations predict fraud
   - Optimize query parameters based on accuracy
   - Recommend queries based on case characteristics

4. **Advanced Analytics:**
   - Temporal pattern detection
   - Seasonality analysis
   - Anomaly baselines per customer segment
