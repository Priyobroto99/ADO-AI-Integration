import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'\} else \{\s*fetchDataFromAPI\(\);\s*\}', '} else { await fetchUserMe(); fetchDataFromAPI(); }', content)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
