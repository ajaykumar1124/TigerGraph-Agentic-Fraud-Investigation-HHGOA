# TigerGraph Agentic Frontend Export Script
# This script creates a distributable package of the React application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TigerGraph Agentic - Frontend Exporter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "[1/5] Installing dependencies..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "[1/5] Dependencies already installed ✓" -ForegroundColor Green
}

# Build the production version
Write-Host "[2/5] Building production version..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed! Please check for errors." -ForegroundColor Red
    exit 1
}

Write-Host "[2/5] Build completed successfully ✓" -ForegroundColor Green

# Create export directory
$exportDir = "TigerGraph-Agentic-Frontend-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Write-Host "[3/5] Creating export package: $exportDir" -ForegroundColor Yellow

New-Item -ItemType Directory -Path $exportDir -Force | Out-Null

# Copy dist folder
Copy-Item -Path "dist" -Destination "$exportDir/dist" -Recurse -Force

# Copy documentation
Copy-Item -Path "README.md" -Destination "$exportDir/README.md" -Force
Copy-Item -Path "ENHANCED_FEATURES.md" -Destination "$exportDir/ENHANCED_FEATURES.md" -Force
Copy-Item -Path "package.json" -Destination "$exportDir/package.json" -Force

# Create deployment instructions
$deploymentInstructions = @"
# TigerGraph Agentic - Frontend Deployment Guide

## Quick Start

This package contains a pre-built production version of the TigerGraph Agentic frontend.

### Option 1: Serve with Node.js

1. Install a simple HTTP server:
   ``````
   npm install -g serve
   ``````

2. Navigate to the dist folder and serve:
   ``````
   cd dist
   serve -s . -p 3000
   ``````

3. Open browser to: http://localhost:3000

### Option 2: Deploy to Netlify

1. Sign up at https://netlify.com
2. Drag and drop the 'dist' folder to Netlify dashboard
3. Your app will be live instantly!

### Option 3: Deploy to Vercel

1. Install Vercel CLI:
   ``````
   npm install -g vercel
   ``````

2. Deploy:
   ``````
   cd dist
   vercel
   ``````

### Option 4: Deploy to GitHub Pages

1. Create a new GitHub repository
2. Push the contents of 'dist' folder to the repository
3. Enable GitHub Pages in repository settings
4. Your app will be available at: https://username.github.io/repo-name

### Option 5: Use with Any Web Server

The 'dist' folder contains static files that can be served by any web server:
- Apache
- Nginx
- IIS
- AWS S3 + CloudFront
- Azure Static Web Apps
- Google Cloud Storage

Simply copy the contents of 'dist' to your web server's public directory.

## Backend Configuration

The frontend expects the backend API to be available at:
- Development: http://localhost:8000
- Production: Update the API base URL in 'dist/assets/index-*.js'

To change the API endpoint, modify 'src/services/api.js' and rebuild.

## Features Included

✓ Dashboard with fraud metrics
✓ Transactions page with real-time monitoring
✓ Analytics dashboard with interactive charts
✓ Case management system
✓ Network visualization
✓ TypeScript type definitions
✓ Responsive design (mobile/tablet/desktop)
✓ Modern banking UI with fraud indicators

## Package Contents

- dist/           - Production build (ready to deploy)
- package.json    - Project dependencies
- README.md       - Project overview
- ENHANCED_FEATURES.md - Detailed feature documentation

## Support

For issues or questions, refer to the main documentation or contact support.

---

**TigerGraph Agentic Fraud Investigation System**
Built with React, TypeScript, and TigerGraph
"@

Set-Content -Path "$exportDir/DEPLOYMENT_GUIDE.md" -Value $deploymentInstructions

Write-Host "[3/5] Files copied successfully ✓" -ForegroundColor Green

# Create a compressed archive
Write-Host "[4/5] Creating ZIP archive..." -ForegroundColor Yellow

$zipFile = "$exportDir.zip"
Compress-Archive -Path $exportDir -DestinationPath $zipFile -Force

$zipSize = (Get-Item $zipFile).Length / 1MB
Write-Host "[4/5] Archive created: $zipFile ($([math]::Round($zipSize, 2)) MB) ✓" -ForegroundColor Green

# Calculate statistics
$fileCount = (Get-ChildItem -Path "$exportDir/dist" -Recurse -File).Count
$totalSize = (Get-ChildItem -Path "$exportDir/dist" -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "[5/5] Package statistics:" -ForegroundColor Yellow
Write-Host "  - Total files: $fileCount" -ForegroundColor White
Write-Host "  - Total size: $([math]::Round($totalSize, 2)) MB" -ForegroundColor White
Write-Host "  - Archive size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor White

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Export completed successfully! ✓" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Package location:" -ForegroundColor Cyan
Write-Host "  Folder: $exportDir" -ForegroundColor White
Write-Host "  Archive: $zipFile" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Extract the ZIP file on your deployment server" -ForegroundColor White
Write-Host "  2. Follow instructions in DEPLOYMENT_GUIDE.md" -ForegroundColor White
Write-Host "  3. Serve the 'dist' folder with any web server" -ForegroundColor White
Write-Host ""
Write-Host "Quick test:" -ForegroundColor Cyan
Write-Host "  npm install -g serve" -ForegroundColor White
Write-Host "  cd $exportDir/dist" -ForegroundColor White
Write-Host "  serve -s . -p 3000" -ForegroundColor White
Write-Host ""
