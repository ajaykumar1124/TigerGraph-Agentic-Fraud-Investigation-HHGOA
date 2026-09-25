"""
Data Loader - Load IEEE-CIS dataset into TigerGraph
Handles CSV parsing, transformation, and graph population
"""

import logging
import pandas as pd
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

from backend.config import settings
from backend.tigergraph.client import get_client

logger = logging.getLogger(__name__)


class DataLoader:
    """Load IEEE-CIS dataset into TigerGraph"""

    def __init__(self, client=None):
        """Initialize loader"""
        self.client = client or get_client()
        self.config = settings.data
        self.data_dir = Path(self.config.data_dir)

    def load_all_data(self) -> Dict[str, int]:
        """Load all dataset components"""
        logger.info("=" * 60)
        logger.info("Starting comprehensive data load into TigerGraph")
        logger.info("=" * 60)

        stats = {}
        try:
            # Load transactions
            stats["transactions"] = self._load_transactions()

            # Load fraud patterns
            stats["patterns"] = self._load_fraud_patterns()

            # Load policies
            stats["policies"] = self._load_policies()

            # Load closed cases for case memory
            stats["historical_cases"] = self._load_historical_cases()

            logger.info("=" * 60)
            logger.info("Data load complete!")
            logger.info(f"Summary: {stats}")
            logger.info("=" * 60)

            return stats

        except Exception as e:
            logger.error(f"✗ Data load failed: {str(e)}")
            raise

    def _load_transactions(self) -> int:
        """Load IEEE-CIS transactions"""
        logger.info("\n[1/4] Loading transactions...")

        trans_file = self.data_dir / self.config.transaction_file
        identity_file = self.data_dir / self.config.identity_file

        if not trans_file.exists():
            logger.warning(f"⚠ Transaction file not found: {trans_file}")
            logger.info("   → Creating synthetic test transactions instead")
            return self._create_synthetic_transactions()

        try:
            # Load transaction CSV
            df_trans = pd.read_csv(trans_file, nrows=self.config.max_samples)
            logger.info(f"   Loaded {len(df_trans)} transactions from CSV")

            # Load identity CSV if available
            df_identity = None
            if identity_file.exists():
                df_identity = pd.read_csv(identity_file)
                logger.info(f"   Loaded {len(df_identity)} identity records")

            # Process and insert
            users_inserted = set()
            cards_inserted = set()
            devices_inserted = set()
            ips_inserted = set()
            merchants_inserted = set()
            transactions_inserted = 0

            for idx, row in df_trans.iterrows():
                if idx % 1000 == 0:
                    logger.info(f"   Processing transaction {idx}/{len(df_trans)}")

                try:
                    # Extract IDs
                    user_id = int(row.get("TransactionID", idx))
                    card_id = int(row.get("CardID", idx))
                    merchant_id = int(row.get("MerchantID", idx))

                    # Insert User
                    if user_id not in users_inserted:
                        self.client.upsert_vertex(
                            "User",
                            str(user_id),
                            {
                                "email": f"user_{user_id}@bank.com",
                                "phone": f"+1-555-{user_id % 10000:04d}",
                                "name": f"Customer_{user_id}",
                                "kyc_status": "verified",
                                "account_age_days": random.randint(30, 1000),
                                "risk_score": float(row.get("isFraud", 0)),
                                "created_at": int(datetime.now().timestamp()),
                                "last_active": int(datetime.now().timestamp()),
                            },
                        )
                        users_inserted.add(user_id)

                    # Insert Card
                    if card_id not in cards_inserted:
                        self.client.upsert_vertex(
                            "Card",
                            str(card_id),
                            {
                                "card_number": f"****{card_id % 10000:04d}",
                                "bin": f"4{card_id % 1000000:06d}",
                                "card_type": "CREDIT",
                                "expiry_date": "12/25",
                                "issuer": "BANK_A",
                                "is_active": True,
                                "created_at": int(datetime.now().timestamp()),
                            },
                        )
                        cards_inserted.add(card_id)

                    # Insert Device
                    device_id = f"device_{user_id}_{idx % 10}"
                    if device_id not in devices_inserted:
                        self.client.upsert_vertex(
                            "Device",
                            device_id,
                            {
                                "device_type": random.choice(["mobile", "desktop", "tablet"]),
                                "os": random.choice(["iOS", "Android", "Windows", "macOS"]),
                                "browser": random.choice(["Chrome", "Safari", "Firefox"]),
                                "user_agent": f"Mozilla/5.0_{idx}",
                                "fingerprint": f"fp_{idx:08x}",
                                "first_seen": int(datetime.now().timestamp()),
                            },
                        )
                        devices_inserted.add(device_id)

                    # Insert IP Address
                    ip_addr = f"192.168.{idx % 256}.{(idx // 256) % 256}"
                    if ip_addr not in ips_inserted:
                        self.client.upsert_vertex(
                            "IPAddress",
                            ip_addr,
                            {
                                "ip_address": ip_addr,
                                "country": random.choice(["US", "UK", "CA", "IN", "CN"]),
                                "region": "State",
                                "city": "City",
                                "is_vpn": random.choice([True, False]),
                                "is_proxy": False,
                                "is_datacenter": False,
                                "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
                            },
                        )
                        ips_inserted.add(ip_addr)

                    # Insert Merchant
                    if merchant_id not in merchants_inserted:
                        self.client.upsert_vertex(
                            "Merchant",
                            str(merchant_id),
                            {
                                "merchant_name": f"Merchant_{merchant_id}",
                                "mcc_code": random.randint(1000, 9999),
                                "country": "US",
                                "risk_category": "RETAIL",
                                "is_high_risk": random.choice([True, False]),
                            },
                        )
                        merchants_inserted.add(merchant_id)

                    # Insert Transaction
                    transaction_id = f"txn_{idx:08x}"
                    amount = float(row.get("Amount", random.uniform(10, 1000)))
                    is_fraud = int(row.get("isFraud", 0)) == 1

                    self.client.upsert_vertex(
                        "Transaction",
                        transaction_id,
                        {
                            "amount": amount,
                            "currency": "USD",
                            "timestamp": int(datetime.now().timestamp()),
                            "transaction_type": "purchase",
                            "is_online": random.choice([True, False]),
                            "is_fraud": is_fraud,
                            "fraud_score": float(row.get("isFraud", 0)),
                        },
                    )

                    # Insert Edges
                    self.client.upsert_edge(
                        "OWNS_CARD",
                        "User",
                        str(user_id),
                        "Card",
                        str(card_id),
                        {"since_date": int(datetime.now().timestamp()), "is_primary": True},
                    )

                    self.client.upsert_edge(
                        "USES_DEVICE",
                        "User",
                        str(user_id),
                        "Device",
                        device_id,
                        {"first_use": int(datetime.now().timestamp()), "usage_count": 1},
                    )

                    self.client.upsert_edge(
                        "CONNECTS_FROM",
                        "Device",
                        device_id,
                        "IPAddress",
                        ip_addr,
                        {"connection_timestamp": int(datetime.now().timestamp()), "connection_duration": 300},
                    )

                    self.client.upsert_edge(
                        "HAS_TRANSACTION",
                        "User",
                        str(user_id),
                        "Transaction",
                        transaction_id,
                        {"timestamp": int(datetime.now().timestamp()), "transaction_sequence": idx},
                    )

                    self.client.upsert_edge(
                        "USED_IN_TRANSACTION",
                        "Card",
                        str(card_id),
                        "Transaction",
                        transaction_id,
                        {"timestamp": int(datetime.now().timestamp())},
                    )

                    self.client.upsert_edge(
                        "DEVICE_IN_TRANSACTION",
                        "Device",
                        device_id,
                        "Transaction",
                        transaction_id,
                        {"timestamp": int(datetime.now().timestamp())},
                    )

                    self.client.upsert_edge(
                        "IP_IN_TRANSACTION",
                        "IPAddress",
                        ip_addr,
                        "Transaction",
                        transaction_id,
                        {"timestamp": int(datetime.now().timestamp())},
                    )

                    self.client.upsert_edge(
                        "TRANSACTED_WITH",
                        "Transaction",
                        transaction_id,
                        "Merchant",
                        str(merchant_id),
                        {"amount": amount, "timestamp": int(datetime.now().timestamp())},
                    )

                    transactions_inserted += 1

                except Exception as e:
                    logger.warning(f"   ⚠ Skipped transaction {idx}: {str(e)}")
                    continue

            logger.info(f"   ✓ Loaded {transactions_inserted} transactions")
            logger.info(f"     - Users: {len(users_inserted)}")
            logger.info(f"     - Cards: {len(cards_inserted)}")
            logger.info(f"     - Devices: {len(devices_inserted)}")
            logger.info(f"     - IPs: {len(ips_inserted)}")
            logger.info(f"     - Merchants: {len(merchants_inserted)}")

            return transactions_inserted

        except Exception as e:
            logger.error(f"✗ Failed to load transactions: {str(e)}")
            raise

    def _create_synthetic_transactions(self, count: int = 100) -> int:
        """Create synthetic transactions for testing"""
        logger.info(f"   Creating {count} synthetic transactions for testing...")

        try:
            for i in range(count):
                user_id = i
                card_id = i
                merchant_id = i % 10
                device_id = f"device_{i}"
                ip_addr = f"192.168.{i % 256}.{(i // 256) % 256}"
                transaction_id = f"txn_{i:08x}"

                # Create User
                self.client.upsert_vertex(
                    "User",
                    str(user_id),
                    {
                        "email": f"user_{user_id}@bank.com",
                        "kyc_status": "verified",
                        "risk_score": 0.0,
                        "created_at": int(datetime.now().timestamp()),
                    },
                )

                # Create Card
                self.client.upsert_vertex(
                    "Card",
                    str(card_id),
                    {
                        "card_number": f"****{card_id % 10000:04d}",
                        "is_active": True,
                        "created_at": int(datetime.now().timestamp()),
                    },
                )

                # Create Device
                self.client.upsert_vertex(
                    "Device",
                    device_id,
                    {"device_type": "mobile", "os": "iOS", "first_seen": int(datetime.now().timestamp())},
                )

                # Create IP
                self.client.upsert_vertex(
                    "IPAddress",
                    ip_addr,
                    {
                        "ip_address": ip_addr,
                        "country": "US",
                        "is_vpn": False,
                        "risk_level": "LOW",
                    },
                )

                # Create Merchant
                self.client.upsert_vertex(
                    "Merchant",
                    str(merchant_id),
                    {
                        "merchant_name": f"Merchant_{merchant_id}",
                        "mcc_code": 5411 + merchant_id,
                        "is_high_risk": False,
                    },
                )

                # Create Transaction
                is_fraud = i % 20 == 0  # 5% fraud rate
                self.client.upsert_vertex(
                    "Transaction",
                    transaction_id,
                    {
                        "amount": random.uniform(10, 500),
                        "currency": "USD",
                        "timestamp": int(datetime.now().timestamp()),
                        "is_fraud": is_fraud,
                        "fraud_score": 1.0 if is_fraud else 0.0,
                    },
                )

                # Create edges
                self.client.upsert_edge(
                    "OWNS_CARD", "User", str(user_id), "Card", str(card_id), {}
                )
                self.client.upsert_edge("USES_DEVICE", "User", str(user_id), "Device", device_id, {})
                self.client.upsert_edge(
                    "CONNECTS_FROM", "Device", device_id, "IPAddress", ip_addr, {}
                )
                self.client.upsert_edge(
                    "HAS_TRANSACTION", "User", str(user_id), "Transaction", transaction_id, {}
                )
                self.client.upsert_edge(
                    "USED_IN_TRANSACTION", "Card", str(card_id), "Transaction", transaction_id, {}
                )
                self.client.upsert_edge(
                    "TRANSACTED_WITH",
                    "Transaction",
                    transaction_id,
                    "Merchant",
                    str(merchant_id),
                    {},
                )

            logger.info(f"   ✓ Created {count} synthetic transactions")
            return count

        except Exception as e:
            logger.error(f"✗ Failed to create synthetic transactions: {str(e)}")
            raise

    def _load_fraud_patterns(self) -> int:
        """Load known fraud patterns"""
        logger.info("\n[2/4] Loading fraud patterns...")

        patterns_file = self.data_dir / self.config.patterns_file

        # Default patterns
        default_patterns = [
            {
                "pattern_id": 1,
                "pattern_name": "Velocity_Attack",
                "pattern_type": "behavioral",
                "description": "Multiple transactions in short time",
                "risk_level": "HIGH",
            },
            {
                "pattern_id": 2,
                "pattern_name": "Card_Testing",
                "pattern_type": "testing",
                "description": "Small amounts to test card validity",
                "risk_level": "HIGH",
            },
            {
                "pattern_id": 3,
                "pattern_name": "Geographic_Anomaly",
                "pattern_type": "location",
                "description": "Transaction in impossible location",
                "risk_level": "MEDIUM",
            },
            {
                "pattern_id": 4,
                "pattern_name": "Device_Mismatch",
                "pattern_type": "device",
                "description": "Transaction from unknown device",
                "risk_level": "MEDIUM",
            },
            {
                "pattern_id": 5,
                "pattern_name": "Merchant_Anomaly",
                "pattern_type": "merchant",
                "description": "Transaction with high-risk merchant",
                "risk_level": "MEDIUM",
            },
        ]

        try:
            if patterns_file.exists():
                with open(patterns_file) as f:
                    patterns = json.load(f)
                    logger.info(f"   Loaded {len(patterns)} patterns from JSON")
            else:
                patterns = default_patterns

            for pattern in patterns:
                self.client.upsert_vertex(
                    "FraudPattern",
                    str(pattern.get("pattern_id", pattern.get("id"))),
                    {
                        "pattern_name": pattern.get("pattern_name"),
                        "pattern_type": pattern.get("pattern_type", "unknown"),
                        "description": pattern.get("description", ""),
                        "risk_level": pattern.get("risk_level", "MEDIUM"),
                        "is_active": pattern.get("is_active", True),
                    },
                )

            logger.info(f"   ✓ Loaded {len(patterns)} fraud patterns")
            return len(patterns)

        except Exception as e:
            logger.error(f"✗ Failed to load fraud patterns: {str(e)}")
            raise

    def _load_policies(self) -> int:
        """Load fraud policies"""
        logger.info("\n[3/4] Loading fraud policies...")

        policies_file = self.data_dir / self.config.policies_file

        # Default policies
        default_policies = [
            {
                "policy_id": 1,
                "policy_name": "High_Risk_Merchant",
                "policy_text": "Block transactions with high-risk merchants",
                "rule_type": "merchant_check",
            },
            {
                "policy_id": 2,
                "policy_name": "Velocity_Check",
                "policy_text": "Flag if >5 transactions in 1 hour",
                "rule_type": "velocity_check",
            },
            {
                "policy_id": 3,
                "policy_name": "Geographic_Check",
                "policy_text": "Flag transactions from new country",
                "rule_type": "location_check",
            },
            {
                "policy_id": 4,
                "policy_name": "Device_Check",
                "policy_text": "Flag transactions from new device",
                "rule_type": "device_check",
            },
            {
                "policy_id": 5,
                "policy_name": "KYC_Check",
                "policy_text": "Require additional verification if KYC incomplete",
                "rule_type": "kyc_check",
            },
            {
                "policy_id": 6,
                "policy_name": "Amount_Check",
                "policy_text": "Flag if amount > user daily limit",
                "rule_type": "amount_check",
            },
        ]

        try:
            policies = default_policies
            if policies_file.exists():
                try:
                    with open(policies_file) as f:
                        policies = json.load(f)
                        logger.info(f"   Loaded {len(policies)} policies from markdown")
                except:
                    logger.info("   Using default policies")

            for policy in policies:
                self.client.upsert_vertex(
                    "Policy",
                    str(policy.get("policy_id", policy.get("id"))),
                    {
                        "policy_name": policy.get("policy_name"),
                        "policy_text": policy.get("policy_text", ""),
                        "rule_type": policy.get("rule_type", "custom"),
                        "is_active": policy.get("is_active", True),
                        "created_at": int(datetime.now().timestamp()),
                    },
                )

            logger.info(f"   ✓ Loaded {len(policies)} policies")
            return len(policies)

        except Exception as e:
            logger.error(f"✗ Failed to load policies: {str(e)}")
            raise

    def _load_historical_cases(self) -> int:
        """Load historical closed cases for case memory"""
        logger.info("\n[4/4] Loading historical cases...")

        closed_cases_file = self.data_dir / self.config.closed_cases_file

        try:
            if closed_cases_file.exists():
                df = pd.read_csv(closed_cases_file, nrows=100)
                logger.info(f"   Loaded {len(df)} historical cases from CSV")

                for idx, row in df.iterrows():
                    case_id = f"hist_case_{idx:06x}"
                    self.client.upsert_vertex(
                        "HistoricalCase",
                        case_id,
                        {
                            "original_case_id": str(row.get("CaseID", idx)),
                            "case_outcome": row.get("Outcome", "resolved"),
                            "accuracy": float(row.get("Accuracy", 0.8)),
                            "patterns_found": str(row.get("Patterns", "[]")),
                            "lessons_learned": row.get("Lessons", ""),
                            "closed_at": int(datetime.now().timestamp()),
                        },
                    )

                logger.info(f"   ✓ Loaded {len(df)} historical cases")
                return len(df)
            else:
                logger.info("   No historical cases file found (optional)")
                return 0

        except Exception as e:
            logger.error(f"✗ Failed to load historical cases: {str(e)}")
            raise


def load_data():
    """Load all data into TigerGraph"""
    try:
        client = get_client()
        loader = DataLoader(client)
        stats = loader.load_all_data()
        return stats
    except Exception as e:
        logger.error(f"Data load failed: {str(e)}")
        raise
