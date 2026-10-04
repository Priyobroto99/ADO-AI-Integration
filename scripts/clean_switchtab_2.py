import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# I will find the block:
#                 if (tabId === 'main') {
#                     document.getElementById('bannerEditContainer').classList.add('hidden');
# and everything down to the end of switchTab

old_block = '''                if (tabId === 'main') {
                    document.getElementById('bannerEditContainer').classList.add('hidden');
                    isEditMode = false;
                } else {
                    const m = globalData.metrics.find(x => x.engagement === currentEngagement);
                    const isAdmin = userRole && userRole.toLowerCase().includes('admin');
                    const isSpoc = m && m.spoc && currentUsername && m.spoc.trim().toLowerCase() === currentUsername.trim().toLowerCase();
                    
                    // FORCE SHOW FOR DEBUGGING
                    document.getElementById('bannerEditContainer').classList.remove('hidden');
                    
                    const debugBtn = document.getElementById('bannerEditBtn');
                    if(debugBtn && !isEditMode) {
                        debugBtn.title = Debug: Role=, User=, SPOC=, isAdmin=, isSpoc=;
                    }
                    
                    // Actually, if we just want to bypass it for them to test:
                    // document.getElementById('bannerEditContainer').classList.remove('hidden');
                    // if (!m || (!isAdmin && !isSpoc)) {
                    //    // They would normally be blocked here
                    // }
                }
            }
            
            const editBtn = document.getElementById('bannerEditBtn');
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

text = text.replace(old_block, '            }')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
