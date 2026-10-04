import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

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

# Find the exact string from "async function fetchDataFromAPI() {" to the matching closing brace.
# Since we know what comes right after it is: document.getElementById('loginBtn')
pattern = re.compile(r'async function fetchDataFromAPI\(\) \{.*?\n\s+\}\s+document\.getElementById\(\'loginBtn\'\)', re.DOTALL)
content = pattern.sub(fetchDataCache + "\n\n        document.getElementById('loginBtn')", content)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
