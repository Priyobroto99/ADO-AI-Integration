import codecs

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add navLoginBtn
nav_login_html = '''
                    <button id="navLoginBtn" class="bg-tremor-brand-DEFAULT border border-tremor-brand-DEFAULT text-white shadow-sm hover:bg-tremor-brand-emphasis font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">
                        Login
                    </button>
                    <button id="updateDataBtn"'''
content = content.replace('<button id="updateDataBtn"', nav_login_html.strip())

# 2. Add Cancel button to modal
cancel_btn_html = '''</button>
                    <button id="closeLoginModalBtn" class="mt-2 px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-300">
                        Cancel
                    </button>
                    <p id="loginError"'''
content = content.replace('</button>\n                    <p id="loginError"', cancel_btn_html.strip())

# 3. Update DOMContentLoaded
old_dom = '''        window.addEventListener('DOMContentLoaded', async () => {
            if(!localStorage.getItem('token')) {
                document.getElementById('loginModal').classList.remove('hidden');
            } else {
                await fetchUserMe();
                fetchDataFromAPI();
            }
        });'''
new_dom = '''        window.addEventListener('DOMContentLoaded', async () => {
            if(!localStorage.getItem('token')) {
                document.getElementById('navLoginBtn').classList.remove('hidden');
                fetchDataFromAPI();
            } else {
                await fetchUserMe();
                fetchDataFromAPI();
            }
        });'''
content = content.replace(old_dom, new_dom)

# 4. Update fetchUserMe
old_fetch = '''                } else if (res.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('loginModal').classList.remove('hidden');
                }'''
new_fetch = '''                } else if (res.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('navLoginBtn').classList.remove('hidden');
                }'''
content = content.replace(old_fetch, new_fetch)

# 5. Add event listeners for the new buttons
event_listeners = '''
        document.getElementById('navLoginBtn').addEventListener('click', () => {
            document.getElementById('loginModal').classList.remove('hidden');
        });
        
        document.getElementById('closeLoginModalBtn').addEventListener('click', () => {
            document.getElementById('loginModal').classList.add('hidden');
            document.getElementById('loginError').classList.add('hidden');
        });
        
        document.getElementById('loginBtn').addEventListener('click','''
content = content.replace("document.getElementById('loginBtn').addEventListener('click',", event_listeners.strip())

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
