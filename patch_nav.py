import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()
    
    # Update the brand text
    content = re.sub(
        r'<span class="brand-copy">Casa Vacanze<small>.*?</small></span>',
        '<span class="brand-copy">Casa Vacanze<small><span>Toscana Valley</span><span>Khao Yai · Thailand</span></small></span>',
        content,
        flags=re.DOTALL
    )
    
    # Add hamburger button before <div class="links">
    if '<button class="mobile-menu-toggle"' not in content:
        content = content.replace(
            '<div class="links">',
            '<button class="mobile-menu-toggle" aria-label="Toggle menu" onclick="this.nextElementSibling.classList.toggle(\'is-open\')"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button><div class="links">'
        )
    
    # Update CSS
    # First, inject default mobile-menu-toggle display: none
    if '.mobile-menu-toggle' not in content:
        content = content.replace(
            '.brand{',
            '.mobile-menu-toggle{display:none;background:none;border:none;color:#073d37;cursor:pointer;padding:4px}.brand{'
        )
    
    # Find the mobile media query and update .links to display none by default
    # and add .links.is-open {display:flex;}
    # Also update brand-copy small span for mobile
    
    if '.links.is-open' not in content:
        mobile_css = ".mobile-menu-toggle{display:block}.links{display:none !important}.links.is-open{display:flex !important;flex-direction:column;gap:12px;padding:16px 0;}.brand-copy small span{display:block;font-size:0.75rem;line-height:1.4;margin-top:2px}"
        
        # Replace the existing .links rule in max-width:800px or 900px
        # We can just inject this at the beginning of the first @media(max-width...
        
        content = re.sub(r'(@media\s*\(\s*max-width:\s*[89]00px\s*\)\s*\{)', r'\1 ' + mobile_css + ' ', content, count=1)
    
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Updated {filename}")

