with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''<div class="flex items-center gap-3">
                    <span id="lastUpdated"'''

replacement = '''<div class="flex items-center gap-3">
                    <div id="userInfoDisplay" class="hidden flex-col text-right mr-3 pr-3 border-r border-tremor-border">
                        <span id="displayUsername" class="text-sm font-semibold text-tremor-content-strong leading-tight"></span>
                        <span id="displayRole" class="text-xs text-tremor-content font-medium uppercase tracking-wider"></span>
                    </div>
                    <span id="lastUpdated"'''

content = content.replace(target, replacement)

js_target = '''userRole = user.role;'''
js_replacement = '''userRole = user.role;
                    document.getElementById('displayUsername').textContent = user.username;
                    document.getElementById('displayRole').textContent = user.role.replace('_', ' ');
                    document.getElementById('userInfoDisplay').classList.remove('hidden');
                    document.getElementById('userInfoDisplay').classList.add('flex');'''

content = content.replace(js_target, js_replacement)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
