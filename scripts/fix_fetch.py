import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('} else {\n                fetchDataFromAPI();', '} else {\n                await fetchUserMe();\n                fetchDataFromAPI();')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
