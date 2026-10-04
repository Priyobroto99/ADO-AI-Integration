import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_svg = '<svg class="w-8 h-8 text-tremor-brand-DEFAULT" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>'

new_svg = '''<svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="barGrad1" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#3b82f6" />
      <stop offset="100%" stop-color="#8b5cf6" />
    </linearGradient>
    <linearGradient id="barGrad2" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#3b82f6" />
    </linearGradient>
    <linearGradient id="barGrad3" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#8b5cf6" />
      <stop offset="100%" stop-color="#ec4899" />
    </linearGradient>
  </defs>
  
  <rect x="4" y="14" width="4" height="6" rx="1" fill="url(#barGrad1)">
    <animate attributeName="height" values="6; 14; 6" dur="1.5s" repeatCount="indefinite" />
    <animate attributeName="y" values="14; 6; 14" dur="1.5s" repeatCount="indefinite" />
  </rect>
  
  <rect x="10" y="8" width="4" height="12" rx="1" fill="url(#barGrad2)">
    <animate attributeName="height" values="12; 4; 16; 12" dur="2s" repeatCount="indefinite" />
    <animate attributeName="y" values="8; 16; 4; 8" dur="2s" repeatCount="indefinite" />
  </rect>
  
  <rect x="16" y="12" width="4" height="8" rx="1" fill="url(#barGrad3)">
    <animate attributeName="height" values="8; 14; 5; 8" dur="1.7s" repeatCount="indefinite" />
    <animate attributeName="y" values="12; 6; 15; 12" dur="1.7s" repeatCount="indefinite" />
  </rect>
</svg>'''

text = text.replace(old_svg, new_svg)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
