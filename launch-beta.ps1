# Eden Beta Launch Script
# Automates final checks and beta deployment

Write-Host "🚀 Eden Agent Beta Launch Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Final smoke tests
Write-Host "[1/6] Running final smoke tests..." -ForegroundColor Yellow
npm test
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tests failed! Cannot proceed with beta launch." -ForegroundColor Red
    exit 1
}
Write-Host "✅ All tests passed!" -ForegroundColor Green
Write-Host ""

# Step 2: Check version control status
Write-Host "[2/6] Checking version control status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Uncommitted changes detected:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    $commit = Read-Host "Commit changes before launch? (y/n)"
    if ($commit -eq "y") {
        $message = Read-Host "Commit message"
        git add .
        git commit -m "$message"
        Write-Host "✅ Changes committed!" -ForegroundColor Green
    }
} else {
    Write-Host "✅ Working directory clean!" -ForegroundColor Green
}
Write-Host ""

# Step 3: Verify environment
Write-Host "[3/6] Verifying environment..." -ForegroundColor Yellow
if (Test-Path .env) {
    Write-Host "✅ .env file exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  No .env file found. Creating from .env.example..." -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "✅ .env created. Please configure it before continuing." -ForegroundColor Green
    }
}
Write-Host ""

# Step 4: Check Python dependencies
Write-Host "[4/6] Checking Python environment..." -ForegroundColor Yellow
python --version
if (Test-Path venv) {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "⚠️  No virtual environment detected" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Open beta documentation
Write-Host "[5/6] Preparing beta documentation..." -ForegroundColor Yellow
if (Test-Path BETA_WELCOME.md) {
    Write-Host "✅ Beta welcome document ready" -ForegroundColor Green
}
if (Test-Path BETA_CHECKLIST.md) {
    Write-Host "✅ Beta checklist ready" -ForegroundColor Green
}
Write-Host ""

# Step 6: Launch options
Write-Host "[6/6] Select launch action:" -ForegroundColor Yellow
Write-Host "  1) Open Miner UI in Edge browser" -ForegroundColor White
Write-Host "  2) View test report" -ForegroundColor White
Write-Host "  3) Create beta release tag" -ForegroundColor White
Write-Host "  4) Push to GitHub" -ForegroundColor White
Write-Host "  5) Open beta documentation" -ForegroundColor White
Write-Host "  6) All of the above" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "🌐 Opening Miner UI..." -ForegroundColor Cyan
        Start-Process "msedge" "http://localhost:3000/Miner/ui/index.html"
        npm start
    }
    "2" {
        Write-Host "📊 Opening test report..." -ForegroundColor Cyan
        npx playwright show-report
    }
    "3" {
        Write-Host "🏷️  Creating beta tag..." -ForegroundColor Cyan
        $version = Read-Host "Enter version (e.g., v0.1.0-beta.1)"
        git tag -a $version -m "Beta release $version"
        Write-Host "✅ Tag created: $version" -ForegroundColor Green
        Write-Host "To push tag: git push origin $version" -ForegroundColor Yellow
    }
    "4" {
        Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Cyan
        git push origin main
        $pushTags = Read-Host "Push tags too? (y/n)"
        if ($pushTags -eq "y") {
            git push origin --tags
        }
        Write-Host "✅ Pushed to GitHub!" -ForegroundColor Green
    }
    "5" {
        Write-Host "📖 Opening documentation..." -ForegroundColor Cyan
        code BETA_WELCOME.md
        code BETA_CHECKLIST.md
    }
    "6" {
        Write-Host "🎯 Executing all launch steps..." -ForegroundColor Cyan
        
        # Tag
        $version = Read-Host "Enter version for tag (e.g., v0.1.0-beta.1)"
        git tag -a $version -m "Beta release $version"
        Write-Host "✅ Tag created: $version" -ForegroundColor Green
        
        # Push
        git push origin main
        git push origin --tags
        Write-Host "✅ Pushed to GitHub!" -ForegroundColor Green
        
        # Open docs
        code BETA_WELCOME.md
        code BETA_CHECKLIST.md
        
        # Open test report
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "npx playwright show-report"
        
        # Start UI
        Write-Host "🌐 Opening Miner UI..." -ForegroundColor Cyan
        Start-Process "msedge" "http://localhost:3000/Miner/ui/index.html"
        npm start
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 Beta launch preparation complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Verify the Miner UI is working in Edge" -ForegroundColor White
Write-Host "  2. Share beta documentation with testers" -ForegroundColor White
Write-Host "  3. Monitor GitHub issues for feedback" -ForegroundColor White
Write-Host "  4. Run regular smoke tests" -ForegroundColor White
Write-Host ""
