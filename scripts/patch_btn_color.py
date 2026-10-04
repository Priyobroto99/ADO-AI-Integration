import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_classes = 'class="bg-tremor-brand-DEFAULT border border-tremor-brand-DEFAULT text-white shadow-sm hover:bg-tremor-brand-emphasis font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden"'
new_classes = 'class="bg-white text-gray-900 border border-gray-300 shadow-sm hover:bg-blue-600 hover:text-white font-medium rounded-md text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden"'

content = content.replace(old_classes, new_classes)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
