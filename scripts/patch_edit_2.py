import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the render functions to pass exact keys
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')

content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')

content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')
content = content.replace('', '')

# Add logic in renderAll to show/hide the Edit button
old_render_all = '''            if (currentTab === 'main') {
                document.getElementById('engagementSelectContainer').classList.add('hidden');
                document.getElementById('teamBannerDetails').classList.add('hidden');
                document.getElementById('teamBannerDetails').classList.remove('flex');
            } else {
                document.getElementById('engagementSelectContainer').classList.remove('hidden');
                document.getElementById('teamBannerDetails').classList.remove('hidden');
                document.getElementById('teamBannerDetails').classList.add('flex');
            }'''
            
new_render_all = '''            if (currentTab === 'main') {
                document.getElementById('engagementSelectContainer').classList.add('hidden');
                document.getElementById('teamBannerDetails').classList.add('hidden');
                document.getElementById('teamBannerDetails').classList.remove('flex');
                document.getElementById('bannerEditContainer').classList.add('hidden');
                isEditMode = false;
            } else {
                document.getElementById('engagementSelectContainer').classList.remove('hidden');
                document.getElementById('teamBannerDetails').classList.remove('hidden');
                document.getElementById('teamBannerDetails').classList.add('flex');
                
                const m = globalData.metrics.find(x => x.engagement === currentEngagement);
                if (m && (userRole === 'admin' || m.spoc === currentUsername)) {
                    document.getElementById('bannerEditContainer').classList.remove('hidden');
                } else {
                    document.getElementById('bannerEditContainer').classList.add('hidden');
                }
            }
            
            const btn = document.getElementById('bannerEditBtn');
            if(isEditMode) {
                btn.innerHTML = 'Save';
                btn.classList.add('bg-tremor-brand-DEFAULT', 'text-white');
                btn.classList.remove('bg-gray-100', 'text-gray-800');
            } else {
                btn.innerHTML = 'Edit';
                btn.classList.remove('bg-tremor-brand-DEFAULT', 'text-white');
                btn.classList.add('bg-gray-100', 'text-gray-800');
            }
            '''
content = content.replace(old_render_all, new_render_all)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
