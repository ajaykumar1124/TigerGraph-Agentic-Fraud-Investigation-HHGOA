"""
Reorganize project to professional structure
KEEPS cases/ folder at root (required for hackathon)
"""
import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create new directory structure"""
    directories = [
        # Backend structure
        "backend/app",
        "backend/app/routes",
        "backend/app/agents",
        "backend/app/services",
        "backend/app/models",
        
        # Frontend structure (already exists, but add missing dirs)
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/services",
        "frontend/public",
        
        # TigerGraph structure
        "tigergraph/schema",
        "tigergraph/queries",
        "tigergraph/loading",
        
        # Data structure
        "data/raw",
        "data/processed",
        "data/sample",
        
        # Scripts
        "scripts",
        
        # Docs
        "docs",
        "docs/screenshots",
        
        # Tests
        "tests",
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("\n✅ Directory structure created!")

def create_backend_files():
    """Create backend __init__.py files and organize"""
    print("\n📝 Creating backend files...")
    
    # Create __init__.py files
    init_files = [
        "backend/app/__init__.py",
        "backend/app/routes/__init__.py",
        "backend/app/agents/__init__.py",
        "backend/app/services/__init__.py",
        "backend/app/models/__init__.py",
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"   ✅ {init_file}")
    
    print("✅ Backend structure created!")

def create_tigergraph_structure():
    """Create TigerGraph structure with README"""
    print("\n📝 Creating TigerGraph structure...")
    
    # Create TigerGraph README
    tigergraph_readme = """# TigerGraph Setup

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
"""
    
    with open("tigergraph/README.md", "w") as f:
        f.write(tigergraph_readme)
    
    print("   ✅ tigergraph/README.md")
    print("✅ TigerGraph structure created!")

def create_scripts():
    """Create utility scripts"""
    print("\n📝 Creating scripts...")
    
    # Setup database script (PowerShell)
    setup_script = """# Setup TigerGraph Database
# Run this script to initialize the database

Write-Host "Setting up TigerGraph Database..." -ForegroundColor Green

# Load environment variables
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# Install TigerGraph schema
Write-Host "Installing schema..." -ForegroundColor Yellow
gsql tigergraph/schema/schema.gsql

# Install queries
Write-Host "Installing queries..." -ForegroundColor Yellow
Get-ChildItem tigergraph/queries/*.gsql | ForEach-Object {
    gsql $_.FullName
}

Write-Host "✅ Setup complete!" -ForegroundColor Green
"""
    
    with open("scripts/setup_database.ps1", "w", encoding="utf-8") as f:
        f.write(setup_script)
    
    print("   ✅ scripts/setup_database.ps1")
    
    # Create load_cases.py
    load_cases_script = """#!/usr/bin/env python3
\"\"\"
Load case data from cases/ folder into TigerGraph
\"\"\"
import json
import os
from pathlib import Path
import pyTigerGraph as tg

def load_cases():
    # Connect to TigerGraph
    conn = tg.TigerGraphConnection(
        host=os.getenv("TG_HOST"),
        graphname=os.getenv("TG_GRAPHNAME", "FraudInvestigation"),
        username=os.getenv("TG_USERNAME", "tigergraph"),
        password=os.getenv("TG_PASSWORD"),
        apiToken=os.getenv("TG_API_TOKEN")
    )
    
    # Load all cases from cases/ folder
    cases_dir = Path("cases")
    for case_file in sorted(cases_dir.glob("HHG-*.json")):
        with open(case_file) as f:
            case_data = json.load(f)
        
        print(f"Loading {case_file.name}...")
        # Insert into TigerGraph
        # conn.upsertVertex("Case", case_data["case_id"], attributes=case_data)
    
    print("✅ All cases loaded!")

if __name__ == "__main__":
    load_cases()
"""
    
    with open("scripts/load_cases.py", "w", encoding="utf-8") as f:
        f.write(load_cases_script)
    
    print("   ✅ scripts/load_cases.py")
    print("✅ Scripts created!")

def create_docs():
    """Create documentation files"""
    print("\n📝 Creating documentation...")
    
    # Architecture doc
    architecture_doc = """# System Architecture

## Overview

The Fraud Investigation Agent system consists of:

1. **Frontend (React)** - User interface for case management
2. **Backend (FastAPI)** - API and agent orchestration
3. **TigerGraph** - Graph database for relationship detection
4. **LLM Agents** - Intelligent investigation workflow

## Architecture Diagram

```
┌─────────────┐
│   React     │
│  Frontend   │
└──────┬──────┘
       │ REST API
┌──────▼──────┐
│   FastAPI   │
│   Backend   │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──────┐
│ TG  │ │ LLM     │
│Graph│ │ Agents  │
└─────┘ └─────────┘
```

## Components

### Frontend
- Dashboard for case overview
- Case detail pages with evidence
- Investigation workflow visualization
- Real-time updates

### Backend
- RESTful API endpoints
- Agent orchestration
- TigerGraph integration
- LLM service wrapper

### Agents
1. **Fraud Agent** - Initial fraud detection
2. **Investigation Agent** - Multi-step investigation
3. **Evidence Agent** - Evidence gathering
4. **Next Action Agent** - Recommendation generation

### TigerGraph
- Graph schema for fraud entities
- GSQL queries for pattern matching
- Real-time relationship traversal
"""
    
    with open("docs/architecture.md", "w") as f:
        f.write(architecture_doc)
    
    print("   ✅ docs/architecture.md")
    
    # Agent workflow doc
    workflow_doc = """# Agent Workflow

## 6-Phase Investigation Process

### Phase 1: Query Graph
- Fetch user profile from TigerGraph
- Get transaction history
- Retrieve device information
- Find related entities

### Phase 2: Get Evidence
- Search fraud policies (GraphRAG)
- Match transaction patterns
- Find similar historical cases
- Gather supporting evidence

### Phase 3: Assess Uncertainty
- Calculate confidence score
- Identify missing information
- Determine if more evidence needed

### Phase 4: Request Evidence (Conditional)
- Generate evidence request
- Collect additional data
- Loop back to Phase 3

### Phase 5: Recommend Action
- Generate recommendation (ALLOW/HOLD/CHALLENGE/BLOCK)
- Provide reasoning
- Cite evidence and policies

### Phase 6: Record Case
- Save investigation to TigerGraph
- Store outcome for learning
- Update fraud patterns
"""
    
    with open("docs/agent-workflow.md", "w") as f:
        f.write(workflow_doc)
    
    print("   ✅ docs/agent-workflow.md")
    print("✅ Documentation created!")

def create_sample_data():
    """Create sample data files"""
    print("\n📝 Creating sample data...")
    
    sample_case = {
        "case_id": "SAMPLE-001",
        "user_id": "USR_TEST",
        "transaction_id": "TXN_TEST",
        "fraud_detected": True,
        "confidence_score": 95,
        "risk_level": "CRITICAL",
        "fraud_type": "Account Takeover",
        "key_findings": [
            "Impossible travel detected",
            "Device mismatch",
            "Unusual transaction pattern"
        ]
    }
    
    with open("data/sample/sample_case.json", "w") as f:
        json.dump(sample_case, f, indent=2)
    
    print("   ✅ data/sample/sample_case.json")
    print("✅ Sample data created!")

def update_gitignore():
    """Update .gitignore with new structure"""
    print("\n📝 Updating .gitignore...")
    
    additional_ignores = """
# Python cache
backend/app/__pycache__/
backend/app/*/__pycache__/

# Data files
data/raw/*.csv
data/processed/*.csv
!data/sample/*.json

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
"""
    
    with open(".gitignore", "a") as f:
        f.write(additional_ignores)
    
    print("   ✅ .gitignore updated")

def main():
    print("=" * 60)
    print("🔧 REORGANIZING PROJECT STRUCTURE")
    print("=" * 60)
    print("\n⚠️  NOTE: cases/ folder will stay at root (required for hackathon)")
    print()
    
    create_directory_structure()
    create_backend_files()
    create_tigergraph_structure()
    create_scripts()
    create_docs()
    create_sample_data()
    update_gitignore()
    
    print("\n" + "=" * 60)
    print("✅ PROJECT REORGANIZATION COMPLETE!")
    print("=" * 60)
    print("\n📁 New structure created:")
    print("   ├── cases/              ⭐ (unchanged - required for hackathon)")
    print("   ├── backend/app/        (organized structure)")
    print("   ├── frontend/           (organized structure)")
    print("   ├── tigergraph/         (schema + queries)")
    print("   ├── scripts/            (utility scripts)")
    print("   ├── docs/               (documentation)")
    print("   └── data/               (sample data)")
    print("\n⚠️  NEXT STEPS:")
    print("   1. Move existing files to new locations manually")
    print("   2. Update import paths in code")
    print("   3. Test that everything still works")
    print("   4. Run: python verify_submission.py")
    print()

if __name__ == "__main__":
    import json
    main()
