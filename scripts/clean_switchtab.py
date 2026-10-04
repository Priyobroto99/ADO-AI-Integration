import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the broken switchTab logic
old_block = '''                if (tabId === 'main') {
                    document.getElementById('bannerEditContainer').classList.add('hidden');
                    isEditMode = false;
                } else {
                    const m = globalData.metrics.find(x => x.engagement === currentEngagement);
                    const isAdmin = userRole && userRole.toLowerCase().includes('admin');
                    const isSpoc = m && m.spoc && currentUsername && m.spoc.trim().toLowerCase() === currentUsername.trim().toLowerCase();
                    
                    if (m && (isAdmin || isSpoc)) {
                        document.getElementById('bannerEditContainer').classList.remove('hidden');
                        document.getElementById('bannerEditContainer').classList.add('block');
                    } else {
                        document.getElementById('bannerEditContainer').classList.add('hidden');
                        document.getElementById('bannerEditContainer').classList.remove('block');
                        isEditMode = false;
                    }
                }'''

new_block = ""
text = text.replace(old_block, new_block)

# Also remove the editBtn logic in switchTab
old_btn = '''            const editBtn = document.getElementById('bannerEditBtn');
            if(editBtn) {
                if(isEditMode) {
                    editBtn.innerHTML = 'Save';
                    editBtn.classList.add('bg-tremor-brand-DEFAULT', 'text-white');
                    editBtn.classList.remove('bg-gray-100', 'text-gray-800');
                } else {
                    editBtn.innerHTML = 'Edit';
                    editBtn.classList.remove('bg-tremor-brand-DEFAULT', 'text-white');
                    editBtn.classList.add('bg-gray-100', 'text-gray-800');
                }
            }'''
text = text.replace(old_btn, "")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
