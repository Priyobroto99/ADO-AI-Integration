import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''<div class="flex items-center gap-3">
                    <div id="userInfoDisplay" class="hidden flex-col text-right mr-3 pr-3 border-r border-tremor-border">
                        <span id="displayUsername" class="text-sm font-semibold text-tremor-content-strong leading-tight"></span>
                        <span id="displayRole" class="text-xs text-tremor-content font-medium uppercase tracking-wider"></span>
                    </div>
                    <span id="lastUpdated"'''

content = re.sub(r'<div class="flex items-center gap-3">\s*<span id="lastUpdated"', replacement, content)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
