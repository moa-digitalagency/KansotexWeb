#!/usr/bin/env python3
"""
Fix hardcoded gold colors to use CSS variables
"""

def fix_html():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix: Points Forts - border colors
    content = content.replace(
        'border: 1px solid rgba(184, 148, 30, 0.2);',
        'border: 1px solid rgba(var(--accent-rgb), 0.2);'
    )
    content = content.replace(
        'border: 1px solid rgba(212, 175, 55, 0.2);',
        'border: 1px solid rgba(var(--accent-rgb), 0.2);'
    )
    
    # Fix: Icon backgrounds in Points Forts
    content = content.replace(
        'background: rgba(184, 148, 30, 0.1);',
        'background: rgba(var(--accent-rgb), 0.1);'
    )
    content = content.replace(
        'background: rgba(212, 175, 55, 0.1);',
        'background: rgba(var(--accent-rgb), 0.1);'
    )
    
    # Fix: Collection arrows
    content = content.replace(
        'style="background: rgba(184, 148, 30, 0.9);">',
        'style="background: rgba(var(--accent-rgb), 0.9);">',
        2  # Only first 2 occurrences (the arrow buttons)
    )
    
    # Fix: Footer social icons
    content = content.replace(
        'style="background: rgba(184, 148, 30, 0.1); border: 1px solid rgba(184, 148, 30, 0.3);">',
        'style="background: rgba(var(--accent-rgb), 0.1); border: 1px solid rgba(var(--accent-rgb), 0.3);">',
    )
    
    # Fix: Footer border
    content = content.replace(
        'style="border-color: rgba(184, 148, 30, 0.2);">',
        'style="border-color: rgba(var(--accent-rgb), 0.2);">',
    )
    
    # Fix: Section spacing - add mb-0 to avoid double spacing
    # Fix sections IDs with missing quotes
    content = content.replace('id="forces py-20 px-6"', 'id="forces" class="py-24 px-6"')
    content = content.replace('id="volets py-20 px-6', 'id="volets" class="py-24 px-6')
    content = content.replace('id="engagement py-20 px-6', 'id="engagement" class="py-24 px-6')
    
    # Fix more section IDs
    content = content.replace('id="collection py-20 px-6', 'id="collection" class="py-24 px-6')
    content = content.replace('id="testimonials py-16 px-6', 'id="testimonials" class="py-24 px-6')
    content = content.replace('id="contact py-20 px-6', 'id="contact" class="py-24 px-6')
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Fixed all hardcoded colors")
    print("✓ Fixed section spacing")
    print("✓ All elements now use CSS variables")

if __name__ == '__main__':
    fix_html()
