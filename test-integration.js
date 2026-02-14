const http = require('http');
const assert = require('assert');

const BASE_URL = 'http://localhost:4280';

// Test suite for SWA integration
const tests = [
    {
        name: 'Homepage loads successfully',
        async test() {
            const response = await fetch(`${BASE_URL}/`);
            assert.equal(response.status, 200, 'Homepage should return 200');
            const text = await response.text();
            assert(text.includes('Kelli') && text.includes('Nathan'), 'Homepage should contain wedding names');
        }
    },
    {
        name: 'Static assets are served correctly',
        async test() {
            const assets = ['/styles.css', '/script.js'];
            for (const asset of assets) {
                const response = await httpGet(`${BASE_URL}${asset}`);
                assert.equal(response.status, 200, `${asset} should be served`);
            }
        }
    },
    {
        name: 'SWA configuration is applied',
        async test() {
            const response = await httpGet(`${BASE_URL}/nonexistent`);
            // Should return index.html due to navigation fallback
            assert.equal(response.status, 200, 'Non-existent routes should return 200');
        }
    },
    {
        name: 'Security headers are present',
        async test() {
            const response = await httpGet(`${BASE_URL}/`);
            const headers = response.headers;
            assert(headers.get('x-content-type-options'), 'Security headers should be present');
        }
    }
];

// Run tests
async function runTests() {
    console.log('🧪 Running Azure SWA Integration Tests\n');
    
    let passed = 0;
    let failed = 0;
    
    for (const test of tests) {
        try {
            await test.test();
            console.log(`✅ ${test.name}`);
            passed++;
        } catch (error) {
            console.log(`❌ ${test.name}`);
            console.log(`   Error: ${error.message}`);
            failed++;
        }
    }
    
    console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
    process.exit(failed > 0 ? 1 : 0);
}

// Helper function for HTTP requests
function httpGet(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                resolve({
                    status: res.statusCode,
                    headers: {
                        get: (name) => res.headers[name.toLowerCase()]
                    },
                    text: async () => data
                });
            });
        }).on('error', reject);
    });
}

// Wait a moment for server to be ready, then run tests
setTimeout(runTests, 2000);
