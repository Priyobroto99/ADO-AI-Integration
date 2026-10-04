import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure emptyState removal of flex is explicitly added
content = content.replace("document.getElementById('emptyState').classList.add('hidden');", "document.getElementById('emptyState').classList.add('hidden');\n                    document.getElementById('emptyState').classList.remove('flex');")

# Fix spacing issues if it added it too many times
content = re.sub(r"(document.getElementById\('emptyState'\).classList.remove\('flex'\);\s*)+", "document.getElementById('emptyState').classList.remove('flex');\n", content)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
