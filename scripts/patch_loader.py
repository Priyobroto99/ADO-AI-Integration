import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = '''        document.getElementById('loginBtn').addEventListener('click', async () => {
            const formData = new FormData();
            formData.append('username', document.getElementById('username').value);
            formData.append('password', document.getElementById('password').value);
            try {
                const res = await fetch('http://localhost:8000/token', { method: 'POST', body: formData });
                if(res.ok) {
                    const data = await res.json();
                    localStorage.setItem('token', data.access_token);
                    document.getElementById('loginModal').classList.add('hidden');
                    // fetch data after login
                    await fetchUserMe();
                    fetchDataFromAPI();
                } else {
                    document.getElementById('loginError').textContent = 'Invalid credentials';
                    document.getElementById('loginError').classList.remove('hidden');
                }
            } catch(e) {
                console.error(e);
            }
        });'''

new_logic = '''        document.getElementById('loginBtn').addEventListener('click', async () => {
            const btn = document.getElementById('loginBtn');
            const originalText = btn.innerHTML;
            btn.innerHTML = <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Authenticating...;
            btn.disabled = true;
            btn.classList.add('opacity-75', 'cursor-not-allowed');
            document.getElementById('loginError').classList.add('hidden');

            const formData = new FormData();
            formData.append('username', document.getElementById('username').value);
            formData.append('password', document.getElementById('password').value);
            try {
                const res = await fetch('http://localhost:8000/token', { method: 'POST', body: formData });
                if(res.ok) {
                    const data = await res.json();
                    localStorage.setItem('token', data.access_token);
                    
                    // fetch data after login while loader still spins
                    await fetchUserMe();
                    await fetchDataFromAPI();
                    
                    document.getElementById('loginModal').classList.add('hidden');
                } else {
                    document.getElementById('loginError').textContent = 'Invalid credentials';
                    document.getElementById('loginError').classList.remove('hidden');
                }
            } catch(e) {
                console.error(e);
                document.getElementById('loginError').textContent = 'Connection error';
                document.getElementById('loginError').classList.remove('hidden');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('opacity-75', 'cursor-not-allowed');
            }
        });'''

content = content.replace(old_logic, new_logic)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
