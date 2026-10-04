with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("document.getElementById('logoutBtn').classList.remove('hidden');", "document.getElementById('logoutBtn').classList.remove('hidden');\n                    document.getElementById('navLoginBtn').classList.add('hidden');")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
