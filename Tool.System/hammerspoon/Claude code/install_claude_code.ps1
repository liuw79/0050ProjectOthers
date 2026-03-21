# Claude Code Installation Script
# Author: AI Assistant
# Version: 1.2
# Description: Auto install Claude Code CLI tool

Write-Host "=== Claude Code Installation Script ===" -ForegroundColor Green
Write-Host ""

# Check Node.js version
Write-Host "Checking Node.js version..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "Current Node.js version: $nodeVersion" -ForegroundColor Green
    
    # Extract version number and check if >= 18
    $versionNumber = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
    if ($versionNumber -lt 18) {
        Write-Host "Error: Claude Code requires Node.js 18 or higher" -ForegroundColor Red
        Write-Host "Please visit https://nodejs.org to download latest version" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "Error: Node.js not found" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ first" -ForegroundColor Yellow
    Write-Host "Download: https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check npm availability
Write-Host "Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: npm not available" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Install Claude Code (using correct package name)
Write-Host "Installing Claude Code..." -ForegroundColor Yellow

try {
    npm install -g @anthropic-ai/claude-code
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Success: Claude Code installed successfully!" -ForegroundColor Green
    } else {
        throw "Installation failed"
    }
} catch {
    Write-Host "Official registry failed, trying China mirror..." -ForegroundColor Yellow
    
    # Set China mirror
    npm config set registry https://registry.npmmirror.com
    
    try {
        npm install -g @anthropic-ai/claude-code
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Success: Claude Code installed with China mirror!" -ForegroundColor Green
        } else {
            throw "China mirror installation also failed"
        }
    } catch {
        Write-Host "Installation failed!" -ForegroundColor Red
        Write-Host "" 
        Write-Host "Possible reasons:" -ForegroundColor Yellow
        Write-Host "1. Network connection issues" -ForegroundColor White
        Write-Host "2. npm permission issues" -ForegroundColor White
        Write-Host "3. Firewall or proxy settings" -ForegroundColor White
        Write-Host "" 
        Write-Host "Alternative solutions:" -ForegroundColor Cyan
        Write-Host "- Claude Web: https://claude.ai" -ForegroundColor White
        Write-Host "- Cursor IDE: https://cursor.sh" -ForegroundColor White
        Write-Host "- VS Code Extensions: Search 'Claude' or 'Continue'" -ForegroundColor White
        
        # Restore official registry
        npm config set registry https://registry.npmjs.org
        exit 1
    } finally {
        # Restore official registry
        npm config set registry https://registry.npmjs.org
    }
}

Write-Host ""
Write-Host "=== Configuration Instructions ===" -ForegroundColor Green
Write-Host "1. Open a new PowerShell terminal" -ForegroundColor White
Write-Host "2. Run command: claude" -ForegroundColor Cyan
Write-Host "3. First run will prompt OAuth authentication" -ForegroundColor White
Write-Host "4. Choose login method:" -ForegroundColor White
Write-Host "   - Option 1: Claude account subscription (Pro $20/month recommended)" -ForegroundColor Yellow
Write-Host "   - Option 2: Anthropic Console API account (pay-per-use)" -ForegroundColor Yellow
Write-Host ""
Write-Host "=== Important Notes ===" -ForegroundColor Red
Write-Host "• Claude Code requires Claude Pro or Max subscription" -ForegroundColor White
Write-Host "• Stable overseas network environment required" -ForegroundColor White
Write-Host "• Recommend US, UK, or Canada VPN nodes" -ForegroundColor White
Write-Host ""
Write-Host "Installation complete! Run 'claude' in new terminal to start" -ForegroundColor Green