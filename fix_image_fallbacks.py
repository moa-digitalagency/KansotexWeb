#!/usr/bin/env python3
"""
Fix image fallback logic in templates.
Change from: content.field|image_url if content.section and content.section.field else fallback
To: (content.field|image_url) or fallback
"""

import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the broken conditional format
# {{ content.XXX.YYY|image_url if content.XXX and content.XXX.YYY else url_for('static', filename='ZZZ') }}
pattern = r'\{\{\s*(\w+\.\w+\.\w+)\|image_url\s+if\s+\w+\.\w+\s+and\s+\w+\.\w+\.\w+\s+else\s+(url_for\([^}]+\))\s*\}\}'

# Replacement with proper fallback logic
# {{ (content.XXX.YYY|image_url) or url_for('static', filename='ZZZ') }}
replacement = r'{{ (\1|image_url) or \2 }}'

# Apply replacement
new_content = re.sub(pattern, replacement, content)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Count changes
changes = content.count('image_url if') - new_content.count('image_url if')
print(f"✅ Fixed {changes} image fallback conditions")
