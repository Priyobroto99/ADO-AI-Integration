import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the broken line
broken_line = 'debugBtn.title = Debug: Role=, User=, SPOC=, isAdmin=, isSpoc=;'
fixed_line = 'debugBtn.title = `Debug: Role=${userRole}, User=${currentUsername}, SPOC=${m ? m.spoc : "None"}, isAdmin=${isAdmin}, isSpoc=${isSpoc}`;'

if broken_line in text:
    text = text.replace(broken_line, fixed_line)
else:
    print("Could not find the exact broken line. It might have different spacing.")

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
