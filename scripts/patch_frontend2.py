import re

with open('current_front.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Update Data Button in Topnav
update_btn = '''
                    <button id="updateDataBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Update Data
                    </button>
                    <button id="backToDashBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Back to Dashboard
                    </button>
'''
content = content.replace('id="refreshBtn"', update_btn.strip() + '\n                    <button id="refreshBtn"')

# 2. Add updateWrapper view HTML after dashboardWrapper
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

# 3. Add JS logic for roles, switching views, and submitting updates
js_logic = '''
        let userRole = null;
        let currentUpdateTab = 'metrics';

        async function fetchUserMe() {
            const token = localStorage.getItem('token');
            if(!token) return;
            try {
                const res = await fetch('http://localhost:8000/users/me', { headers: { 'Authorization': 'Bearer ' + token } });
                if(res.ok) {
                    const user = await res.json();
                    userRole = user.role;
                    document.getElementById('updateDataBtn').classList.remove('hidden');
                    if(userRole === 'admin') {
                        document.getElementById('tabConfigs').classList.remove('hidden');
                    }
                }
            } catch (e) { console.error(e); }
        }

        document.getElementById('updateDataBtn').addEventListener('click', () => {
            document.getElementById('dashboardWrapper').classList.add('hidden');
            document.getElementById('emptyState').classList.add('hidden');
            document.getElementById('updateWrapper').classList.remove('hidden');
            document.getElementById('updateWrapper').classList.add('flex');
            document.getElementById('updateDataBtn').classList.add('hidden');
            document.getElementById('backToDashBtn').classList.remove('hidden');
            
            // Populate team select
            const sel = document.getElementById('updateTeamSelect');
            sel.innerHTML = '';
            globalData.metrics.forEach(m => {
                let opt = document.createElement('option');
                opt.value = m.team_id; // Using team_id
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
            fetchDataFromAPI(); // Refresh dashboard
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

            // Find data for this team ID
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
                // Configs are nested in globalData.ragConfig[engagement]
                const engagement = metric.engagement;
                // find configs from DB
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
                div.innerHTML = 
                    <label class="block text-xs text-tremor-content font-medium mb-1"></label>
                    <input type="text" id="input_" value="" class="w-full border border-tremor-border rounded px-2 py-1 text-sm text-gray-700">
                ;
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
            const method = 'PUT'; // all are PUT

            try {
                const res = await fetch(url, {
                    method,
                    headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const msgEl = document.getElementById('updateMsg');
                msgEl.classList.remove('hidden');
                if(res.ok) {
                    msgEl.textContent = 'Saved successfully!';
                    msgEl.className = 'text-sm mt-2 text-green-600';
                    // Re-fetch global data in background
                    const [mRes, dRes, cRes] = await Promise.all([
                        fetch('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                        fetch('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } }),
                        fetch('http://localhost:8000/configs', { headers: { 'Authorization': 'Bearer ' + token } })
                    ]);
                    globalData.metrics = await mRes.json();
                    globalData.details = await dRes.json();
                    globalData.ragConfig = await cRes.json();
                } else {
                    const err = await res.json();
                    msgEl.textContent = err.detail || 'Error saving data';
                    msgEl.className = 'text-sm mt-2 text-red-600';
                }
                setTimeout(() => msgEl.classList.add('hidden'), 3000);
            } catch(e) {
                console.error(e);
            }
        });
'''
# JS literal fixes applied (removed Python f-string escaping)
content = content.replace('async function fetchDataFromAPI() {', js_logic.strip() + '\n\n        async function fetchDataFromAPI() {')

# 4. Modify login/autoload logic to call fetchUserMe
content = content.replace('fetchDataFromAPI();', 'await fetchUserMe();\n                    fetchDataFromAPI();')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
