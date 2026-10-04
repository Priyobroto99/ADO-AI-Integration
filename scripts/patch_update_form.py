import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML Update
old_html = '''                <h2 class="text-tremor-title font-medium text-tremor-content-strong mb-4">Update Team Data</h2>
                
                <div class="mb-4">
                    <label class="text-sm text-tremor-content">Select Team</label>
                    <select id="updateTeamSelect" class="mt-1 block w-full border border-tremor-border rounded-tremor-default px-3 py-2 text-tremor-content-strong text-sm focus:ring-tremor-brand-DEFAULT focus:border-tremor-brand-DEFAULT shadow-sm">
                    </select>
                </div>

                <div class="flex gap-4 border-b border-tremor-border mb-4">
                    <button id="tabMetrics" class="px-4 py-2 text-sm font-medium text-tremor-brand-DEFAULT border-b-2 border-tremor-brand-DEFAULT">Metrics</button>
                    <button id="tabDetails" class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong">Details</button>
                    <button id="tabConfigs" class="px-4 py-2 text-sm font-medium text-tremor-content hover:text-tremor-content-strong hidden">Configurations</button>
                </div>'''

new_html = '''                <h2 class="text-tremor-title font-medium text-tremor-content-strong mb-4">Update Team Configuration</h2>
                
                <div class="mb-4">
                    <label class="text-sm text-tremor-content">Select Team</label>
                    <select id="updateTeamSelect" class="mt-1 block w-full border border-tremor-border rounded-tremor-default px-3 py-2 text-tremor-content-strong text-sm focus:ring-tremor-brand-DEFAULT focus:border-tremor-brand-DEFAULT shadow-sm">
                    </select>
                </div>'''

content = content.replace(old_html, new_html)

# 2. Toast HTML
toast_html = '''
    <div id="toast" class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-md shadow-lg transform transition-all duration-300 translate-y-20 opacity-0 z-50 flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        <span id="toastMsg">Updated successfully</span>
    </div>
</body>'''
content = content.replace('</body>', toast_html)

# 3. JS removals
content = content.replace("let currentUpdateTab = 'metrics';", "")
content = content.replace('''if(userRole === 'admin') {
                        document.getElementById('tabConfigs').classList.remove('hidden');
                    }''', "")

old_tabs_js = '''        ['tabMetrics', 'tabDetails', 'tabConfigs'].forEach(tab => {
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
        });'''
content = content.replace(old_tabs_js, "")

# 4. Update renderUpdateForm
old_render_form = '''        function renderUpdateForm() {
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
        }'''

new_render_form = '''        function renderUpdateForm() {
            const container = document.getElementById('updateFormContainer');
            container.innerHTML = '';
            const teamId = document.getElementById('updateTeamSelect').value;
            if(!teamId) return;

            const metric = globalData.metrics.find(m => m.team_id == teamId) || {};
            const engagement = metric.engagement;
            const conf = globalData.ragConfig[engagement] || {};
            
            let fieldsToRender = {};
            Object.keys(conf).forEach(k => {
                if(k !== 'type' && conf[k] && typeof conf[k] === 'object') {
                    fieldsToRender[k + '_expected'] = conf[k].expected;
                    fieldsToRender[k + '_variance'] = conf[k].variance;
                }
            });

            Object.keys(fieldsToRender).forEach(k => {
                const div = document.createElement('div');
                div.innerHTML = '<label class="block text-xs text-tremor-content font-medium mb-1">' + getFriendlyName(k) + '</label>' +
                                '<input type="text" id="input_' + k + '" value="' + (fieldsToRender[k] !== null && fieldsToRender[k] !== undefined ? fieldsToRender[k] : '') + '" class="w-full border border-tremor-border rounded px-2 py-1 text-sm text-gray-700">';
                container.appendChild(div);
            });
        }'''
content = content.replace(old_render_form, new_render_form)

# 5. Replace Save Button logic
old_save_regex = r"document\.getElementById\('saveUpdateBtn'\)\.addEventListener\('click', async \(\) => \{.*?\n        \}\);"

new_save_js = '''document.getElementById('saveUpdateBtn').addEventListener('click', async () => {
            const btn = document.getElementById('saveUpdateBtn');
            const originalText = btn.innerHTML;
            btn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Updating...`;
            btn.disabled = true;
            btn.classList.add('opacity-75', 'cursor-not-allowed');

            const teamId = document.getElementById('updateTeamSelect').value;
            if(!teamId) {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('opacity-75', 'cursor-not-allowed');
                return;
            }
            
            const payload = {};
            const inputs = document.getElementById('updateFormContainer').querySelectorAll('input');
            inputs.forEach(input => {
                const k = input.id.replace('input_', '');
                payload[k] = input.value === '' ? null : input.value;
            });

            const token = localStorage.getItem('token');
            const url = "http://localhost:8000/teams/" + teamId + "/configs";

            try {
                const res = await fetch(url, {
                    method: 'PUT',
                    headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const msgEl = document.getElementById('updateMsg');
                if(res.ok) {
                    msgEl.classList.add('hidden');
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
                    
                    // Show toast
                    const toast = document.getElementById('toast');
                    toast.classList.remove('translate-y-20', 'opacity-0');
                    setTimeout(() => { toast.classList.add('translate-y-20', 'opacity-0'); }, 3000);
                } else {
                    const err = await res.json();
                    msgEl.textContent = err.detail || 'Error saving data';
                    msgEl.className = 'text-sm mt-2 text-red-600';
                    msgEl.classList.remove('hidden');
                }
            } catch(e) {
                console.error(e);
                const msgEl = document.getElementById('updateMsg');
                msgEl.textContent = 'Connection error';
                msgEl.className = 'text-sm mt-2 text-red-600';
                msgEl.classList.remove('hidden');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('opacity-75', 'cursor-not-allowed');
            }
        });'''

content = re.sub(old_save_regex, new_save_js, content, flags=re.DOTALL)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
