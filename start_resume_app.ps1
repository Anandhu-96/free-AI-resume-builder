# Start the Resume AI Streamlit app and open the landing page
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath
Write-Host "Starting Streamlit app..."
Start-Process -NoNewWindow -FilePath "streamlit" -ArgumentList "run page.py" 
Start-Sleep -Seconds 2
$index = Join-Path $projectPath "index.html"
if (Test-Path $index) {
    Start-Process "${index}"
} else {
    Write-Host "index.html not found. Open it manually." -ForegroundColor Yellow
}
