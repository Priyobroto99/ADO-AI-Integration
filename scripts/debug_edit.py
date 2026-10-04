import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''                    const m = globalData.metrics.find(x => x.engagement === currentEngagement);
                    const isAdmin = userRole && userRole.toLowerCase().includes('admin');
                    const isSpoc = m && m.spoc && currentUsername && m.spoc.trim().toLowerCase() === currentUsername.trim().toLowerCase();
                    
                    if (m && (isAdmin || isSpoc)) {
                        document.getElementById('bannerEditContainer').classList.remove('hidden');
                    } else {
                        document.getElementById('bannerEditContainer').classList.add('hidden');
                        isEditMode = false;
                    }'''

new_block = '''                    const m = globalData.metrics.find(x => x.engagement === currentEngagement);
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
                    // }'''

content = content.replace(old_block, new_block)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
