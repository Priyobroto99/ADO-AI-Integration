with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''                if(res.ok) {
                    const user = await res.json();
                    userRole = user.role;
                    document.getElementById('displayUsername').textContent = user.username;
                    document.getElementById('displayRole').textContent = user.role.replace('_', ' ');
                    document.getElementById('userInfoDisplay').classList.remove('hidden');
                    document.getElementById('userInfoDisplay').classList.add('flex');
                    document.getElementById('updateDataBtn').classList.remove('hidden');
                    if(userRole === 'admin') {
                        document.getElementById('tabConfigs').classList.remove('hidden');
                    }
                }'''

replacement = target + ''' else if (res.status === 401) {
                    localStorage.removeItem('token');
                    document.getElementById('loginModal').classList.remove('hidden');
                }'''

content = content.replace(target, replacement)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
