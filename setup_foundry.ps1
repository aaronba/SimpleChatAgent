# Setup script for Azure AI Foundry Agent Service integration
# Run this in PowerShell

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Azure AI Foundry Setup Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
Write-Host "`n[2/5] Installing Azure AI Foundry packages..." -ForegroundColor Yellow
$packages = @(
    "agent-framework",
    "azure-identity",
    "azure-ai-projects"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    pip install $package --quiet
}
Write-Host "  ✓ Packages installed" -ForegroundColor Green

# Step 3: Check Azure CLI
Write-Host "`n[3/5] Checking Azure CLI..." -ForegroundColor Yellow
$azVersion = az --version 2>&1 | Select-String "azure-cli"
if ($azVersion) {
    Write-Host "  ✓ Azure CLI found" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Azure CLI not found. Install from: https://aka.ms/azure-cli" -ForegroundColor Yellow
}

# Step 4: Check Azure login
Write-Host "`n[4/5] Checking Azure authentication..." -ForegroundColor Yellow
$azAccount = az account show 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Logged in to Azure" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Not logged in to Azure. Run: az login" -ForegroundColor Yellow
}

# Step 5: Setup .env file
Write-Host "`n[5/5] Setting up environment file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ⚠ .env file already exists, skipping" -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "  ✓ Created .env file from template" -ForegroundColor Green
    Write-Host "  → Please edit .env and add your Azure AI Foundry settings" -ForegroundColor Cyan
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your Azure AI Foundry settings:" -ForegroundColor White
Write-Host "   - AZURE_AI_PROJECT_ENDPOINT" -ForegroundColor Gray
Write-Host "   - AZURE_AI_MODEL_DEPLOYMENT_NAME" -ForegroundColor Gray
Write-Host "`n2. If not logged in, run:" -ForegroundColor White
Write-Host "   az login" -ForegroundColor Gray
Write-Host "`n3. Test the setup:" -ForegroundColor White
Write-Host "   python foundry_examples.py" -ForegroundColor Gray
Write-Host "`n4. Run the agent:" -ForegroundColor White
Write-Host "   python app_with_foundry.py" -ForegroundColor Gray
Write-Host ""
