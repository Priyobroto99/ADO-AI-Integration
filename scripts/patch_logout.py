import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the HTML button
logout_btn_html = '''<button id="logoutBtn" class="bg-white text-red-600 border border-red-200 shadow-sm hover:bg-red-50 hover:text-red-700 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                        Logout
                    </button>'''
                    
content = re.sub(r'<button id="refreshBtn".*?</button>', logout_btn_html, content, flags=re.DOTALL)

# 2. Replace const refreshBtn
content = re.sub(r"const refreshBtn = document\.getElementById\('refreshBtn'\);", "const logoutBtn = document.getElementById('logoutBtn');", content)

# 3. Replace the event listener
logout_event = '''logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('token');
            window.location.reload();
        });'''
        
content = re.sub(r"refreshBtn\.addEventListener\('click', async \(\) => \{.*?\n        \}\);", logout_event, content, flags=re.DOTALL)

# 4. Unhide the logout button when fetchUserMe succeeds (next to updateDataBtn)
content = content.replace("document.getElementById('updateDataBtn').classList.remove('hidden');", "document.getElementById('updateDataBtn').classList.remove('hidden');\n                    document.getElementById('logoutBtn').classList.remove('hidden');")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
