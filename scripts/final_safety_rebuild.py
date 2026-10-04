import codecs
import re

# 1. Base rebuild
with codecs.open('current_front.html', 'r', 'utf-16') as f:
    content = f.read().replace('\r\n', '\n')

# 1a. Update View HTML & TopNav Buttons
update_btn = '''
                    <button id="navLoginBtn" class="bg-white text-gray-900 border border-gray-300 shadow-sm hover:bg-blue-600 hover:text-white font-medium rounded-md text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Login
                    </button>
                    <button id="updateDataBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Update Data
                    </button>
                    <button id="backToDashBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Back to Dashboard
                    </button>
'''
content = content.replace('<button id="refreshBtn"', update_btn.strip() + '\n                    <button id="refreshBtn"')

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
                label = label.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); });
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
                    document.getElementById('navLoginBtn').classList.add('hidden');
                    if(userRole === 'admin') {
                        document.getElementById('tabConfigs').classList.remove('hidden');
                    }
                } else if (res.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('navLoginBtn').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('hidden');
                    document.getElementById('dashboardWrapper').classList.remove('flex');
                    document.getElementById('loggedOutState').classList.remove('hidden');
                    document.getElementById('loggedOutState').classList.add('flex');
                }
            } catch (e) { console.error(e); }
        }

        document.getElementById('navLoginBtn').addEventListener('click', () => {
            document.getElementById('loginModal').classList.remove('hidden');
        });

        document.getElementById('updateDataBtn').addEventListener('click', () => {
            document.getElementById('dashboardWrapper').classList.add('hidden');
            document.getElementById('dashboardWrapper').classList.remove('flex');
            document.getElementById('emptyState').classList.add('hidden');
            document.getElementById('loggedOutState').classList.add('hidden');
            document.getElementById('loggedOutState').classList.remove('flex');
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
content = re.sub(r'\s*async function fetchDataFromAPI\(\) \{', '\n\n' + js_logic.strip() + '\n\n                async function fetchDataFromAPI() {', content, count=1)

userInfo = '''<div class="flex items-center gap-3">
                    <div id="userInfoDisplay" class="hidden flex-col text-right mr-3 pr-3 border-r border-tremor-border">
                        <span id="displayUsername" class="text-sm font-semibold text-tremor-content-strong leading-tight"></span>
                        <span id="displayRole" class="text-xs text-tremor-content font-medium uppercase tracking-wider"></span>
                    </div>
                    <span id="lastUpdated"'''
content = re.sub(r'<div class="flex items-center gap-3">\s*<span id="lastUpdated"', userInfo, content)

logout_btn_html = '''<button id="logoutBtn" class="bg-white text-red-600 border border-red-200 shadow-sm hover:bg-red-50 hover:text-red-700 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                        Logout
                    </button>'''
content = re.sub(r'<button id="refreshBtn"[^>]*>.*?</button>', logout_btn_html, content, flags=re.DOTALL, count=1)
content = re.sub(r"const refreshBtn = document\.getElementById\('refreshBtn'\);", "const logoutBtn = document.getElementById('logoutBtn');", content)

logout_event = '''logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('token');
            sessionStorage.removeItem('dashboardData');
            sessionStorage.removeItem('dashboardTimestamp');
            window.location.reload();
        });'''
content = re.sub(r"refreshBtn\.addEventListener\('click', async \(\) => \{.*?\n\}\);", logout_event, content, flags=re.DOTALL)

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
                    document.getElementById('loggedOutState').classList.add('hidden');
                    document.getElementById('loggedOutState').classList.remove('flex');
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
                    document.getElementById('loggedOutState').classList.add('hidden');
                    document.getElementById('loggedOutState').classList.remove('flex');
                    document.getElementById('dashboardWrapper').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('flex');
                    
                    updateDropdown();
                    renderAll();
                    
                    document.getElementById('lastUpdated').textContent = 'Refreshed (API): ' + new Date().toLocaleTimeString();
                } else if (metricsRes.status === 401 || detailsRes.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('navLoginBtn').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('hidden');
                    document.getElementById('dashboardWrapper').classList.remove('flex');
                    document.getElementById('emptyState').classList.add('hidden');
                    document.getElementById('loggedOutState').classList.remove('hidden');
                    document.getElementById('loggedOutState').classList.add('flex');
                }
            } catch(e) {
                console.error('Error fetching data:', e);
            }
        }'''
        
orig_fetch = '''                async function fetchDataFromAPI() {
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

# Add close modal cancel button
cancel_btn = '''</button>
                    <button id="closeLoginModalBtn" class="mt-2 px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-300">
                        Cancel
                    </button>
                    <p id="loginError"'''
content = content.replace('</button>\n                    <p id="loginError"', cancel_btn)

# Add close modal JS
content = content.replace("document.getElementById('loginBtn').addEventListener('click',", "document.getElementById('closeLoginModalBtn').addEventListener('click', () => { document.getElementById('loginModal').classList.add('hidden'); document.getElementById('loginError').classList.add('hidden'); });\n\n        document.getElementById('loginBtn').addEventListener('click',")

# Fix login success logic
content = content.replace("document.getElementById('loginModal').classList.add('hidden');\n                    // fetch data after login\n                    fetchDataFromAPI();", "document.getElementById('loginModal').classList.add('hidden');\n                    // fetch data after login\n                    await fetchUserMe();\n                    fetchDataFromAPI();")


# Now add the animation safely!
new_css = '''
    <style>
        @keyframes float1 { 0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; } 50% { transform: translate(-20px, -40px) scale(1.1); opacity: 0.6; } }
        @keyframes float2 { 0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.2; } 50% { transform: translate(30px, -30px) scale(0.9); opacity: 0.5; } }
        @keyframes float3 { 0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.2; } 50% { transform: translate(-30px, 30px) scale(1.2); opacity: 0.4; } }
        @keyframes float4 { 0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.15; } 50% { transform: translate(40px, 40px) scale(1.3); opacity: 0.4; } }
        @keyframes ripple { 0% { transform: scale(0.8) translate(-50%, -50%); opacity: 1; } 100% { transform: scale(2.5) translate(-20%, -20%); opacity: 0; } }
        @keyframes gradientMove { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes panGrid { 0% { background-position: 0 0; } 100% { background-position: 40px 40px; } }
        @keyframes growBar { 0%, 100% { height: 20%; } 50% { height: 85%; } }
        @keyframes dashLine { 0% { stroke-dashoffset: 200; } 50% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: -200; } }
        .bg-animated-gradient { background: linear-gradient(-45deg, #f8fafc, #eff6ff, #e0e7ff, #f8fafc); background-size: 400% 400%; animation: gradientMove 15s ease infinite; }
        .bg-animated-grid { background-size: 40px 40px; background-image: linear-gradient(to right, rgba(99, 102, 241, 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(99, 102, 241, 0.05) 1px, transparent 1px); animation: panGrid 20s linear infinite; }
    </style>
</head>'''
content = content.replace('</head>', new_css)


new_logged_out = '''
        <div id="loggedOutState" class="hidden relative flex-col items-center justify-center min-h-[82vh] w-full gap-8 rounded-2xl bg-animated-gradient overflow-hidden border border-gray-200 shadow-sm mt-2">
            
            <!-- Panning Grid Background -->
            <div class="absolute inset-0 bg-animated-grid mix-blend-multiply opacity-60"></div>
            
            <!-- Floating Data Orbs (Expanded) -->
            <div class="absolute top-10 left-10 w-32 h-32 bg-blue-300 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float1 8s ease-in-out infinite;"></div>
            <div class="absolute top-20 right-20 w-48 h-48 bg-indigo-200 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float2 10s ease-in-out infinite;"></div>
            <div class="absolute bottom-10 left-32 w-36 h-36 bg-purple-200 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float3 12s ease-in-out infinite;"></div>
            <div class="absolute bottom-20 right-32 w-40 h-40 bg-blue-200 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float4 14s ease-in-out infinite;"></div>
            <div class="absolute top-1/2 left-4 w-24 h-24 bg-purple-300 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float2 9s ease-in-out infinite;"></div>
            <div class="absolute bottom-1/4 right-10 w-28 h-28 bg-indigo-300 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float1 11s ease-in-out infinite;"></div>
            
            <!-- Floating Data Strings/Nodes -->
            <div class="absolute top-1/4 left-1/4 text-xs text-blue-600/30 font-mono tracking-widest font-bold" style="animation: float1 15s infinite;">0100110</div>
            <div class="absolute bottom-1/3 right-1/4 text-xs text-indigo-600/30 font-mono tracking-widest font-bold" style="animation: float2 18s infinite;">DATA.SYNC()</div>
            <div class="absolute top-1/2 right-[15%] text-xs text-purple-600/30 font-mono tracking-widest font-bold" style="animation: float3 12s infinite;">{ metrics: live }</div>
            <div class="absolute bottom-[20%] left-[15%] text-xs text-blue-600/30 font-mono tracking-widest font-bold" style="animation: float4 14s infinite;">SYSTEM.ONLINE</div>
            <div class="absolute top-[15%] right-[30%] text-xs text-indigo-600/30 font-mono tracking-widest font-bold" style="animation: float1 16s infinite;">await fetchMetrics()</div>

            <!-- Pulse Rings Behind Icon -->
            <div class="absolute top-1/2 left-1/2 w-80 h-80 border border-blue-400/40 rounded-full" style="animation: ripple 3s linear infinite; transform-origin: top left;"></div>
            <div class="absolute top-1/2 left-1/2 w-80 h-80 border border-indigo-300/40 rounded-full" style="animation: ripple 3s linear infinite 1.5s; transform-origin: top left;"></div>
            <div class="absolute top-1/2 left-1/2 w-[28rem] h-[28rem] border border-purple-200/30 rounded-full" style="animation: ripple 4s linear infinite 0.75s; transform-origin: top left;"></div>

            <!-- Foreground Animated Icon -->
            <div class="relative w-72 h-72 border-b-4 border-l-4 border-gray-300/80 z-10 backdrop-blur-md bg-white/40 p-5 rounded-xl shadow-lg">
                <!-- Animated Bars -->
                <div class="absolute bottom-0 left-6 w-12 bg-blue-400 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 0s;"></div>
                <div class="absolute bottom-0 left-24 w-12 bg-indigo-400 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 0.4s;"></div>
                <div class="absolute bottom-0 left-44 w-12 bg-purple-500 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 0.8s;"></div>
                <div class="absolute bottom-0 left-64 w-12 bg-blue-600 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 1.2s;"></div>
                
                <!-- Animated Trend Line -->
                <svg class="absolute inset-0 w-full h-full text-green-500 z-20 drop-shadow-lg" fill="none" stroke="currentColor" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path stroke-width="4" stroke-linecap="round" stroke-linejoin="round" d="M8,80 L32,45 L58,55 L95,15" stroke-dasharray="200" style="animation: dashLine 4s ease-in-out infinite;"></path>
                    <circle cx="95" cy="15" r="5" fill="currentColor" class="animate-pulse shadow-green-500"></circle>
                </svg>
            </div>
            
            <!-- Text Content -->
            <div class="text-center z-10 bg-white/60 px-10 py-5 rounded-2xl backdrop-blur-md shadow-lg border border-white/80 mt-4">
                <h2 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-700 tracking-tight drop-shadow-sm">CAT Delivery Excellence</h2>
                <p class="text-gray-700 mt-3 text-base max-w-md mx-auto font-medium">Please login to access real-time team metrics, performance analytics, and advanced tracker configurations.</p>
            </div>
        </div>
        
        <div id="emptyState"'''
content = content.replace('<div id="emptyState"', new_logged_out)


# Update DOMContentLoaded
new_dom = '''window.addEventListener('DOMContentLoaded', async () => {
            if(!localStorage.getItem('token')) {
                document.getElementById('navLoginBtn').classList.remove('hidden');
                document.getElementById('dashboardWrapper').classList.add('hidden');
                document.getElementById('dashboardWrapper').classList.remove('flex');
                document.getElementById('emptyState').classList.add('hidden');
                document.getElementById('loggedOutState').classList.remove('hidden');
                document.getElementById('loggedOutState').classList.add('flex');
            } else {
                await fetchUserMe();
                fetchDataFromAPI();
            }
        });'''
content = content.replace('''window.addEventListener('DOMContentLoaded', () => {
            if(!localStorage.getItem('token')) {
                document.getElementById('loginModal').classList.remove('hidden');
            } else {
                fetchDataFromAPI();
            }
        });''', new_dom)


with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
