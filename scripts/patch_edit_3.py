import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

edit_btn_js = '''
        document.getElementById('bannerEditBtn').addEventListener('click', async (e) => {
            if (!isEditMode) {
                isEditMode = true;
                renderAll();
                return;
            }
            
            // Save logic
            const btn = e.target;
            const originalText = btn.innerHTML;
            btn.innerHTML = <svg class="animate-spin -ml-1 mr-2 h-3 w-3 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Saving...;
            btn.disabled = true;
            btn.classList.add('opacity-75', 'cursor-not-allowed');

            const mPayload = {};
            const dPayload = {};
            
            document.querySelectorAll('input[id^="edit_metric_"], textarea[id^="edit_detail_"], select[id^="edit_detail_"], input[id^="edit_detail_"]').forEach(el => {
                if (el.id.startsWith('edit_metric_')) {
                    const key = el.id.replace('edit_metric_', '');
                    mPayload[key] = el.value === '' ? null : el.value;
                } else if (el.id.startsWith('edit_detail_')) {
                    const key = el.id.replace('edit_detail_', '');
                    dPayload[key] = el.value === '' ? null : el.value;
                }
            });

            const teamId = globalData.metrics.find(x => x.engagement === currentEngagement).team_id;
            const token = localStorage.getItem('token');
            
            try {
                const promises = [];
                if (Object.keys(mPayload).length > 0) {
                    promises.push(fetch('http://localhost:8000/metrics/' + teamId, {
                        method: 'PUT',
                        headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                        body: JSON.stringify(mPayload)
                    }));
                }
                if (Object.keys(dPayload).length > 0) {
                    promises.push(fetch('http://localhost:8000/details/' + teamId, {
                        method: 'PUT',
                        headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
                        body: JSON.stringify(dPayload)
                    }));
                }
                
                await Promise.all(promises);
                
                // Fetch fresh data
                const [mRes, dRes] = await Promise.all([
                    fetch('http://localhost:8000/metrics', { headers: { 'Authorization': 'Bearer ' + token } }),
                    fetch('http://localhost:8000/details', { headers: { 'Authorization': 'Bearer ' + token } })
                ]);
                globalData.metrics = await mRes.json();
                globalData.details = await dRes.json();
                
                sessionStorage.setItem('dashboardData', JSON.stringify({
                    metrics: globalData.metrics,
                    details: globalData.details,
                    ragConfig: globalData.ragConfig
                }));
                sessionStorage.setItem('dashboardTimestamp', Date.now().toString());
                
                isEditMode = false;
                renderAll();
                
                const toast = document.getElementById('toast');
                toast.classList.remove('translate-y-20', 'opacity-0');
                setTimeout(() => { toast.classList.add('translate-y-20', 'opacity-0'); }, 3000);
                
            } catch(e) {
                console.error(e);
                alert("Failed to save changes. Please try again.");
            } finally {
                btn.innerHTML = 'Edit';
                btn.disabled = false;
                btn.classList.remove('opacity-75', 'cursor-not-allowed');
            }
        });
'''

# Insert it right before the window.addEventListener('DOMContentLoaded'
content = content.replace("window.addEventListener('DOMContentLoaded', async () => {", edit_btn_js + "\n        window.addEventListener('DOMContentLoaded', async () => {")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
