import codecs
import re

with codecs.open('current_front.html', 'r', 'utf-16') as f:
    content = f.read()

# --- 1. Add Update Data View & JS ---
# 1a. Add TopNav button
update_btn = '''
                    <button id="updateDataBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Update Data
                    </button>
                    <button id="backToDashBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Back to Dashboard
                    </button>
'''
content = content.replace('<button id="refreshBtn"', update_btn.strip() + '\n                    <button id="refreshBtn"')

# 1b. Add View HTML
update_view_html = '''
        <!-- Update Data View -->
        <div id="updateWrapper" class="hidden flex-col gap-6">
            <div class="bg-white rounded-tremor-default border border-tremor-border shadow-tremor-card p-4">
                <h2 class="text-tremor-title font-medium text-tremor-content-strong mb-4">Update Team Data</h2>
                
                <div class="mb-4">
                    <label class="text-sm text-tremor-content">Select Team</label>
                    <select id="updateTeamSelect" class="mt-1 block w-full border border-tremor-border rounded-tremor-default px-3 py-2 text-tremor-content-strong text-sm focus:ring-tremor-brand-DEFAULT focus:border-tremor-brand-DEFAULT shadow-sm">
                    </select>
                </div>

                <div class="flex gap-4 border-b border-tremor-border mb-4">
                    <button id="tabMetrics" class="px-4 py-2 text-sm font-medium text-tremor-brand-DEFAULT border-b-2 border-tremor-brand-DEFAULT">Metrics</button>
                    <button id="tabDetails" class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong">Details</button>
                    <button id="tabConfigs" class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong hidden">Configurations</button>
                </div>

                <!-- Forms Container -->
                <div id="updateFormContainer" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Fields will be dynamically injected here -->
                </div>

                <div class="mt-6 flex justify-end gap-3">
                    <p id="updateMsg" class="text-sm mt-2 hidden"></p>
                    <button id="saveUpdateBtn" class="bg-tremor-brand-DEFAULT text-white px-4 py-2 rounded-tremor-default text-sm font-medium hover:bg-tremor-brand-emphasis shadow-sm">Save Changes</button>
                </div>
            </div>
        </div>
'''
content = content.replace('<div id="dashboardWrapper"', update_view_html.strip() + '\n\n        <div id="dashboardWrapper"')

# 1c. Add Update JS logic (Friendly names mapping included!)
js_logic = '''
        let userRole = null;
        let currentUpdateTab = 'metrics';

        const friendlyNames = {
            'spAssigned': 'Story Points Assigned',
            'spCompleted': 'Story Points Completed',
            'usAssigned': 'User Stories Assigned',
            'usCompleted': 'User Stories Completed',
            'usPushed': 'User Stories Pushed',
            'defectLeakage': 'Defect Leakage (%)',
            'prodIncidents': 'Production Incidents',
            'openRisks': 'Open Risks',
            'escalations': 'Escalations',
            'autoCoverage': 'Automation Coverage (%)',
            'autoStability': 'Automation Stability (%)',
            'autoToolsReq': 'Automation Tools Gap',
            'buildToolsReq': 'Build Tools Gap',
            'sowMilestones': 'SOW Milestones',
            'regRunTime': 'Regression Run Time',
            'regExecTimeNoAuto': 'Regression Exec Time (No Auto)',
            'autoBugs': 'Automation Bugs',
            'kt': 'Knowledge Transfer',
            'assets': 'Assets Created',
            'usAssignedPts': 'US Assigned Details',
            'defectPts': 'Defect Details',
            'incidentPts': 'Incident Details',
            'riskPts': 'Risk Details',
            'sowPts': 'SOW Details',
            'escalationPts': 'Escalation Details',
            'autoToolPts': 'Auto Tool Details',
            'buildToolPts': 'Build Tool Details',
            'cloudProf': 'Cloud Proficiency',
            'cicdSetup': 'CI/CD Setup',
            'ktPrep': 'KT Preparation',
            'autoBugsPts': 'Auto Bugs Details',
            'cicdMat': 'CI/CD Maturity',
            'assetPts': 'Asset Details',
            'deloitteTime': 'Deloitte Time',
            'tenroxTime': 'Tenrox Time',
            'catManager': 'CAT Manager',
            'engagementCode': 'Engagement Code',
            'lobLead': 'LOB Lead',
            'processComp': 'Process Compliance (%)'
        };

        function getFriendlyName(key) {
            let label = key;
            if (key.endsWith('_expected')) {
                const base = key.replace('_expected', '');
                label = (friendlyNames[base] || base) + ' (Expected)';
            } else if (key.endsWith('_variance')) {
                const base = key.replace('_variance', '');
                label = (friendlyNames[base] || base) + ' (Variance)';
            } else {
                label = friendlyNames[key] || key;
            }
            if (label === key) {
                label = label.replace(/([A-Z])/g, ' ').replace(/^./, function(str){ return str.toUpperCase(); });
            }
            return label;
        }

        async function fetchUserMe() {
            const token = localStorage.getItem('token');
            if(!token) return;
            try {
                const res = await fetch('http://localhost:8000/users/me', { headers: { 'Authorization': 'Bearer ' + token } });
                if(res.ok) {
                    const user = await res.json();
                    userRole = user.role;
                    document.getElementById('displayUsername').textContent = user.username;
                    document.getElementById('displayRole').textContent = user.role.replace('_', ' ');
                    document.getElementById('userInfoDisplay').classList.remove('hidden');
                    document.getElementById('userInfoDisplay').classList.add('flex');
                    document.getElementById('updateDataBtn').classList.remove('hidden');
                    document.getElementById('logoutBtn').classList.remove('hidden');
                    if(userRole === 'admin') {
                        document.getElementById('tabConfigs').classList.remove('hidden');
                    }
                } else if (res.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('loginModal').classList.remove('hidden');
                }
            } catch (e) { console.error(e); }
        }

        document.getElementById('updateDataBtn').addEventListener('click', () => {
            document.getElementById('dashboardWrapper').classList.add('hidden');
            document.getElementById('dashboardWrapper').classList.remove('flex');
            document.getElementById('emptyState').classList.add('hidden');
            document.getElementById('updateWrapper').classList.remove('hidden');
            document.getElementById('updateWrapper').classList.add('flex');
            document.getElementById('updateDataBtn').classList.add('hidden');
            document.getElementById('backToDashBtn').classList.remove('hidden');
            
            const sel = document.getElementById('updateTeamSelect');
            sel.innerHTML = '';
            globalData.metrics.forEach(m => {
                let opt = document.createElement('option');
                opt.value = m.team_id;
                opt.textContent = m.engagement;
                sel.appendChild(opt);
            });
            renderUpdateForm();
        });

        document.getElementById('backToDashBtn').addEventListener('click', () => {
            document.getElementById('updateWrapper').classList.add('hidden');
            document.getElementById('updateWrapper').classList.remove('flex');
            document.getElementById('dashboardWrapper').classList.remove('hidden');
            document.getElementById('dashboardWrapper').classList.add('flex');
            document.getElementById('updateDataBtn').classList.remove('hidden');
            document.getElementById('backToDashBtn').classList.add('hidden');
            fetchDataFromAPI();
        });

        document.getElementById('updateTeamSelect').addEventListener('change', renderUpdateForm);

        ['tabMetrics', 'tabDetails', 'tabConfigs'].forEach(tab => {
            document.getElementById(tab).addEventListener('click', (e) => {
                ['tabMetrics', 'tabDetails', 'tabConfigs'].forEach(t => {
                    document.getElementById(t).classList.remove('border-b-2', 'border-tremor-brand-DEFAULT', 'text-tremor-brand-DEFAULT');
                    document.getElementById(t).classList.add('text-tremor-content');
                });
                e.target.classList.remove('text-tremor-content');
                e.target.classList.add('border-b-2', 'border-tremor-brand-DEFAULT', 'text-tremor-brand-DEFAULT');
                currentUpdateTab = tab.replace('tab', '').toLowerCase();
                renderUpdateForm();
            });
        });

        function renderUpdateForm() {
            const container = document.getElementById('updateFormContainer');
            container.innerHTML = '';
            const teamId = document.getElementById('updateTeamSelect').value;
            if(!teamId) return;

            const metric = globalData.metrics.find(m => m.team_id == teamId) || {};
            const detail = globalData.details.find(d => d.team_id == teamId) || {};
            
            let fieldsToRender = {};
            if(currentUpdateTab === 'metrics') {
                fieldsToRender = { ...metric };
                delete fieldsToRender.id; delete fieldsToRender.team_id; delete fieldsToRender.engagement; delete fieldsToRender.spoc;
            } else if (currentUpdateTab === 'details') {
                fieldsToRender = { ...detail };
                delete fieldsToRender.id; delete fieldsToRender.team_id; delete fieldsToRender.engagement; delete fieldsToRender.spoc;
            } else if (currentUpdateTab === 'configs') {
                const engagement = metric.engagement;
                const conf = globalData.ragConfig[engagement] || {};
                Object.keys(conf).forEach(k => {
                    if(k !== 'type' && conf[k] && typeof conf[k] === 'object') {
                        fieldsToRender[k + '_expected'] = conf[k].expected;
                        fieldsToRender[k + '_variance'] = conf[k].variance;
                    }
                });
            }

            Object.keys(fieldsToRender).forEach(k => {
                const div = document.createElement('div');
                div.innerHTML = '<label class="block text-xs text-tremor-content font-medium mb-1">' + getFriendlyName(k) + '</label>' +
                                '<input type="text" id="input_' + k + '" value="' + (fieldsToRender[k] !== null && fieldsToRender[k] !== undefined ? fieldsToRender[k] : '') + '" class="w-full border border-tremor-border rounded px-2 py-1 text-sm text-gray-700">';
                container.appendChild(div);
            });
        }

        document.getElementById('saveUpdateBtn').addEventListener('click', async () => {
            const teamId = document.getElementById('updateTeamSelect').value;
            if(!teamId) return;
            
            const payload = {};
            const inputs = document.getElementById('updateFormContainer').querySelectorAll('input');
            inputs.forEach(input => {
                const k = input.id.replace('input_', '');
                payload[k] = input.value === '' ? null : input.value;
            });

            const token = localStorage.getItem('token');
            const url = "http://localhost:8000/" + (currentUpdateTab === 'configs' ? 'teams/' + teamId + '/configs' : currentUpdateTab + '/' + teamId);

            try {
                const res = await fetch(url, {
                    method: 'PUT',
                    headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const msgEl = document.getElementById('updateMsg');
                msgEl.classList.remove('hidden');
                if(res.ok) {
                    msgEl.textContent = 'Saved successfully!';
                    msgEl.className = 'text-sm mt-2 text-green-600';
                    const [mRes, dRes, cRes] = await Promise.all([
                        fetch('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                        fetch('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                        fetch('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } })
                    ]);
                    globalData.metrics = await mRes.json();
                    globalData.details = await dRes.json();
                    globalData.ragConfig = await cRes.json();
                    
                    sessionStorage.setItem('dashboardData', JSON.stringify({
                        metrics: globalData.metrics,
                        details: globalData.details,
                        ragConfig: globalData.ragConfig
                    }));
                    sessionStorage.setItem('dashboardTimestamp', Date.now().toString());
                } else {
                    const err = await res.json();
                    msgEl.textContent = err.detail || 'Error saving data';
                    msgEl.className = 'text-sm mt-2 text-red-600';
                }
                setTimeout(() => { msgEl.classList.add('hidden'); }, 3000);
            } catch(e) {
                console.error(e);
            }
        });
'''
content = content.replace('async function fetchDataFromAPI() {', js_logic.strip() + '\n\n        async function fetchDataFromAPI() {')


# --- 2. Add TopNav User Info ---
userInfo = '''<div class="flex items-center gap-3">
                    <div id="userInfoDisplay" class="hidden flex-col text-right mr-3 pr-3 border-r border-tremor-border">
                        <span id="displayUsername" class="text-sm font-semibold text-tremor-content-strong leading-tight"></span>
                        <span id="displayRole" class="text-xs text-tremor-content font-medium uppercase tracking-wider"></span>
                    </div>
                    <span id="lastUpdated"'''
content = re.sub(r'<div class="flex items-center gap-3">\s*<span id="lastUpdated"', userInfo, content)


# --- 3. Replace Refresh Button with Logout Button ---
logout_btn_html = '''<button id="logoutBtn" class="bg-white text-red-600 border border-red-200 shadow-sm hover:bg-red-50 hover:text-red-700 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                        Logout
                    </button>'''
# Carefully replace just the refresh button.
content = re.sub(r'<button id="refreshBtn".*?</button>', logout_btn_html, content, flags=re.DOTALL)

# Replace JS logic for logout
content = re.sub(r"const refreshBtn = document\.getElementById\('refreshBtn'\);", "const logoutBtn = document.getElementById('logoutBtn');", content)

logout_event = '''logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('token');
            sessionStorage.removeItem('dashboardData');
            sessionStorage.removeItem('dashboardTimestamp');
            window.location.reload();
        });'''
content = re.sub(r"refreshBtn\.addEventListener\('click', async \(\) => \{.*?\n        \}\);", logout_event, content, flags=re.DOTALL)


# --- 4. Rewrite fetchDataFromAPI for Caching ---
fetchDataCache = '''async function fetchDataFromAPI(forceRefresh = false) {
            const token = localStorage.getItem('token');
            const now = Date.now();
            const cacheTime = sessionStorage.getItem('dashboardTimestamp');
            
            if (!forceRefresh && cacheTime && (now - parseInt(cacheTime) < 300000)) { // 5 minutes cache
                const cachedData = sessionStorage.getItem('dashboardData');
                if (cachedData) {
                    const parsed = JSON.parse(cachedData);
                    globalData.metrics = parsed.metrics;
                    globalData.details = parsed.details;
                    globalData.ragConfig = parsed.ragConfig;
                    
                    document.getElementById('emptyState').classList.add('hidden');
                    document.getElementById('dashboardWrapper').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('flex');
                    
                    updateDropdown();
                    renderAll();
                    
                    document.getElementById('lastUpdated').textContent = 'Refreshed (Cache): ' + new Date().toLocaleTimeString();
                    return;
                }
            }

            try {
                const [metricsRes, detailsRes, configsRes] = await Promise.all([
                    fetch('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } })
                ]);
                
                if (metricsRes.ok && detailsRes.ok && configsRes.ok) {
                    const metrics = await metricsRes.json();
                    const details = await detailsRes.json();
                    const configs = await configsRes.json();
                    
                    globalData.metrics = metrics;
                    globalData.details = details;
                    globalData.ragConfig = configs;
                    
                    sessionStorage.setItem('dashboardData', JSON.stringify({
                        metrics: metrics,
                        details: details,
                        ragConfig: configs
                    }));
                    sessionStorage.setItem('dashboardTimestamp', Date.now().toString());
                    
                    document.getElementById('emptyState').classList.add('hidden');
                    document.getElementById('dashboardWrapper').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('flex');
                    
                    updateDropdown();
                    renderAll();
                    
                    document.getElementById('lastUpdated').textContent = 'Refreshed (API): ' + new Date().toLocaleTimeString();
                } else if (metricsRes.status === 401 || detailsRes.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('loginModal').classList.remove('hidden');
                }
            } catch(e) {
                console.error('Error fetching data:', e);
            }
        }'''
        
# Because we know the exact original fetchDataFromAPI text from current_front.html, we can replace it precisely!
orig_fetch = '''        async function fetchDataFromAPI() {
            const token = localStorage.getItem('token');
            try {
                const [metricsRes, detailsRes, configsRes] = await Promise.all([
                    fetch('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } })
                ]);
                
                if (metricsRes.ok && detailsRes.ok && configsRes.ok) {
                    const metrics = await metricsRes.json();
                    const details = await detailsRes.json();
                    const configs = await configsRes.json();
                    
                    globalData.metrics = metrics;
                    globalData.details = details;
                    globalData.ragConfig = configs;
                    
                    document.getElementById('emptyState').classList.add('hidden');
                    document.getElementById('dashboardWrapper').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('flex');
                    
                    updateDropdown();
                    renderAll();
                    
                    document.getElementById('lastUpdated').textContent = 'Refreshed (API): ' + new Date().toLocaleTimeString();
                } else if (metricsRes.status === 401 || detailsRes.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('loginModal').classList.remove('hidden');
                }
            } catch (err) {
                console.error("API fetch failed:", err);
            }
        }'''
        
content = content.replace(orig_fetch, fetchDataCache)


# --- 5. Fix Login Logic ---
login_fix = '''                    document.getElementById('loginModal').classList.add('hidden');
                    // fetch data after login
                    await fetchUserMe();
                    fetchDataFromAPI();'''
                    
content = content.replace('''                    document.getElementById('loginModal').classList.add('hidden');
                    // fetch data after login
                    fetchDataFromAPI();''', login_fix)


# --- 6. Fix DOMContentLoaded Logic ---
dom_fix = '''            if(!localStorage.getItem('token')) {
                document.getElementById('loginModal').classList.remove('hidden');
            } else {
                await fetchUserMe();
                fetchDataFromAPI();
            }'''
content = content.replace('''            if(!localStorage.getItem('token')) {
                document.getElementById('loginModal').classList.remove('hidden');
            } else {
                fetchDataFromAPI();
            }''', dom_fix)

content = content.replace("window.addEventListener('DOMContentLoaded', () => {", "window.addEventListener('DOMContentLoaded', async () => {")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
