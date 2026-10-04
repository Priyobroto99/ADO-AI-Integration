import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Load Excel button and file input
content = re.sub(r'<input type="file" id="excelFile".*?</button>', '', content, flags=re.DOTALL)

# 2. Remove disabled from refreshBtn
content = re.sub(r'id="refreshBtn"\s*class="([^"]*?)\s*disabled:opacity-50 disabled:cursor-not-allowed"\s*disabled>', r'id="refreshBtn" class="\1">', content)

# 3. Modify empty state
content = re.sub(r'<h3 class="text-lg font-medium text-tremor-content-strong">No Data Loaded</h3>', '<h3 class="text-lg font-medium text-tremor-content-strong" id="loadingText">Loading Data from Database...</h3>', content)
content = re.sub(r'<p class="text-sm text-tremor-content mt-1 mb-6 max-w-md">Please load the CAT Delivery Excellence Tracker Excel file to view the dashboard\.</p>', '<p class="text-sm text-tremor-content mt-1 mb-6 max-w-md">Please wait while we fetch the latest data.</p>', content)
content = re.sub(r'<button onclick="document\.getElementById\(\'excelFile\'\)\.click\(\)"[^>]*>Select Excel File</button>', '', content)

# 4. Remove refreshBtn old event listener entirely
content = re.sub(r'refreshBtn\.addEventListener\(\'click\', async \(\) => \{[\s\S]*?alert\("No file loaded yet!"\);\s*\}\s*\}\);', '', content)

# Replace with the new refresh logic in script block
new_refresh = '''refreshBtn.addEventListener('click', async () => {
    const btn = document.getElementById('refreshBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-tremor-brand-DEFAULT inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Refreshing...`;
    await fetchDataFromAPI();
    btn.innerHTML = originalText;
});'''

# Insert it before updateDropdown() definition
content = content.replace('function updateDropdown()', new_refresh + '\n\n        function updateDropdown()')

# 5. Remove the window.addEventListener('DOMContentLoaded', async () => { ... XLSX.read ... }) logic
content = re.sub(r'// Autoload default Excel file if hosted on web server.*?\}\);', '', content, flags=re.DOTALL)

# Remove processFile function which depends on XLSX
content = re.sub(r'function processFile\(file\) \{.*?\/\* End processFile \*\/\s*\}', '', content, flags=re.DOTALL)
# It doesn't have an end comment. Let's not remove it, it won't hurt to just leave it as dead code.

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
