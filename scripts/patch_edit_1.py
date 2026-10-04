import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add isEditMode flag
if 'let isEditMode = false;' not in content:
    content = content.replace('let currentTab = "main";', 'let currentTab = "main";\n        let isEditMode = false;')

# 2. Add Edit Button to Banner
old_banner_details = '''                    <div id="teamBannerDetails" class="hidden flex-col gap-1 border-t sm:border-t-0 sm:border-l border-tremor-border pt-3 sm:pt-0 sm:pl-6">
                        <div class="text-xs text-tremor-content">
                            CAT Manager: <span id="bannerCatManager" class="font-semibold text-tremor-content-strong">--</span>
                        </div>
                        <div class="text-xs text-tremor-content">
                            Engagement Code: <span id="bannerEngagementCode" class="font-semibold text-tremor-content-strong">--</span>
                        </div>
                    </div>'''

new_banner_details = '''                    <div id="teamBannerDetails" class="hidden flex-col gap-1 border-t sm:border-t-0 sm:border-l border-tremor-border pt-3 sm:pt-0 sm:pl-6">
                        <div class="text-xs text-tremor-content">
                            CAT Manager: <span id="bannerCatManager" class="font-semibold text-tremor-content-strong">--</span>
                        </div>
                        <div class="text-xs text-tremor-content">
                            Engagement Code: <span id="bannerEngagementCode" class="font-semibold text-tremor-content-strong">--</span>
                        </div>
                    </div>
                    <div id="bannerEditContainer" class="hidden border-t sm:border-t-0 sm:border-l border-tremor-border pt-3 sm:pt-0 sm:pl-6">
                        <button id="bannerEditBtn" class="bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-medium px-3 py-1.5 rounded border border-gray-300 shadow-sm transition-colors">Edit</button>
                    </div>'''

content = content.replace(old_banner_details, new_banner_details)

# 3. Update createCard
old_create_card = '''        function createCard(title, value, metricKey, suffix="", subLabel="") {'''
new_create_card = '''        function createCard(title, value, metricKey, suffix="", subLabel="", isDetail=false, overrideKey="") {
            if (isEditMode && (overrideKey || (metricKey !== RAG.NONE && metricKey !== RAG.GREEN && metricKey !== RAG.YELLOW && metricKey !== RAG.RED))) {
                const k = overrideKey || metricKey;
                const fieldId = isDetail ? 'edit_detail_' + k : 'edit_metric_' + k;
                return <div class="bg-white rounded-tremor-default border border-tremor-border shadow-tremor-card p-4 ring-1 ring-tremor-border">
                    <p class="text-sm text-tremor-content-subtle font-medium truncate"></p>
                    <input type="text" id="" value="" class="mt-2 block w-full border border-tremor-border rounded-md px-2 py-1 text-sm text-gray-700">
                </div>;
            }'''
content = content.replace(old_create_card, new_create_card)

# 4. Update createListPanel
old_list_panel = '''        function createListPanel(title, rawPoints) {'''
new_list_panel = '''        function createListPanel(title, rawPoints, detailKey="") {
            if (isEditMode && detailKey) {
                return <div class="bg-tremor-background-muted rounded-tremor-default border border-tremor-border p-4">
                    <p class="text-sm font-medium text-tremor-content-strong mb-2"></p>
                    <textarea id="edit_detail_" class="block w-full border border-tremor-border rounded-md px-2 py-1 text-sm text-gray-700" rows="3"></textarea>
                    <p class="text-xs text-gray-400 mt-1">Separate points with |</p>
                </div>;
            }'''
content = content.replace(old_list_panel, new_list_panel)

# 5. Update createYesNoBadge
old_yesno = '''        function createYesNoBadge(title, value, rag = RAG.NONE) {'''
new_yesno = '''        function createYesNoBadge(title, value, rag = RAG.NONE, detailKey="") {
            if (isEditMode && detailKey) {
                return <div class="flex items-center justify-between p-3 rounded-tremor-default border border-tremor-border bg-white shadow-sm">
                    <span class="text-sm font-medium text-tremor-content-strong"></span>
                    <select id="edit_detail_" class="border border-tremor-border rounded-md px-2 py-1 text-sm text-gray-700">
                        <option value="" >--</option>
                        <option value="Yes" >Yes</option>
                        <option value="No" >No</option>
                    </select>
                </div>;
            }'''
content = content.replace(old_yesno, new_yesno)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
