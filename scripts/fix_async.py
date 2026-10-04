with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("window.addEventListener('DOMContentLoaded', () => {", "window.addEventListener('DOMContentLoaded', async () => {")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
