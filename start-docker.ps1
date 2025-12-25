# Bio-Watcher Docker Launcher
# Run this to start everything!

Write-Host "`n🏥 BIO-WATCHER: Starting with Docker`n" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Gray

# Check if Docker is running
Write-Host "`n🔍 Checking Docker..." -ForegroundColor Yellow
$dockerRunning = docker ps 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not running!" -ForegroundColor Red
    Write-Host "   Please start Docker Desktop and try again.`n" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Docker is running`n" -ForegroundColor Green

# Check .env file
Write-Host "🔍 Checking configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Copying from .env.example...`n" -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}
Write-Host "✅ Configuration found`n" -ForegroundColor Green

# Build containers
Write-Host "🔨 Building Docker containers..." -ForegroundColor Yellow
Write-Host "   (This may take 5-10 minutes on first run)`n" -ForegroundColor Gray
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Build failed! Check errors above.`n" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Build successful!`n" -ForegroundColor Green

# Start containers
Write-Host "🚀 Starting containers..." -ForegroundColor Yellow
Write-Host "   Press Ctrl+C to stop`n" -ForegroundColor Gray

docker-compose up

Write-Host "`n`n👋 Shutting down...`n" -ForegroundColor Cyan
