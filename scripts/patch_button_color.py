import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace button classes
old_class = 'class="bg-tremor-brand-DEFAULT text-white px-4 py-2 rounded-tremor-default text-sm font-medium hover:bg-tremor-brand-emphasis shadow-sm"'
new_class = 'class="bg-tremor-brand-DEFAULT text-black hover:text-black px-4 py-2 rounded-tremor-default text-sm font-medium hover:bg-tremor-brand-emphasis shadow-sm"'
content = content.replace(old_class, new_class)

# Replace SVG text color
old_svg = 'text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"'
new_svg = 'text-black inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"'
content = content.replace(old_svg, new_svg)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
