# Setup TigerGraph Database
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
