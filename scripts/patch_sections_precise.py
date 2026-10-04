import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find exact start and end
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'function renderUpdateForm()' in line:
        start_idx = i
    if start_idx != -1 and 'async function fetchDataFromAPI' in line:
        end_idx = i
        break

if start_idx == -1 or end_idx == -1:
    print("Could not find the block bounds!")
    exit(1)

# The end of saveUpdateBtn is right before fetchDataFromAPI. We will replace lines from start_idx to end_idx - 1 (inclusive).

new_block_str = r'''        function renderUpdateForm() {
            const container = document.getElementById('updateFormContainer');
            container.innerHTML = '';
            const teamId = document.getElementById('updateTeamSelect').value;
            if(!teamId) return;

            const metric = globalData.metrics.find(m => m.team_id == teamId) || {};
            const detail = globalData.details.find(d => d.team_id == teamId) || {};
            
            const METRIC_SECTIONS = {
                'Delivery': ['delivery_sp_assigned', 'delivery_sp_completed', 'delivery_us_pushed', 'delivery_us_assigned', 'delivery_us_completed'],
                'Program Health': ['health_overall', 'health_delivery', 'health_quality', 'health_automation', 'health_compliance'],
                'Quality': ['quality_uat_defects', 'quality_prod_defects', 'quality_bugs_pushed'],
                'Capability & Gaps': ['capability_primary', 'capability_secondary'],
                'Automation': ['automation_manual_hrs', 'automation_automated_hrs', 'automation_coverage'],
                'Compliance': ['compliance_trainings', 'compliance_timesheet'],
                'Problem Statement & Effort': ['problem_tickets', 'effort_saved_hrs']
            };

            const DETAIL_SECTIONS = {
                'General Information': ['catManager', 'engagementCode'],
                'Delivery Details': ['details_delivery'],
                'Program Health Details': ['details_health'],
                'Quality Details': ['details_quality'],
                'Capability Details': ['details_capability'],
                'Automation Details': ['details_automation'],
                'Compliance Details': ['details_compliance'],
                'Problem Statement Details': ['details_problem']
            };

            const CONFIG_SECTIONS = {
                'Delivery Rules': ['delivery_sp_ratio', 'delivery_us_ratio', 'delivery_us_pushed'],
                'Quality Rules': ['quality_uat_defects', 'quality_prod_defects'],
                'Automation Rules': ['automation_coverage'],
                'Compliance Rules': ['compliance_trainings', 'compliance_timesheet']
            };

            let sections = {};
            let sourceData = {};

            if(currentUpdateTab === 'metrics') {
                sections = METRIC_SECTIONS;
                sourceData = { ...metric };
            } else if (currentUpdateTab === 'details') {
                sections = DETAIL_SECTIONS;
                sourceData = { ...detail };
            } else if (currentUpdateTab === 'configs') {
                sections = CONFIG_SECTIONS;
                const engagement = metric.engagement;
                const conf = globalData.ragConfig[engagement] || {};
                // Flatten configs
                Object.keys(conf).forEach(k => {
                    if(k !== 'type' && conf[k] && typeof conf[k] === 'object') {
                        sourceData[k + '_expected'] = conf[k].expected;
                        sourceData[k + '_variance'] = conf[k].variance;
                    }
                });
            }

            // Render Sections
            Object.keys(sections).forEach(sectionTitle => {
                const keys = sections[sectionTitle];
                let hasFields = false;
                
                let actualKeysToRender = [];
                if (currentUpdateTab === 'configs') {
                    keys.forEach(k => {
                        actualKeysToRender.push(k + '_expected');
                        actualKeysToRender.push(k + '_variance');
                    });
                } else {
                    actualKeysToRender = keys;
                }
                
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'mb-6 bg-gray-50 p-4 rounded-tremor-default border border-tremor-border';
                
                const header = document.createElement('h3');
                header.className = 'text-sm font-semibold text-tremor-content-strong mb-4 pb-2 border-b border-tremor-border';
                header.textContent = sectionTitle;
                sectionDiv.appendChild(header);

                const grid = document.createElement('div');
                grid.className = 'grid grid-cols-1 sm:grid-cols-2 gap-4';
                
                actualKeysToRender.forEach(k => {
                    const div = document.createElement('div');
                    // For details lists, use textarea and parse JSON array to newlines
                    let val = sourceData[k] !== null && sourceData[k] !== undefined ? sourceData[k] : '';
                    let isTextarea = currentUpdateTab === 'details' && k.startsWith('details_');
                    
                    if(isTextarea && val && typeof val === 'string' && val.startsWith('[')) {
                        try {
                            const parsed = JSON.parse(val);
                            if(Array.isArray(parsed)) val = parsed.join('\n');
                        } catch(e) {}
                    }
                    
                    div.innerHTML = `<label class="block text-xs text-tremor-content font-medium mb-1">${getFriendlyName(k)}</label>`;
                    if(isTextarea) {
                        div.innerHTML += `<textarea id="input_${k}" rows="3" class="w-full border border-tremor-border rounded px-3 py-2 text-sm text-gray-700 shadow-sm focus:ring-tremor-brand-DEFAULT focus:border-tremor-brand-DEFAULT">${val}</textarea>`;
                        div.className = 'sm:col-span-2'; // full width for textareas
                    } else {
                        div.innerHTML += `<input type="text" id="input_${k}" value="${val}" class="w-full border border-tremor-border rounded px-3 py-2 text-sm text-gray-700 shadow-sm focus:ring-tremor-brand-DEFAULT focus:border-tremor-brand-DEFAULT">`;
                    }
                    grid.appendChild(div);
                });
                
                sectionDiv.appendChild(grid);
                container.appendChild(sectionDiv);
            });
        }

        document.getElementById('saveUpdateBtn').addEventListener('click', async () => {
            const teamId = document.getElementById('updateTeamSelect').value;
            if(!teamId) return;
            
            const payload = {};
            const inputs = document.getElementById('updateFormContainer').querySelectorAll('input, textarea');
            inputs.forEach(input => {
                const k = input.id.replace('input_', '');
                let val = input.value === '' ? null : input.value;
                
                // If it is a details list textarea, convert back to JSON array string
                if (currentUpdateTab === 'details' && k.startsWith('details_') && val) {
                    const lines = val.split('\n').map(l => l.trim()).filter(l => l.length > 0);
                    val = JSON.stringify(lines);
                }
                
                payload[k] = val;
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
                    msgEl.className = 'text-sm mt-2 text-green-600 font-medium';
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
                    
                    // Force refresh main view
                    renderAll();
                } else {
                    msgEl.textContent = 'Error saving data.';
                    msgEl.className = 'text-sm mt-2 text-red-600 font-medium';
                }
                setTimeout(() => { msgEl.classList.add('hidden'); }, 3000);
            } catch(e) {
                console.error(e);
            }
        });

'''

# Because it's a raw string, \n is literal \n. But we want \n in JS string literals!
# So we must replace literal newline characters with \\n just for JS.
# Wait, no. Python parses r'\n' as two chars: `\` and `n`.
# So inside the raw string, \n is exactly what we want in JS (`\n` string escape)!

new_lines = lines[:start_idx] + [new_block_str] + lines[end_idx:]

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

