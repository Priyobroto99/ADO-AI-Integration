import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# I want to replace `parsed.join(\'\\n\');` with `parsed.join('\\n');`
text = text.replace(r"parsed.join(\'\\n\');", r"parsed.join('\n');")
text = text.replace(r"val.split(\'\\n\')", r"val.split('\n')")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
