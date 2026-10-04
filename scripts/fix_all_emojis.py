import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'>[^<]*?On Track</span>', r'>✅ On Track</span>', text)
text = re.sub(r'>[^<]*?At Risk</span>', r'>⚠️ At Risk</span>', text)
text = re.sub(r'>[^<]*?Off Track</span>', r'>🔴 Off Track</span>', text)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
