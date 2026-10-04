import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('btn.innerHTML = \\<svg', 'btn.innerHTML = `<svg')
text = text.replace('btn.innerHTML = <svg', 'btn.innerHTML = `<svg')
text = text.replace('Authenticating...\\;', 'Authenticating...`;')
text = text.replace('Authenticating...;', 'Authenticating...`;')
text = text.replace('Waking up DB... (Retry ${retries}/5)\\;', 'Waking up DB... (Retry ${retries}/5)`;')
text = text.replace('Waking up DB... (Retry ${retries}/5);', 'Waking up DB... (Retry ${retries}/5)`;')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
