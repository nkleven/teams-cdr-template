import { setupFirstRunExperience } from './passkey';

// Mock CDR Data
const mockCDRs = [
  { id: "CDR-1001", timestamp: "2023-10-27 09:15:22", source: "+15550101", dest: "+15550102", duration: "00:05:23", status: "Success", quality: "Good" },
  { id: "CDR-1002", timestamp: "2023-10-27 09:20:05", source: "+15550103", dest: "+15550104", duration: "00:00:00", status: "Failed", quality: "N/A" },
  { id: "CDR-1003", timestamp: "2023-10-27 09:45:11", source: "+15550105", dest: "+15550101", duration: "00:12:45", status: "Success", quality: "Fair" },
  { id: "CDR-1004", timestamp: "2023-10-27 10:05:30", source: "+15550102", dest: "+15550199", duration: "00:02:10", status: "Success", quality: "Good" },
  { id: "CDR-1005", timestamp: "2023-10-27 10:15:00", source: "+15550108", dest: "+15550109", duration: "00:00:45", status: "Dropped", quality: "Poor" },
];

// Gamification State
let setupProgress = 0;
const totalSteps = 3;

async function initApp() {
  setupThemeToggle();
  
  // Check if setup is complete
  const isSetupComplete = localStorage.getItem('isSetupComplete');
  
  if (!isSetupComplete) {
    // Start Wizard
    await setupFirstRunExperience(); // Passkey first
    renderSetupWizard();
  } else {
    renderDashboard();
  }
}

function setupThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  const body = document.body;
  const currentTheme = localStorage.getItem('theme');
  
  if (currentTheme === 'dark') {
    body.setAttribute('data-theme', 'dark');
    if (toggleBtn) toggleBtn.textContent = 'Light Mode';
  }

  toggleBtn?.addEventListener('click', () => {
    if (body.getAttribute('data-theme') === 'dark') {
      body.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
      toggleBtn.textContent = 'Dark Mode';
    } else {
      body.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      toggleBtn.textContent = 'Light Mode';
    }
  });
}

// --- Setup Wizard Logic ---

function renderSetupWizard() {
  const app = document.getElementById('app');
  if (!app) return;
  
  // Show gamification badge in header
  const badge = document.getElementById('user-badge-area');
  if (badge) badge.style.display = 'inline-block';

  app.innerHTML = `
    <div class="card" style="max-width: 600px; margin: 40px auto; text-align: center;">
      <div class="wizard-steps">
        <div class="step-indicator active" id="step-1-ind">1</div>
        <div class="step-indicator" id="step-2-ind">2</div>
        <div class="step-indicator" id="step-3-ind">3</div>
      </div>
      
      <h2 style="margin-bottom: 8px;">Welcome to CDR Dashboard</h2>
      <p style="color: var(--neutral-secondary); margin-bottom: 24px;">Let's get your environment ready in 3 simple steps.</p>
      
      <div id="wizard-content">
        <!-- Step 1 Content -->
        <div class="fui-input-group">
          <label class="fui-label">Organization Name</label>
          <input type="text" class="fui-input" id="org-name" placeholder="e.g. Contoso Ltd.">
        </div>
        <div class="fui-input-group">
          <label class="fui-label">Primary Region</label>
          <select class="fui-input" id="org-region">
            <option>North America</option>
            <option>Europe</option>
            <option>Asia Pacific</option>
          </select>
        </div>
        
        <div style="margin-top: 32px; display: flex; justify-content: flex-end;">
          <button class="fui-btn fui-btn-primary" id="next-btn-1">Next: Connect Data</button>
        </div>
      </div>
    </div>
  `;

  document.getElementById('next-btn-1')?.addEventListener('click', () => {
    const orgNameInput = document.getElementById('org-name') as HTMLInputElement;
    const orgName = orgNameInput.value;
    if (orgName) {
      localStorage.setItem('orgName', orgName);
      advanceWizard(2);
    } else {
      alert('Please enter an organization name.');
    }
  });
}

function advanceWizard(step: number) {
  const content = document.getElementById('wizard-content');
  const ind1 = document.getElementById('step-1-ind');
  const ind2 = document.getElementById('step-2-ind');
  const ind3 = document.getElementById('step-3-ind');

  if (step === 2) {
    ind1?.classList.add('completed');
    ind1?.classList.remove('active');
    ind2?.classList.add('active');
    
    if (content) {
      content.innerHTML = `
        <h3 style="margin-top: 0;">Connect Data Source</h3>
        <p style="font-size: 14px; color: var(--neutral-secondary);">We need to connect to your SIP trunk or SBC logs.</p>
        
        <div style="background-color: var(--neutral-lighter); padding: 16px; border-radius: 4px; margin-bottom: 24px; text-align: left;">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <input type="radio" name="source" checked style="margin-right: 8px;">
                <strong>Upload Sample Data (Scaffolding)</strong>
            </div>
            <div style="display: flex; align-items: center;">
                <input type="radio" name="source" disabled style="margin-right: 8px;">
                <span style="color: var(--neutral-tertiary);">Connect Live SBC (Premium)</span>
            </div>
        </div>

        <div style="margin-top: 32px; display: flex; justify-content: space-between;">
          <button class="fui-btn fui-btn-standard" disabled>Back</button>
          <button class="fui-btn fui-btn-primary" id="next-btn-2">Import Data</button>
        </div>
      `;
      
      document.getElementById('next-btn-2')?.addEventListener('click', () => {
        // Simulate data loading
        const btn = document.getElementById('next-btn-2') as HTMLButtonElement;
        btn.textContent = 'Importing...';
        setTimeout(() => {
            advanceWizard(3);
        }, 1000);
      });
    }
  } else if (step === 3) {
    ind2?.classList.add('completed');
    ind2?.classList.remove('active');
    ind3?.classList.add('active');
    
    if (content) {
      content.innerHTML = `
        <h3 style="margin-top: 0;">You're All Set!</h3>
        <div style="font-size: 48px; margin: 20px 0;">🎉</div>
        <p>You've earned the <strong>"System Architect"</strong> badge.</p>
        
        <div class="badge-container" style="justify-content: center; margin-bottom: 24px;">
            <span class="badge earned">System Architect</span>
            <span class="badge">Data Analyst</span>
            <span class="badge">Troubleshooter</span>
        </div>

        <div style="margin-top: 32px; display: flex; justify-content: flex-end;">
          <button class="fui-btn fui-btn-primary" id="finish-btn">Go to Dashboard</button>
        </div>
      `;
      
      document.getElementById('finish-btn')?.addEventListener('click', () => {
        localStorage.setItem('isSetupComplete', 'true');
        renderDashboard();
      });
    }
  }
}


// --- Main Dashboard Logic ---

function renderDashboard() {
  const app = document.getElementById('app');
  const orgName = localStorage.getItem('orgName') || 'My Organization';
  
  // Hide wizard badge
  const badge = document.getElementById('user-badge-area');
  if (badge) badge.style.display = 'none';

  if (!app) return;

  app.innerHTML = `
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h2 style="margin: 0;">${orgName} Overview</h2>
        <div class="badge-container">
            <span class="badge earned">System Architect</span>
            <span class="badge">Level 1</span>
        </div>
      </div>

      <div class="tabs">
        <div class="tab active" id="tab-dashboard">Calls</div>
        <div class="tab" id="tab-admin">Admin</div>
      </div>
      
      <div id="tab-content">
        ${getDashboardContent()}
      </div>
    </div>
  `;

  document.getElementById('tab-dashboard')?.addEventListener('click', () => switchTab('dashboard'));
  document.getElementById('tab-admin')?.addEventListener('click', () => switchTab('admin'));
}

function switchTab(tabName: string) {
  const dashboardTab = document.getElementById('tab-dashboard');
  const adminTab = document.getElementById('tab-admin');
  const contentArea = document.getElementById('tab-content');

  if (tabName === 'dashboard') {
    dashboardTab?.classList.add('active');
    adminTab?.classList.remove('active');
    if (contentArea) contentArea.innerHTML = getDashboardContent();
  } else {
    dashboardTab?.classList.remove('active');
    adminTab?.classList.add('active');
    if (contentArea) contentArea.innerHTML = getAdminContent();
  }
}

function getDashboardContent() {
  const rows = mockCDRs.map(cdr => {
    const statusColor = cdr.status === 'Success' ? 'var(--success)' : 'var(--error)';
    return `
      <tr>
        <td>${cdr.id}</td>
        <td>${cdr.timestamp}</td>
        <td>${cdr.source}</td>
        <td>${cdr.dest}</td>
        <td>${cdr.duration}</td>
        <td style="color: ${statusColor}; font-weight: 600;">${cdr.status}</td>
        <td>${cdr.quality}</td>
        <td><button class="fui-btn fui-btn-standard" style="height: 24px; min-width: 60px; font-size: 12px;" onclick="alert('Viewing details for ${cdr.id}')">View</button></td>
      </tr>
    `;
  }).join('');

  return `
    <div style="display: flex; gap: 16px; margin-bottom: 24px;">
        <div style="flex: 1; background: var(--neutral-lighter); padding: 16px; border-radius: 4px;">
            <div style="font-size: 12px; color: var(--neutral-secondary); font-weight: 600;">TOTAL CALLS</div>
            <div style="font-size: 24px; font-weight: 600;">1,245</div>
        </div>
        <div style="flex: 1; background: var(--neutral-lighter); padding: 16px; border-radius: 4px;">
            <div style="font-size: 12px; color: var(--neutral-secondary); font-weight: 600;">SUCCESS RATE</div>
            <div style="font-size: 24px; font-weight: 600; color: var(--success);">98.2%</div>
        </div>
        <div style="flex: 1; background: var(--neutral-lighter); padding: 16px; border-radius: 4px;">
            <div style="font-size: 12px; color: var(--neutral-secondary); font-weight: 600;">AVG DURATION</div>
            <div style="font-size: 24px; font-weight: 600;">4m 12s</div>
        </div>
    </div>

    <h3 style="font-size: 16px; margin-bottom: 12px;">Recent Call Logs</h3>
    <table style="margin-bottom: 32px;">
      <thead>
        <tr>
          <th>ID</th>
          <th>Time</th>
          <th>Source</th>
          <th>Destination</th>
          <th>Duration</th>
          <th>Status</th>
          <th>Quality</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>
    
    <h3 style="font-size: 16px; margin-bottom: 12px;">Diagnostic Visualization</h3>
    <div class="sip-ladder">
        <div class="sip-flow-row">
          <div class="sip-actor">Caller</div>
          <div class="sip-actor">SBC</div>
          <div class="sip-actor">Teams Proxy</div>
        </div>
        
        <div class="sip-flow-row">
          <div style="width: 120px;"></div>
          <div class="sip-arrow"><span class="sip-label">INVITE</span></div>
          <div style="width: 120px;"></div>
        </div>
        
        <div class="sip-flow-row">
          <div style="width: 120px;"></div>
          <div class="sip-arrow left"><span class="sip-label">100 Trying</span></div>
          <div style="width: 120px;"></div>
        </div>
        
        <div class="sip-flow-row">
          <div style="width: 120px;"></div>
          <div style="flex:1"></div>
          <div class="sip-arrow"><span class="sip-label">INVITE</span></div>
        </div>
        
        <div class="sip-flow-row">
          <div style="width: 120px;"></div>
          <div style="flex:1"></div>
          <div class="sip-arrow left"><span class="sip-label">404 Not Found</span></div>
        </div>
    </div>
  `;
}

function getAdminContent() {
  return `
    <h3 style="font-size: 16px; margin-bottom: 16px;">System Administration</h3>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
        <div style="border: 1px solid var(--neutral-light); padding: 16px; border-radius: 4px;">
            <h4 style="margin-top: 0;">User Management</h4>
            <table style="margin-bottom: 16px;">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Role</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>admin@contoso.com</td>
                  <td>Global Admin</td>
                  <td style="color: var(--success); font-weight: 600;">Active</td>
                </tr>
                <tr>
                  <td>operator@contoso.com</td>
                  <td>Viewer</td>
                  <td style="color: var(--success); font-weight: 600;">Active</td>
                </tr>
              </tbody>
            </table>
            <button class="fui-btn fui-btn-standard">Add User</button>
        </div>

        <div style="border: 1px solid var(--neutral-light); padding: 16px; border-radius: 4px;">
            <h4 style="margin-top: 0;">Data Retention</h4>
            <div class="fui-input-group">
                <label class="fui-label">Retention Period (Days)</label>
                <input type="number" class="fui-input" value="90">
            </div>
            <div style="display: flex; gap: 8px;">
                <button class="fui-btn fui-btn-primary">Save Policy</button>
                <button class="fui-btn fui-btn-standard" style="color: var(--error); border-color: var(--error);">Purge Now</button>
            </div>
        </div>
    </div>
  `;
}

initApp();
