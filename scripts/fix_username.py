import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add currentUsername global
if 'let currentUsername = null;' not in content:
    content = content.replace('let userRole = null;', 'let userRole = null;\n        let currentUsername = null;')

# 2. Set currentUsername in fetchUserMe
old_fetch_user = "userRole = user.role;"
new_fetch_user = "userRole = user.role;\n                    currentUsername = user.username;"
content = content.replace(old_fetch_user, new_fetch_user)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
