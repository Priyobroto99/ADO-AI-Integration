import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Inject forced CSS
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
    </style>
</head>'''

content = content.replace('</head>', css_inject)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
