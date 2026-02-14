const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

console.log('🔍 Azure Static Web Apps Diagnostic Tool\n');

// Diagnostic checks
const diagnostics = {
    // Check 1: Verify required files exist
    checkRequiredFiles() {
        console.log('📁 Checking required files...');
        const requiredFiles = [
            'index.html',
            'staticwebapp.config.json',
            'styles.css',
            'script.js'
        ];
        
        let allFilesPresent = true;
        requiredFiles.forEach(file => {
            const exists = fs.existsSync(path.join(__dirname, file));
            console.log(`  ${exists ? '✅' : '❌'} ${file}`);
            if (!exists) allFilesPresent = false;
        });
        
        return allFilesPresent;
    },

    // Check 2: Validate SWA configuration
    validateSWAConfig() {
        console.log('\n⚙️ Validating SWA configuration...');
        try {
            const config = JSON.parse(fs.readFileSync('staticwebapp.config.json', 'utf8'));
            console.log('  ✅ Configuration is valid JSON');
            
            // Check for routes
            if (config.routes) {
                console.log(`  ✅ Routes configured: ${config.routes.length} route(s)`);
            }
            
            // Check for headers
            if (config.globalHeaders) {
                console.log('  ✅ Global headers configured');
            }
            
            return true;
        } catch (error) {
            console.log('  ❌ Configuration error:', error.message);
            return false;
        }
    },

    // Check 3: Test local server
    async testLocalServer(port = 4280) {
        console.log(`\n🌐 Testing local server on port ${port}...`);
        
        return new Promise((resolve) => {
            const options = {
                hostname: 'localhost',
                port: port,
                path: '/',
                method: 'GET',
                timeout: 5000
            };

            const req = http.request(options, (res) => {
                console.log(`  ✅ Server responding (Status: ${res.statusCode})`);
                resolve(true);
            });

            req.on('error', (error) => {
                console.log('  ❌ Server not running. Start with: npm run swa:start');
                resolve(false);
            });

            req.on('timeout', () => {
                console.log('  ❌ Server timeout');
                req.destroy();
                resolve(false);
            });

            req.end();
        });
    },

    // Check 4: Validate HTML structure
    validateHTML() {
        console.log('\n📄 Validating HTML structure...');
        const html = fs.readFileSync('index.html', 'utf8');
        
        const checks = [
            { pattern: /<meta.*viewport/i, name: 'Viewport meta tag' },
            { pattern: /<section.*id="hero"/i, name: 'Hero section' },
            { pattern: /<form.*id="rsvpForm"/i, name: 'RSVP form' },
            { pattern: /<script.*src="script.js"/i, name: 'JavaScript file linked' },
            { pattern: /<link.*href="styles.css"/i, name: 'CSS file linked' }
        ];
        
        let allChecksPassed = true;
        checks.forEach(check => {
            const exists = check.pattern.test(html);
            console.log(`  ${exists ? '✅' : '❌'} ${check.name}`);
            if (!exists) allChecksPassed = false;
        });
        
        return allChecksPassed;
    },

    // Check 5: Test SWA CLI installation
    checkSWACLI() {
        console.log('\n🛠️ Checking SWA CLI installation...');
        const { execSync } = require('child_process');
        
        try {
            const version = execSync('swa --version', { encoding: 'utf8' });
            console.log(`  ✅ SWA CLI installed (${version.trim()})`);
            return true;
        } catch (error) {
            console.log('  ❌ SWA CLI not installed. Install with: npm install -g @azure/static-web-apps-cli');
            return false;
        }
    },

    // Check 6: Performance metrics
    checkPerformance() {
        console.log('\n⚡ Checking performance metrics...');
        
        const fileSizes = {
            'index.html': 10000,  // 10KB warning threshold
            'styles.css': 50000,  // 50KB warning threshold
            'script.js': 30000    // 30KB warning threshold
        };
        
        let performanceOk = true;
        Object.entries(fileSizes).forEach(([file, threshold]) => {
            try {
                const stats = fs.statSync(file);
                const size = stats.size;
                const sizeKB = (size / 1024).toFixed(2);
                
                if (size > threshold) {
                    console.log(`  ⚠️ ${file}: ${sizeKB}KB (exceeds ${threshold/1024}KB threshold)`);
                    performanceOk = false;
                } else {
                    console.log(`  ✅ ${file}: ${sizeKB}KB`);
                }
            } catch (error) {
                console.log(`  ❌ ${file}: File not found`);
            }
        });
        
        return performanceOk;
    }
};

// Run all diagnostics
async function runDiagnostics() {
    console.log('Starting diagnostics...\n');
    console.log('=' .repeat(50));
    
    const results = {
        files: diagnostics.checkRequiredFiles(),
        config: diagnostics.validateSWAConfig(),
        html: diagnostics.validateHTML(),
        performance: diagnostics.checkPerformance(),
        cli: diagnostics.checkSWACLI(),
        server: await diagnostics.testLocalServer()
    };
    
    console.log('\n' + '='.repeat(50));
    console.log('\n📊 Diagnostic Summary:');
    
    const passed = Object.values(results).filter(r => r).length;
    const total = Object.keys(results).length;
    
    console.log(`\nTests passed: ${passed}/${total}`);
    
    if (passed === total) {
        console.log('\n✅ All checks passed! Your site is ready for Azure deployment.');
        console.log('\nNext steps:');
        console.log('1. Run locally: npm run swa:start');
        console.log('2. Deploy to Azure: npm run swa:deploy');
    } else {
        console.log('\n⚠️ Some checks failed. Please fix the issues above.');
        console.log('\nQuick fixes:');
        if (!results.cli) {
            console.log('- Install SWA CLI: npm install -g @azure/static-web-apps-cli');
        }
        if (!results.server) {
            console.log('- Start local server: npm run swa:start');
        }
        if (!results.files) {
            console.log('- Ensure all required files are present');
        }
    }
}

// Run diagnostics
runDiagnostics().catch(console.error);
