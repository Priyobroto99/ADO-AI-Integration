import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace broken unicodes
text = text.replace('âœ…', '\u2705')
text = text.replace('ðŸ”´', '\U0001F534')
text = text.replace('âšï¸', '\u26A0\uFE0F')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
