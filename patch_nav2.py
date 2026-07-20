import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()
    
    # Update mobile-menu-toggle css to have order: 3
    content = content.replace(
        '.mobile-menu-toggle{display:block}',
        '.mobile-menu-toggle{display:block;order:3}'
    )
    
    # Ensure links has order 4 when open
    content = content.replace(
        '.links.is-open{display:flex !important',
        '.links.is-open{display:flex !important;order:4;width:100%'
    )
    
    # Just in case, let's also make sure .book is order 2
    if '@media(max-width:800px)' in content:
        content = content.replace('@media(max-width:800px){', '@media(max-width:800px){ .book{order:2}')
    elif '@media(max-width:900px)' in content:
        content = content.replace('@media(max-width:900px){', '@media(max-width:900px){ .book{order:2}')
        
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Patched order in {filename}")

