import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject CSS for animation inside <style> or create a <style> block in <head>
css_style = '''
    <style>
        @keyframes growBar {
            0%, 100% { height: 20%; }
            50% { height: 85%; }
        }
        @keyframes dashLine {
            0% { stroke-dashoffset: 200; }
            50% { stroke-dashoffset: 0; }
            100% { stroke-dashoffset: -200; }
        }
    </style>
</head>'''
content = content.replace('</head>', css_style)

# 2. Add the loggedOutState HTML right before emptyState
animation_html = '''
        <!-- Logged Out Animation State -->
        <div id="loggedOutState" class="hidden flex-col items-center justify-center h-[60vh] gap-8">
            <div class="relative w-64 h-64 border-b-2 border-l-2 border-gray-200">
                <!-- Animated Bars -->
                <div class="absolute bottom-0 left-6 w-10 bg-blue-300 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 0s;"></div>
                <div class="absolute bottom-0 left-20 w-10 bg-blue-400 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 0.4s;"></div>
                <div class="absolute bottom-0 left-36 w-10 bg-indigo-500 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 0.8s;"></div>
                <div class="absolute bottom-0 left-52 w-10 bg-blue-600 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 1.2s;"></div>
                
                <!-- Animated Trend Line -->
                <svg class="absolute inset-0 w-full h-full text-green-500 z-10 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M10,80 L35,45 L60,55 L95,15" stroke-dasharray="200" style="animation: dashLine 4s ease-in-out infinite;"></path>
                    <circle cx="95" cy="15" r="3" fill="currentColor" class="animate-pulse"></circle>
                </svg>
            </div>
            <div class="text-center">
                <h2 class="text-3xl font-bold text-gray-800 tracking-tight">CAT Delivery Excellence</h2>
                <p class="text-gray-500 mt-2 text-sm max-w-sm mx-auto">Please login to access real-time team metrics, performance analytics, and advanced tracker configurations.</p>
            </div>
        </div>
        
        <div id="emptyState"'''
content = content.replace('<div id="emptyState"', animation_html)

# 3. Update DOMContentLoaded logic
dom_old = '''        window.addEventListener('DOMContentLoaded', async () => {
            if(!localStorage.getItem('token')) {
                document.getElementById('navLoginBtn').classList.remove('hidden');
                fetchDataFromAPI();
            } else {
                await fetchUserMe();
                fetchDataFromAPI();
            }
        });'''
dom_new = '''        window.addEventListener('DOMContentLoaded', async () => {
            if(!localStorage.getItem('token')) {
                document.getElementById('navLoginBtn').classList.remove('hidden');
                document.getElementById('emptyState').classList.add('hidden');
                document.getElementById('dashboardWrapper').classList.add('hidden');
                document.getElementById('dashboardWrapper').classList.remove('flex');
                document.getElementById('loggedOutState').classList.remove('hidden');
                document.getElementById('loggedOutState').classList.add('flex');
            } else {
                await fetchUserMe();
                fetchDataFromAPI();
            }
        });'''
content = content.replace(dom_old, dom_new)

# 4. In fetchUserMe, if 401, hide dashboard and show animation
fetch_me_old = '''                } else if (res.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('navLoginBtn').classList.remove('hidden');
                }'''
fetch_me_new = '''                } else if (res.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('navLoginBtn').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('hidden');
                    document.getElementById('dashboardWrapper').classList.remove('flex');
                    document.getElementById('loggedOutState').classList.remove('hidden');
                    document.getElementById('loggedOutState').classList.add('flex');
                }'''
content = content.replace(fetch_me_old, fetch_me_new)

# 5. In fetchDataFromAPI, if 401, hide dashboard and show animation
fetch_api_old = '''                } else if (metricsRes.status === 401 || detailsRes.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('loginModal').classList.remove('hidden');
                }'''
fetch_api_new = '''                } else if (metricsRes.status === 401 || detailsRes.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('navLoginBtn').classList.remove('hidden');
                    document.getElementById('dashboardWrapper').classList.add('hidden');
                    document.getElementById('dashboardWrapper').classList.remove('flex');
                    document.getElementById('loggedOutState').classList.remove('hidden');
                    document.getElementById('loggedOutState').classList.add('flex');
                }'''
content = content.replace(fetch_api_old, fetch_api_new)

# 6. Hide animation when data successfully fetched
hide_anim = '''                    document.getElementById('loggedOutState').classList.add('hidden');
                    document.getElementById('loggedOutState').classList.remove('flex');
                    document.getElementById('emptyState').classList.add('hidden');'''
content = content.replace("document.getElementById('emptyState').classList.add('hidden');", hide_anim)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
