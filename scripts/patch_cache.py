import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update fetchDataFromAPI to include caching
new_fetch_func = '''async function fetchDataFromAPI(forceRefresh = false) {
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
                    document.getElementById('lastUpdated').textContent = 'Refreshed (Cache): ' + new Date().toLocaleTimeString();
                    document.getElementById('lastUpdated').classList.remove('hidden');
                    
                    initializeDashboard();
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
                    document.getElementById('lastUpdated').textContent = 'Refreshed (API): ' + new Date().toLocaleTimeString();
                    document.getElementById('lastUpdated').classList.remove('hidden');
                    
                    initializeDashboard();
                } else if (metricsRes.status === 401 || detailsRes.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('loginModal').classList.remove('hidden');
                }
            } catch(e) {
                console.error('Error fetching data:', e);
            }
        }'''

# Replace old fetchDataFromAPI
# We use regex to match from sync function fetchDataFromAPI() { down to its closing bracket.
# Because the function is large, let's just do a string replacement of the exact body, or regex with DOTALL.
pattern = re.compile(r'async function fetchDataFromAPI\(\) \{.*?\n        \}', re.DOTALL)
content = pattern.sub(new_fetch_func, content, count=1)

# 2. Update saveUpdateBtn click handler to update cache
cache_update_logic = '''
                    globalData.metrics = await mRes.json();
                    globalData.details = await dRes.json();
                    globalData.ragConfig = await cRes.json();
                    
                    sessionStorage.setItem('dashboardData', JSON.stringify({
                        metrics: globalData.metrics,
                        details: globalData.details,
                        ragConfig: globalData.ragConfig
                    }));
                    sessionStorage.setItem('dashboardTimestamp', Date.now().toString());'''

content = content.replace('''
                    globalData.metrics = await mRes.json();
                    globalData.details = await dRes.json();
                    globalData.ragConfig = await cRes.json();''', cache_update_logic)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
