"""
Risk Scoring Engine

Calculates fraud risk scores from various signals.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class RiskSignal:
    """A signal that contributes to fraud risk."""
    signal_name: str
    signal_value: float  # 0.0 to 1.0
    weight: float  # 0.0 to 1.0
    description: str


class RiskScoringEngine:
    """
    Calculates fraud risk scores using weighted signal combination.
    
    Signals are weighted by importance and combined using normalized sum.
    """
    
    # Signal weights (sum to 1.0)
    SIGNAL_WEIGHTS = {
        "bank_risk_score": 0.25,          # Risk from detection system
        "transaction_velocity": 0.15,    # Unusual transaction patterns
        "device_anomaly": 0.15,          # New/suspicious device
        "ip_anomaly": 0.15,              # Unusual IP
        "account_takeover_indicators": 0.15,  # Potential ATO signals
        "network_fraud_indicators": 0.10,    # Connected fraud network
        "behavioral_anomaly": 0.05      # Unusual behavior for customer
    }
    
    def __init__(self):
        """Initialize risk engine."""
        # Verify weights sum to 1.0
        total_weight = sum(self.SIGNAL_WEIGHTS.values())
        assert abs(total_weight - 1.0) < 0.01, f"Weights must sum to 1.0, got {total_weight}"
    
    def calculate_risk(self, signals: List[RiskSignal]) -> Tuple[float, Dict]:
        """
        Calculate overall risk score from signals.
        
        Args:
            signals: List of RiskSignal objects
        
        Returns:
            (risk_score, signal_breakdown)
        """
        weighted_sum = 0.0
        signal_breakdown = {}
        
        for signal in signals:
            weighted_value = signal.signal_value * signal.weight
            weighted_sum += weighted_value
            signal_breakdown[signal.signal_name] = {
                "value": signal.signal_value,
                "weight": signal.weight,
                "contribution": weighted_value,
                "description": signal.description
            }
        
        risk_score = min(weighted_sum, 1.0)  # Cap at 1.0
        
        return risk_score, signal_breakdown
    
    def score_transaction_velocity(
        self,
        transaction_count: int,
        total_amount: float,
        unique_merchants: int,
        customer_baseline_velocity: int = 2
    ) -> RiskSignal:
        """
        Calculate velocity anomaly score.
        
        Normal: ~2 transactions/hour
        Suspicious: 5+ transactions/hour
        Critical: 10+ transactions/hour
        """
        velocity = transaction_count / 1.0  # per hour
        baseline = customer_baseline_velocity
        
        if velocity <= baseline:
            velocity_score = 0.0
        elif velocity <= baseline * 2.5:
            velocity_score = 0.4
        elif velocity <= baseline * 5:
            velocity_score = 0.7
        else:
            velocity_score = 0.95
        
        description = f"{transaction_count} transactions in 1 hour (baseline: {baseline}/hr)"
        
        return RiskSignal(
            signal_name="transaction_velocity",
            signal_value=velocity_score,
            weight=self.SIGNAL_WEIGHTS["transaction_velocity"],
            description=description
        )
    
    def score_device_anomaly(
        self,
        is_new_device: bool,
        shared_device_count: int = 0,
        device_risk_history: int = 0
    ) -> RiskSignal:
        """
        Score device-related anomalies.
        
        - New device: +0.3
        - Shared with many customers: +0.4
        - Known fraudulent device: +0.8
        """
        device_score = 0.0
        
        if is_new_device:
            device_score += 0.3
        
        if shared_device_count > 5:
            device_score += 0.4
        elif shared_device_count > 2:
            device_score += 0.2
        
        if device_risk_history > 0:
            device_score += min(device_risk_history * 0.1, 0.8)
        
        device_score = min(device_score, 1.0)
        
        description = f"New device: {is_new_device}, Shared: {shared_device_count} users, History: {device_risk_history}"
        
        return RiskSignal(
            signal_name="device_anomaly",
            signal_value=device_score,
            weight=self.SIGNAL_WEIGHTS["device_anomaly"],
            description=description
        )
    
    def score_ip_anomaly(
        self,
        is_new_ip: bool,
        shared_ip_count: int = 0,
        is_datacenter_ip: bool = False,
        is_vpn_proxy: bool = False
    ) -> RiskSignal:
        """
        Score IP-related anomalies.
        
        - New IP: +0.2
        - Shared with many customers: +0.4
        - Datacenter/VPN: +0.3
        """
        ip_score = 0.0
        
        if is_new_ip:
            ip_score += 0.2
        
        if shared_ip_count > 5:
            ip_score += 0.4
        elif shared_ip_count > 2:
            ip_score += 0.2
        
        if is_datacenter_ip or is_vpn_proxy:
            ip_score += 0.3
        
        ip_score = min(ip_score, 1.0)
        
        description = f"New IP: {is_new_ip}, Shared: {shared_ip_count} users, Datacenter/VPN: {is_datacenter_ip or is_vpn_proxy}"
        
        return RiskSignal(
            signal_name="ip_anomaly",
            signal_value=ip_score,
            weight=self.SIGNAL_WEIGHTS["ip_anomaly"],
            description=description
        )
    
    def score_account_takeover_indicators(
        self,
        failed_logins: int = 0,
        password_changed_recently: bool = False,
        new_beneficiary_added: bool = False,
        unusual_location: bool = False
    ) -> RiskSignal:
        """
        Score account takeover (ATO) indicators.
        
        - Failed logins > 3: +0.3
        - Recent password change: +0.2
        - New beneficiary: +0.4
        - Unusual location: +0.15
        """
        ato_score = 0.0
        
        if failed_logins > 3:
            ato_score += 0.3
        
        if password_changed_recently:
            ato_score += 0.2
        
        if new_beneficiary_added:
            ato_score += 0.4
        
        if unusual_location:
            ato_score += 0.15
        
        ato_score = min(ato_score, 1.0)
        
        description = f"Failed logins: {failed_logins}, Pwd changed: {password_changed_recently}, New beneficiary: {new_beneficiary_added}, Unusual location: {unusual_location}"
        
        return RiskSignal(
            signal_name="account_takeover_indicators",
            signal_value=ato_score,
            weight=self.SIGNAL_WEIGHTS["account_takeover_indicators"],
            description=description
        )
    
    def score_network_fraud_indicators(
        self,
        network_size: int = 0,
        critical_nodes: int = 0,
        confirmed_fraud_connections: int = 0
    ) -> RiskSignal:
        """
        Score fraud network indicators.
        
        - Part of network: +0.2
        - Connected to critical nodes: +0.4
        - Confirmed fraud connections: +0.6
        """
        network_score = 0.0
        
        if network_size > 0:
            network_score += 0.2
        
        if critical_nodes > 0:
            network_score += min(critical_nodes * 0.15, 0.4)
        
        if confirmed_fraud_connections > 0:
            network_score += min(confirmed_fraud_connections * 0.2, 0.6)
        
        network_score = min(network_score, 1.0)
        
        description = f"Network size: {network_size}, Critical nodes: {critical_nodes}, Confirmed fraud: {confirmed_fraud_connections}"
        
        return RiskSignal(
            signal_name="network_fraud_indicators",
            signal_value=network_score,
            weight=self.SIGNAL_WEIGHTS["network_fraud_indicators"],
            description=description
        )
    
    def score_behavioral_anomaly(
        self,
        typical_amount: float = 500,
        transaction_amount: float = 0,
        typical_frequency: int = 2,
        current_frequency: int = 0
    ) -> RiskSignal:
        """
        Score behavioral anomalies.
        
        - Amount deviation: up to +0.5
        - Frequency deviation: up to +0.3
        """
        behavior_score = 0.0
        
        # Amount deviation
        if typical_amount > 0:
            amount_ratio = transaction_amount / typical_amount
            if amount_ratio > 3:
                behavior_score += 0.5
            elif amount_ratio > 1.5:
                behavior_score += 0.3
        
        # Frequency deviation
        if typical_frequency > 0:
            freq_ratio = current_frequency / typical_frequency
            if freq_ratio > 5:
                behavior_score += 0.3
            elif freq_ratio > 2:
                behavior_score += 0.15
        
        behavior_score = min(behavior_score, 1.0)
        
        description = f"Amount ratio: {transaction_amount/typical_amount if typical_amount > 0 else 0:.1f}x, Frequency ratio: {current_frequency/typical_frequency if typical_frequency > 0 else 0:.1f}x"
        
        return RiskSignal(
            signal_name="behavioral_anomaly",
            signal_value=behavior_score,
            weight=self.SIGNAL_WEIGHTS["behavioral_anomaly"],
            description=description
        )


def test_risk_engine():
    """Test risk scoring engine."""
    engine = RiskScoringEngine()
    
    print("\n" + "="*70)
    print("RISK SCORING ENGINE TEST")
    print("="*70 + "\n")
    
    # Scenario 1: High risk (account takeover indicators)
    signals = [
        engine.score_transaction_velocity(12, 5000, 6),
        engine.score_device_anomaly(True, shared_device_count=3),
        engine.score_ip_anomaly(True, shared_ip_count=2),
        engine.score_account_takeover_indicators(
            failed_logins=5,
            password_changed_recently=True,
            new_beneficiary_added=True,
            unusual_location=True
        ),
        RiskSignal("bank_risk_score", 0.85, engine.SIGNAL_WEIGHTS["bank_risk_score"], "System risk score"),
        RiskSignal("network_fraud_indicators", 0.3, engine.SIGNAL_WEIGHTS["network_fraud_indicators"], "Minor network connection"),
        RiskSignal("behavioral_anomaly", 0.4, engine.SIGNAL_WEIGHTS["behavioral_anomaly"], "Amount deviation")
    ]
    
    risk, breakdown = engine.calculate_risk(signals)
    
    print(f"Scenario 1: Account Takeover Suspected")
    print(f"Overall Risk Score: {risk:.2f}\n")
    print("Signal Breakdown:")
    for signal_name, details in breakdown.items():
        print(f"  {signal_name}:")
        print(f"    Value: {details['value']:.2f}")
        print(f"    Weight: {details['weight']:.2f}")
        print(f"    Contribution: {details['contribution']:.4f}")
        print(f"    Description: {details['description']}\n")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    test_risk_engine()
