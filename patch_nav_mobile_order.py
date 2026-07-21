import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add .nav-right { flex-direction: row-reverse; } to the mobile media query we just added
    content = content.replace(
        '@media(max-width:800px){   .menu-text{display:none}',
        '@media(max-width:800px){ .nav-right{flex-direction:row-reverse}  .menu-text{display:none}'
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

