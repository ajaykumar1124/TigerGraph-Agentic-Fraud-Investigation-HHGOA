# TigerGraph Setup

## Schema
- `schema/`: Graph schema definitions
- `queries/`: GSQL queries for fraud detection
- `loading/`: Data loading scripts

## Quick Start

1. **Create Graph Schema:**
   ```bash
   gsql schema/schema.gsql
   ```

2. **Load Queries:**
   ```bash
   gsql queries/fraud_patterns.gsql
   ```

3. **Load Data:**
   ```bash
   gsql loading/load_data.gsql
   ```

## Queries Available
- `find_suspicious_accounts.gsql` - Detect suspicious account patterns
- `trace_money_flow.gsql` - Track transaction flows
- `find_connected_entities.gsql` - Find fraud rings
- `transaction_history.gsql` - Get complete transaction history
- `fraud_patterns.gsql` - Match known fraud patterns
