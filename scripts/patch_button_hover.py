import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace button classes with important tags
old_class = 'class="bg-tremor-brand-DEFAULT text-black hover:text-black px-4 py-2 rounded-tremor-default text-sm font-medium hover:bg-tremor-brand-emphasis shadow-sm"'
new_class = 'class="bg-tremor-brand-DEFAULT !text-black hover:!text-black px-4 py-2 rounded-tremor-default text-sm font-medium hover:bg-tremor-brand-emphasis shadow-sm"'
content = content.replace(old_class, new_class)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
