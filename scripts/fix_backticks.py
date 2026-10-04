import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix return <div ... > to return `<div ... >
text = text.replace('return <div class="bg-white rounded-tremor-default', 'return `<div class="bg-white rounded-tremor-default')
text = text.replace('</div>;', '</div>`;')

text = text.replace('return <div class="bg-tremor-background-muted', 'return `<div class="bg-tremor-background-muted')
# it shares </div>; so the previous replace handles it

text = text.replace('return <div class="flex items-center justify-between', 'return `<div class="flex items-center justify-between')
# it shares </div>; so the previous replace handles it

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
