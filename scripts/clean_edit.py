import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove bannerEditContainer from HTML
text = re.sub(r'<div id=\"bannerEditContainer\"[^>]*>.*?</div>', '', text, flags=re.DOTALL)

# 2. Remove the injected CSS
css_inject = '''    <style>
        /* FORCE DISPLAY FOR DEBUGGING */
        #bannerEditContainer {
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        #teamBannerDetails {
            display: flex !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
    </style>'''
text = text.replace(css_inject, '')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
