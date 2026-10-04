with open('patch_update_form.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('content = content.replace(old_html, new_html)', 'content = content.replace(new_html, old_html)')
text = text.replace('content = content.replace(old_js, new_js)', 'content = content.replace(new_js, old_js)')
text = text.replace('content = content.replace(old_save_js, new_save_js)', 'content = content.replace(new_save_js, old_save_js)')
text = text.replace('content = content.replace(old_btn, new_btn)', 'content = content.replace(new_btn, old_btn)')

with open('reverse_patch_update_form.py', 'w', encoding='utf-8') as f:
    f.write(text)
