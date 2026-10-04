with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the stripped backticks caused by powershell earlier
content = content.replace('btn.innerHTML = <svg', "btn.innerHTML = '<svg")
content = content.replace('</path></svg> Saving...;', "</path></svg> Saving...';")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
