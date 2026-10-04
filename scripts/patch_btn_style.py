import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_btn = '<button id="saveUpdateBtn" class="bg-tremor-brand-DEFAULT text-white px-4 py-2 rounded-tremor-default text-sm font-medium hover:bg-tremor-brand-emphasis shadow-sm">Save Changes</button>'
new_btn = '<button id="saveUpdateBtn" class="px-4 py-2 rounded-tremor-default text-sm font-medium shadow-sm transition-all duration-200 border border-black text-black bg-white hover:bg-blue-500 hover:border-transparent hover:text-white">Save Changes</button>'

text = text.replace(old_btn, new_btn)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
