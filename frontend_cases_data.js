const cases = [
  {
    "id": "HHG-001",
    "customer": "USR_0001",
    "title": "Account Takeover - Impossible Travel",
    "risk": 92,
    "status": "CRITICAL",
    "amount": 39000,
    "transactions": 4,
    "time": "2 hours ago",
    "findings": [
      "Impossible travel: Mumbai to Delhi in 7 minutes",
      "Multiple ATM withdrawals in rapid succession",
      "Device fingerprint mismatch across transactions",
      "Unusual withdrawal amounts exceeding daily limits"
    ],
    "recommendations": [
      "Block account immediately, contact customer, file fraud report"
    ]
  },
  {
    "id": "HHG-002",
    "customer": "USR_0002",
    "title": "International Wire Transfer Fraud",
    "risk": 94,
    "status": "CRITICAL",
    "amount": 45000,
    "transactions": 4,
    "time": "4 hours ago",
    "findings": [
      "Large wire transfer to high-risk country at 3:15 AM",
      "First-time international transfer",
      "Velocity check failed - exceeded daily limit by 300%",
      "Customer behavioral anomaly detected"
    ],
    "recommendations": [
      "Hold transaction for manual review, contact customer immediately"
    ]
  },
  {
    "id": "HHG-003",
    "customer": "USR_0003",
    "title": "Cryptocurrency Exchange Fraud",
    "risk": 96,
    "status": "CRITICAL",
    "amount": 95000,
    "transactions": 4,
    "time": "6 hours ago",
    "findings": [
      "Large crypto purchase from unverified exchange",
      "KYC data mismatch with customer profile",
      "Transaction originated from high-risk jurisdiction",
      "Unusual time of transaction (2:30 AM)"
    ],
    "recommendations": [
      "Block transaction, require enhanced KYC verification"
    ]
  },
  {
    "id": "HHG-004",
    "customer": "USR_0004",
    "title": "Early Morning ATM Withdrawal",
    "risk": 89,
    "status": "HIGH",
    "amount": 35000,
    "transactions": 4,
    "time": "8 hours ago",
    "findings": [
      "Large ATM withdrawal at 5:00 AM in Chennai",
      "Location 200km from customer's home address",
      "Amount exceeds typical customer behavior by 400%",
      "First withdrawal at this ATM location"
    ],
    "recommendations": [
      "Flag account for monitoring, verify with customer"
    ]
  },
  {
    "id": "HHG-005",
    "customer": "USR_0005",
    "title": "Rapid Succession Transfers",
    "risk": 75,
    "status": "HIGH",
    "amount": 24500,
    "transactions": 4,
    "time": "10 hours ago",
    "findings": [
      "Three transfers within 5 minutes from mobile app",
      "Transfers to new recipients not in contact list",
      "Velocity exceeded by 150%",
      "Geolocation shows unusual IP address"
    ],
    "recommendations": [
      "Require additional verification for future transfers"
    ]
  },
  {
    "id": "HHG-006",
    "customer": "USR_0006",
    "title": "False Positive - Legitimate Business Transaction",
    "risk": 45,
    "status": "LOW",
    "amount": 0,
    "transactions": 4,
    "time": "12 hours ago",
    "findings": [
      "Large transfer flagged but verified as legitimate business payment",
      "Customer has history of similar business transactions",
      "Proper documentation provided",
      "Recipient is verified business entity"
    ],
    "recommendations": [
      "Whitelist this business relationship, close case"
    ]
  },
  {
    "id": "HHG-007",
    "customer": "USR_0007",
    "title": "Card Present Fraud - Stolen Card",
    "risk": 91,
    "status": "HIGH",
    "amount": 8000,
    "transactions": 4,
    "time": "14 hours ago",
    "findings": [
      "Multiple failed PIN attempts followed by signature transaction",
      "High-value jewelry store purchase",
      "Card reported stolen 2 hours before transaction",
      "Customer location 500km away at time of purchase"
    ],
    "recommendations": [
      "Reverse transaction, contact merchant, file police report"
    ]
  },
  {
    "id": "HHG-008",
    "customer": "USR_0008",
    "title": "E-commerce Fraud - Account Takeover",
    "risk": 88,
    "status": "HIGH",
    "amount": 15000,
    "transactions": 4,
    "time": "16 hours ago",
    "findings": [
      "Multiple e-commerce purchases to new shipping address",
      "Email change request 1 hour before purchases",
      "Different device and IP address than historical pattern",
      "High-value electronics ordered for express delivery"
    ],
    "recommendations": [
      "Cancel orders, lock account, contact customer"
    ]
  },
  {
    "id": "HHG-009",
    "customer": "USR_0009",
    "title": "Business Email Compromise (BEC)",
    "risk": 93,
    "status": "CRITICAL",
    "amount": 250000,
    "transactions": 4,
    "time": "18 hours ago",
    "findings": [
      "Wire transfer initiated after email compromise",
      "Payment to new vendor not in system",
      "Email headers show spoofed domain",
      "Urgent payment request bypassed normal approval"
    ],
    "recommendations": [
      "Block transfer immediately, alert security team, contact vendor"
    ]
  },
  {
    "id": "HHG-010",
    "customer": "USR_0010",
    "title": "Phishing Attack - Credential Theft",
    "risk": 87,
    "status": "HIGH",
    "amount": 12000,
    "transactions": 4,
    "time": "20 hours ago",
    "findings": [
      "Login from unusual location immediately after phishing email sent",
      "Multiple failed authentication attempts",
      "Successful login followed by immediate fund transfer",
      "Customer reported suspicious email 30 minutes later"
    ],
    "recommendations": [
      "Reset credentials, reverse transfer if possible, educate customer"
    ]
  },
  {
    "id": "HHG-011",
    "customer": "USR_0011",
    "title": "False Positive - Customer Traveling",
    "risk": 38,
    "status": "LOW",
    "amount": 0,
    "transactions": 4,
    "time": "22 hours ago",
    "findings": [
      "International transactions flagged during customer vacation",
      "Customer provided travel notice",
      "Transaction pattern consistent with travel itinerary",
      "All transactions verified by customer"
    ],
    "recommendations": [
      "Close case, no action required"
    ]
  },
  {
    "id": "HHG-012",
    "customer": "USR_0012",
    "title": "Money Mule Activity",
    "risk": 90,
    "status": "HIGH",
    "amount": 75000,
    "transactions": 4,
    "time": "24 hours ago",
    "findings": [
      "Multiple large deposits followed by immediate withdrawals",
      "Funds moved through multiple accounts in chain pattern",
      "Account holder appears to be unknowing participant",
      "Connected to known fraud ring through graph analysis"
    ],
    "recommendations": [
      "Freeze account, report to authorities, interview account holder"
    ]
  },
  {
    "id": "HHG-013",
    "customer": "USR_0013",
    "title": "Check Fraud - Altered Check",
    "risk": 85,
    "status": "HIGH",
    "amount": 5500,
    "transactions": 4,
    "time": "26 hours ago",
    "findings": [
      "Check amount altered from \u20b9550 to \u20b95500",
      "Payee name modified",
      "Signature mismatch detected by analysis",
      "Customer denies writing check for this amount"
    ],
    "recommendations": [
      "Deny check payment, contact customer, file fraud report"
    ]
  },
  {
    "id": "HHG-014",
    "customer": "USR_0014",
    "title": "SIM Swap Attack",
    "risk": 92,
    "status": "CRITICAL",
    "amount": 28000,
    "transactions": 4,
    "time": "28 hours ago",
    "findings": [
      "Mobile number ported to new SIM card",
      "Immediate login and password reset after SIM swap",
      "Multiple fund transfers within 15 minutes",
      "Customer unable to receive OTP verification"
    ],
    "recommendations": [
      "Block account, reverse transfers, deactivate mobile banking"
    ]
  },
  {
    "id": "HHG-015",
    "customer": "USR_0015",
    "title": "Insider Fraud - Employee Access Abuse",
    "risk": 78,
    "status": "HIGH",
    "amount": 18000,
    "transactions": 4,
    "time": "30 hours ago",
    "findings": [
      "Employee accessed customer accounts outside normal duties",
      "Small recurring transfers to external account",
      "Access logs show unusual after-hours activity",
      "Pattern detected across multiple customer accounts"
    ],
    "recommendations": [
      "Suspend employee access, conduct internal investigation"
    ]
  },
  {
    "id": "HHG-016",
    "customer": "USR_0016",
    "title": "False Positive - Legitimate Large Purchase",
    "risk": 42,
    "status": "LOW",
    "amount": 0,
    "transactions": 4,
    "time": "32 hours ago",
    "findings": [
      "Large real estate down payment flagged",
      "Customer provided documentation of home purchase",
      "Transaction verified with real estate agent",
      "Funds properly sourced and documented"
    ],
    "recommendations": [
      "Approve transaction, close case"
    ]
  },
  {
    "id": "HHG-017",
    "customer": "USR_0017",
    "title": "Romance Scam - Social Engineering",
    "risk": 89,
    "status": "HIGH",
    "amount": 45000,
    "transactions": 4,
    "time": "34 hours ago",
    "findings": [
      "Multiple transfers to same overseas recipient",
      "Customer contacted after family reported concern",
      "Recipient profile matches known romance scam pattern",
      "Customer emotionally invested, initially denied fraud"
    ],
    "recommendations": [
      "Block further transfers, victim support services, education"
    ]
  },
  {
    "id": "HHG-018",
    "customer": "USR_0018",
    "title": "ATM Skimming Device",
    "risk": 94,
    "status": "CRITICAL",
    "amount": 67000,
    "transactions": 4,
    "time": "36 hours ago",
    "findings": [
      "15 customers compromised at same ATM location",
      "Fraudulent transactions within 48 hours of ATM use",
      "Card data used at international locations",
      "Skimming device found during ATM inspection"
    ],
    "recommendations": [
      "Block all affected cards, notify customers, alert authorities"
    ]
  },
  {
    "id": "HHG-019",
    "customer": "USR_0019",
    "title": "Synthetic Identity Fraud",
    "risk": 86,
    "status": "HIGH",
    "amount": 32000,
    "transactions": 4,
    "time": "38 hours ago",
    "findings": [
      "New account opened with partially fabricated identity",
      "Mix of real and fake identity documents",
      "Rapid credit line increases requested",
      "No prior credit history found for SSN/Aadhaar combination"
    ],
    "recommendations": [
      "Close account, report to credit bureaus, investigate other accounts"
    ]
  },
  {
    "id": "HHG-020",
    "customer": "USR_0020",
    "title": "Ransomware Payment",
    "risk": 91,
    "status": "CRITICAL",
    "amount": 150000,
    "transactions": 4,
    "time": "40 hours ago",
    "findings": [
      "Large cryptocurrency purchase following ransomware attack",
      "Company systems encrypted by malware",
      "Payment demanded in Bitcoin to specific wallet",
      "Transaction initiated under duress"
    ],
    "recommendations": [
      "Contact cybersecurity team, law enforcement, consider alternatives"
    ]
  }
];
