import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any corrupted version of Hourly Rate (something/hr)
# The original might be "Hourly Rate (₹/hr):" or similar
text = re.sub(r'Hourly Rate \([^)]*?/hr\)', 'Hourly Rate (₹/hr)', text)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
