import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

broken_str = 'btn.innerHTML = <svg'
fixed_str = 'btn.innerHTML = <svg'
text = text.replace(broken_str, fixed_str)

broken_end = '</path></svg> Authenticating...;'
fixed_end = '</path></svg> Authenticating...;'
text = text.replace(broken_end, fixed_end)

# Also let's ensure there are no other missing backticks!
# In patch_retry.py:
# btn.innerHTML = <svg ...> Waking up DB...;
text = text.replace('btn.innerHTML = <svg class=\"animate-spin', 'btn.innerHTML = <svg class=\"animate-spin')
text = text.replace('</path></svg> Waking up DB... (Retry ' + str(retries) + '/5);', '</path></svg> Waking up DB... (Retry /5);')
text = text.replace('</path></svg> Waking up DB... (Retry ', '</path></svg> Waking up DB... (Retry /5); //')

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
