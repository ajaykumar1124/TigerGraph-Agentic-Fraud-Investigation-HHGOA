# TigerGraph Schema Mapping for Fraud Investigation

## Data Flow: CSV → Python Processing → TigerGraph Vertices & Edges

### 1. TRANSACTIONS.CSV → Vertices & Edges

**Source Columns:**
- `TransactionID` → Transaction PK
- `customer_id` → Customer PK, Transaction.customer_id
- `TransactionAmt` → Transaction.amount
- `card1`, `card2`, `card3`, `card4`, `card5` → derive Account ID
- `timestamp` → Transaction.timestamp
- `risk_score` → Transaction.bank_risk_score
- `isFraud` → Transaction.is_fraud
- `ProductCD` → Transaction.product_code

**Created Entities:**
1. **Customer Vertex** (if not exists)
   - customer_id (PK)
   - Other fields populated later

2. **Account Vertex** (if not exists)
   - account_id = hash(customer_id + card1 + card2)
   - account_type = "CREDIT_CARD" (inferred)
   - card_last_4 = last 4 of card1

3. **Transaction Vertex**
   - transaction_id (PK) = TransactionID
   - customer_id
   - account_id
   - amount = TransactionAmt
   - timestamp = TransactionDT
   - bank_risk_score = risk_score
   - is_fraud = isFraud
   - status = "COMPLETED" (default)

4. **Merchant Vertex** (if not exists)
   - merchant_id = hash(P_emaildomain + addr1)
   - merchant_name = "Merchant_" + merchant_id
   - merchant_category = ProductCD mapping

5. **Edges Created:**
   - Customer -[OWNS]-> Account
   - Customer -[PERFORMS]-> Transaction
   - Transaction -[TRANSACTION_TO]-> Merchant

---

### 2. IDENTITY.CSV → Device & IP Vertices + Edges

**Source Columns:**
- `TransactionID` → link to Transaction
- `DeviceInfo` → Device PK derivation
- `DeviceType`, `DeviceOS`, `browser` → Device properties
- `IP_addr` → IPAddress PK
- `id_*` → Device fingerprinting
- `user_agent` → Device.user_agent

**Created Entities:**
1. **Device Vertex** (if not exists)
   - device_id = hash(DeviceInfo + DeviceType + DeviceOS + user_agent)
   - device_type = DeviceType mapping (1-4)
   - device_os = DeviceOS
   - browser = browser
   - user_agent = user_agent
   - first_seen = MIN(timestamp from all txns)
   - last_seen = MAX(timestamp from all txns)

2. **IPAddress Vertex** (if not exists)
   - ip_address (PK) = IP_addr
   - isp = "ISP_UNKNOWN" (not in data, can be enriched)
   - first_seen = MIN(timestamp)
   - last_seen = MAX(timestamp)
   - customer_count = COUNT(DISTINCT customer_id)

3. **Edges Created:**
   - Customer -[USES_DEVICE]-> Device
   - Customer -[USES_IP]-> IPAddress
   - Device -[SEEN_IN_TRANSACTION]-> IPAddress
   - Transaction -[USES_DEVICE]-> Device (optional, can be inferred)
   - Transaction -[USES_IP]-> IPAddress (optional)

---

### 3. CLOSED_CASES_HISTORY.CSV → FraudCase Vertices & Historical Evidence

**Source Columns:**
- `case_id` → FraudCase PK
- `customer_id` → FraudCase.customer_id
- `fraud_pattern` → FraudCase.fraud_pattern_detected, -[MATCHES_PATTERN]->
- `initial_risk_score`, `final_risk_score` → FraudCase.initial_risk_score, current_risk_score
- `evidence_count` → number of Evidence vertices to create
- `investigation_duration_hours` → inferred timing
- `action_taken` → Action vertex creation
- `outcome` → FraudCase.investigation_notes

**Created Entities:**
1. **FraudCase Vertex** (historical, case_status="CLOSED")
   - case_id (PK)
   - customer_id
   - initial_risk_score
   - current_risk_score = final_risk_score
   - fraud_pattern_detected
   - case_status = "CLOSED"
   - created_timestamp = now() (simulated)
   - updated_timestamp = closed_timestamp

2. **FraudPattern Vertex** (reference, shared)
   - pattern_id = ACCOUNT_TAKEOVER, PAYMENT_FRAUD, etc.
   - pattern_name
   - description
   - risk_weight = 0.7-0.9 (configurable)

3. **Action Vertex** (historical)
   - action_id = hash(case_id + action_taken)
   - case_id
   - action_type = action_taken
   - action_status = "EXECUTED"
   - approval_required = FALSE (already executed)

4. **Edges Created:**
   - FraudCase -[MATCHES_PATTERN]-> FraudPattern
   - FraudCase -[RECOMMENDS_ACTION]-> Action

---

### 4. CASE_PACK.CSV → Benchmark Cases (FraudCase)

**Source Columns:**
- `case_id` → FraudCase PK
- `flagged_txn_id` → Transaction to investigate
- `customer_id` → FraudCase.customer_id
- `trigger_type` → FraudCase.trigger_type
- `expected_fraud_type` → FraudCase.fraud_pattern_detected (ground truth)
- `fraud_confidence` → initial risk estimate

**Created Entities:**
1. **FraudCase Vertex** (benchmark, case_status="OPEN")
   - case_id (PK)
   - customer_id
   - trigger_transaction_id = flagged_txn_id
   - trigger_type
   - initial_risk_score = fraud_confidence
   - current_risk_score = fraud_confidence (before investigation)
   - fraud_pattern_detected = expected_fraud_type
   - case_status = "OPEN"
   - created_timestamp = now()

2. **Edges Created:**
   - FraudCase -[INVESTIGATES]-> Transaction (trigger_transaction_id)

---

## Loading Strategy

### Step 1: Create Vertices (Dimension Tables)
Order:
1. Customer (from transactions.customer_id unique values)
2. Account (derived from transactions)
3. Device (from identity)
4. IPAddress (from identity)
5. Merchant (from transactions)
6. FraudPattern (reference data, insert 5 patterns)

### Step 2: Create Transaction Facts
1. Transaction (from transactions.csv)
2. Edge: Customer -[PERFORMS]-> Transaction
3. Edge: Customer -[OWNS]-> Account
4. Edge: Transaction -[TRANSACTION_TO]-> Merchant

### Step 3: Create Device & Network Links
1. Edge: Customer -[USES_DEVICE]-> Device
2. Edge: Customer -[USES_IP]-> IPAddress
3. Edge: Device -[SEEN_IN_TRANSACTION]-> IPAddress (via intermediate Transaction)

### Step 4: Load Historical Cases (Closed)
1. FraudCase (from closed_cases_history.csv)
2. Edge: FraudCase -[MATCHES_PATTERN]-> FraudPattern
3. Evidence vertices (synthetic, derived from case metadata)
4. Edge: FraudCase -[HAS_EVIDENCE]-> Evidence
5. Action vertices
6. Edge: FraudCase -[RECOMMENDS_ACTION]-> Action

### Step 5: Load Benchmark Cases (Open)
1. FraudCase (from case_pack.csv)
2. Edge: FraudCase -[INVESTIGATES]-> Transaction

---

## Data Quality & Validation

### Checks During Load
- [x] No NULL primary keys
- [x] Transaction timestamps are valid
- [x] Risk scores are 0-1 or 0-100 (normalize)
- [x] Customer IDs exist before creating OWNS/PERFORMS
- [x] Account IDs are unique per customer
- [x] Device & IP counts match transaction counts
- [x] Fraud patterns exist before matching
- [x] No duplicate edges

### Post-Load Verification
```
SELECT COUNT(*) as customer_count FROM Customer;
SELECT COUNT(*) as transaction_count FROM Transaction;
SELECT COUNT(*) as device_count FROM Device;
SELECT COUNT(*) as ip_count FROM IPAddress;
SELECT COUNT(*) as case_count FROM FraudCase;
SELECT COUNT(DISTINCT customer_id) FROM Customer;
```

---

## Implementation Notes

### ID Generation Strategy
- **Customer ID**: Use as-is from CSV
- **Account ID**: `hash(customer_id + card1 + card2 + card3)` (PAN-safe)
- **Device ID**: `hash(DeviceInfo + browser + user_agent)`
- **IPAddress ID**: Use as-is
- **Merchant ID**: `hash(destination + product_code)` (if available)
- **Case ID**: Use as-is from CSV
- **Evidence ID**: `case_id + "_" + evidence_type + "_" + counter`
- **Action ID**: `case_id + "_action_" + counter`

### Deduplication
- Use MERGE operations to avoid duplicate vertices
- Check existence before INSERT for Customers, Devices, IPs, Merchants
- Allow multiple transactions per customer-device-ip combination

### Future Enrichment
- Add IP geolocation data (country, city, lat/long)
- Add merchant risk profiles
- Add customer KYC/AML status
- Add transaction category classification
- Link to external fraud databases
