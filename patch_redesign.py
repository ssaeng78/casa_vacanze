import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Replace the various .book buttons with the unified LINE logo button
    # In index.html: <a class="book" href="#contact"><span class="line-mark">LINE</span><span class="book-text"><span>สอบถาม</span><span>รายละเอียด</span></span></a>
    # In others: <a class="book" ...>สอบถาม<br>รายละเอียด</a>
    content = re.sub(
        r'<a class="book"[^>]*>.*?</a>',
        '<a class="book line-icon-only" href="#contact" aria-label="Contact us">LINE</a>',
        content,
        flags=re.DOTALL
    )

    # 2. Add the CSS for .line-icon-only and the brand-copy small formatting
    # We will inject it right after .brand-copy small strong{...}
    desktop_css = (
        ".brand-copy small{display:flex;align-items:center;gap:4px} "
        ".brand-copy small span:first-child:after{content:'·'} "
        ".line-icon-only{display:flex;align-items:center;justify-content:center;width:44px;height:44px;background:#06c755;color:#fff!important;border-radius:50%;font-weight:800;font-size:.85rem;text-decoration:none;box-shadow:0 4px 12px rgba(6,199,85,.3);transition:transform .2s ease} "
        ".line-icon-only:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(6,199,85,.4)} "
    )
    
    # Remove the old brand-copy small css
    content = re.sub(
        r'\.brand-copy small\{[^\}]+\}',
        '',
        content
    )
    
    # Inject our new css after brand-copy
    content = content.replace(
        '.brand-copy{',
        desktop_css + '.brand-copy{'
    )
    
    # Remove old .book and .line-mark CSS to avoid conflicts, if they exist
    content = re.sub(r'\.book\{[^\}]+\}', '', content)
    content = re.sub(r'\.line-mark\{[^\}]+\}', '', content)
    content = re.sub(r'\.book-text\{[^\}]+\}', '', content)
    content = re.sub(r'\.book-text span\{[^\}]+\}', '', content)

    # 3. Update mobile CSS to handle the stacked brand text and the nav layout
    mobile_css = (
        ".brand-copy small{flex-direction:column;align-items:flex-start;gap:0} "
        ".brand-copy small span:first-child:after{display:none} "
        "nav{justify-content:space-between} "
        ".brand{margin-right:auto} "
        ".book{order:2;margin-right:12px} "
        ".mobile-menu-toggle{order:3} "
        ".links{order:4;width:100%} "
    )
    
    # We inject this into the first @media(max-width:800px) block
    content = re.sub(r'(@media\s*\(\s*max-width:\s*[89]00px\s*\)\s*\{)', r'\1 ' + mobile_css, content, count=1)
    
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Patched {filename}")

