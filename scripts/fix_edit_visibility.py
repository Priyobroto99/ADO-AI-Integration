import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''                    teamBannerDetails.classList.remove('hidden');
                    teamBannerDetails.classList.add('flex');
                }
            }'''

new_block = '''                    teamBannerDetails.classList.remove('hidden');
                    teamBannerDetails.classList.add('flex');
                }
                
                if (tabId === 'main') {
                    document.getElementById('bannerEditContainer').classList.add('hidden');
                    isEditMode = false;
                } else {
                    const m = globalData.metrics.find(x => x.engagement === currentEngagement);
                    const isAdmin = userRole && userRole.toLowerCase().includes('admin');
                    const isSpoc = m && m.spoc && currentUsername && m.spoc.trim().toLowerCase() === currentUsername.trim().toLowerCase();
                    
                    if (m && (isAdmin || isSpoc)) {
                        document.getElementById('bannerEditContainer').classList.remove('hidden');
                    } else {
                        document.getElementById('bannerEditContainer').classList.add('hidden');
                        isEditMode = false;
                    }
                }
            }
            
            const btn = document.getElementById('bannerEditBtn');
            if(btn) {
                if(isEditMode) {
                    btn.innerHTML = 'Save';
                    btn.classList.add('bg-tremor-brand-DEFAULT', 'text-white');
                    btn.classList.remove('bg-gray-100', 'text-gray-800');
                } else {
                    btn.innerHTML = 'Edit';
                    btn.classList.remove('bg-tremor-brand-DEFAULT', 'text-white');
                    btn.classList.add('bg-gray-100', 'text-gray-800');
                }
            }'''

content = content.replace(old_block, new_block)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
