import codecs
import re

with codecs.open('current_front.html', 'r', 'utf-16') as f:
    content = f.read().replace('\r\n', '\n')
print('Start:', 'loginBtn' in content)

# 1a
update_btn = '''<button id="updateDataBtn"...'''
content = content.replace('<button id="refreshBtn"', update_btn.strip() + '\n                    <button id="refreshBtn"')
print('1a:', 'loginBtn' in content)

# 1b
update_view_html = '''<div id="updateWrapper"...'''
content = content.replace('<div id="dashboardWrapper"', update_view_html.strip() + '\n\n        <div id="dashboardWrapper"')
print('1b:', 'loginBtn' in content)

# 1c
content = re.sub(r'\s*async function fetchDataFromAPI\(\) \{', '\n\n' + 'js_logic' + '\n\n        async function fetchDataFromAPI() {', content, count=1)
print('1c:', 'loginBtn' in content)

# 2
userInfo = '''<div class="flex items-center gap-3">...'''
content = re.sub(r'<div class="flex items-center gap-3">\s*<span id="lastUpdated"', userInfo, content)
print('2:', 'loginBtn' in content)

# 3
logout_btn_html = '''<button id="logoutBtn"...'''
content = re.sub(r'<button id="refreshBtn".*?</button>', logout_btn_html, content, flags=re.DOTALL, count=1)
content = re.sub(r"const refreshBtn = document\.getElementById\('refreshBtn'\);", "const logoutBtn = document.getElementById('logoutBtn');", content)
logout_event = '''logoutBtn.addEventListener...'''
content = re.sub(r"refreshBtn\.addEventListener\('click', async \(\) => \{.*?\n        \}\);", logout_event, content, flags=re.DOTALL)
print('3:', 'loginBtn' in content)

# 4
fetchDataCache = '''async function fetchDataFromAPI(forceRefresh = false)...'''
pattern = re.compile(r'async function fetchDataFromAPI\(\) \{.*?\n        \}', re.DOTALL)
content = pattern.sub(fetchDataCache, content, count=1)
print('4:', 'loginBtn' in content)

# 5
login_fix_regex = re.compile(r'document\.getElementById\(\'loginModal\'\)\.classList\.add\(\'hidden\'\);\s*// fetch data after login\s*fetchDataFromAPI\(\);')
content = login_fix_regex.sub("document.getElementById('loginModal').classList.add('hidden');\n                    // fetch data after login\n                    await fetchUserMe();\n                    fetchDataFromAPI();", content)
print('5:', 'loginBtn' in content)
