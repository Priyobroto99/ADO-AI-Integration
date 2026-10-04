import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_update_btn = '<button id="updateDataBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">'
new_update_btn = '<button id="updateDataBtn" class="bg-white border border-black text-black shadow-sm font-medium rounded-tremor-default text-sm px-4 py-2 transition-all duration-200 flex items-center gap-2 hidden hover:bg-blue-500 hover:border-transparent hover:text-white">'

old_back_btn = '<button id="backToDashBtn" class="bg-white border border-tremor-border text-tremor-content-emphasis shadow-sm hover:bg-gray-50 font-medium rounded-tremor-default text-sm px-4 py-2 transition-colors flex items-center gap-2 hidden">'
new_back_btn = '<button id="backToDashBtn" class="bg-white border border-black text-black shadow-sm font-medium rounded-tremor-default text-sm px-4 py-2 transition-all duration-200 flex items-center gap-2 hidden hover:bg-blue-500 hover:border-transparent hover:text-white">'

text = text.replace(old_update_btn, new_update_btn)
text = text.replace(old_back_btn, new_back_btn)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
