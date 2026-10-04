import re

with open('frontend/cat_dashboard.html', 'rb') as f:
    b = f.read()

# Fix Financial Savings Rupee
b = b.replace(b'\xc3\xa2\xe2\x80\x9a\xc2\xb9', b'\xe2\x82\xb9')

# Fix Em Dash double encoding (often caused by —)
b = b.replace(b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d', b'\xe2\x80\x94')

# Fix Track Trend (ðŸ“ˆ -> 📈)
b = b.replace(b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xcb\x86 Track Trend', b'\xf0\x9f\x93\x88 Track Trend')

# Fix Informational (ðŸ“Š -> 📊)
b = b.replace(b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc5\xa0 Informational', b'\xf0\x9f\x93\x8a Informational')

with open('frontend/cat_dashboard.html', 'wb') as f:
    f.write(b)
