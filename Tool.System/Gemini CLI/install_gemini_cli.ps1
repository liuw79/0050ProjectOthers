# ===================================================
# Gemini CLI Installation Assistant
# ===================================================

Write-Host "This assistant will guide you through installing Gemini CLI." -ForegroundColor Green
Write-Host ""

# --- Step 1: Check Node.js ---
Write-Host "--- 1. Checking for Node.js (version 18+ required) ---" -ForegroundColor Cyan
try {
    $nodeVersion = (node -v) -replace 'v',''
    Write-Host "Found Node.js version: $nodeVersion" -ForegroundColor Green
    $majorVersion = [int]$nodeVersion.Split('.')[0]
    if ($majorVersion -lt 18) {
        Write-Error "Node.js version 18 or higher is required. Please upgrade your Node.js installation from https://nodejs.org/"
        exit
    }
} catch {
    Write-Error "Node.js is not installed or not in your PATH. Please install Node.js 18 or higher from: https://nodejs.org/"
    exit
}

# --- Step 2: Install Gemini CLI ---
Write-Host ""
Write-Host "--- 2. Installing Gemini CLI ---" -ForegroundColor Cyan
Write-Host "Attempting to install Gemini CLI globally using npm..."
Write-Host ""

try {
    npm install -g @google/gemini-cli
    Write-Host "[SUCCESS] Gemini CLI appears to be installed successfully!" -ForegroundColor Green
} catch {
    Write-Error "npm installation failed. This might be due to network issues or permissions. Try running this script as an Administrator."
    Write-Host "As an alternative, you can run Gemini CLI directly using npx: npx https://github.com/google-gemini/gemini-cli" -ForegroundColor Yellow
    exit
}

# --- Step 3: Configuration ---
Write-Host ""
Write-Host "--- 3. How to Configure ---" -ForegroundColor Cyan
Write-Host "To start using Gemini, open a NEW terminal and type: gemini"
Write-Host "A browser window should open for you to log in with your Google account."
Write-Host ""
Write-Host "For advanced use, you may need an API Key. To get one:"
Write-Host "1. Visit Google AI Studio: https://aistudio.google.com/app/apikey"
Write-Host "2. Set it as an environment variable. Run this in your PowerShell terminal:"
Write-Host '   $env:GEMINI_API_KEY="YOUR_API_KEY"' -ForegroundColor Magenta
Write-Host "   [SECURITY WARNING] Do NOT save your API key directly in scripts or text files." -ForegroundColor Red
Write-Host "   Use environment variables as recommended for better security." -ForegroundColor Red
Write-Host "   (Replace YOUR_API_KEY with your actual key)"
Write-Host "To make it permanent, add it to your PowerShell profile or system environment variables."

Write-Host ""
Write-Host "Installation guide finished."
Read-Host -Prompt "Press Enter to exit..."