import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace using regex between teamBannerDetails and function end
pattern = r'(teamBannerDetails\.classList\.add\(\\\'flex\\\'\);\s*\}\s*\n)\s*if \(tabId === \\\'main\\\'\) \{.*?\}\s*\}'
text = re.sub(pattern, r'\1        }', text, flags=re.DOTALL)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
