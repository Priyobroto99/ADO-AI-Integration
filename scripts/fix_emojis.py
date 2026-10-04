import codecs

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace corrupted strings
text = text.replace('âœ…', '?')
text = text.replace('ðŸ”´', '??')
text = text.replace('âš ï¸', '??')

# Also in case they were slightly different:
text = text.replace('âš\x8fï¸\x8f', '??')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
