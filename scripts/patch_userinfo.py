with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

html_to_add = '''<div class="flex items-center gap-3">
                    <div id="userInfoDisplay" class="hidden flex-col text-right mr-3 pr-3 border-r border-tremor-border">
                        <span id="displayUsername" class="text-sm font-semibold text-tremor-content-strong leading-tight"></span>
                        <span id="displayRole" class="text-xs text-tremor-content font-medium uppercase tracking-wider"></span>
                    </div>'''

content = content.replace('<div class="flex items-center gap-3">', html_to_add, 1) # Only replace the first occurrence (wait, there are two of them? Let me verify)
