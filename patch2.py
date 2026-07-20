import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # Replace HTML Button
    content = re.sub(
        r'<a class="book"[^>]*>.*?</a>',
        '<a class="book line-icon-only" href="#contact" aria-label="Contact us via LINE">LINE</a>',
        content,
        flags=re.DOTALL
    )

    # 1. Desktop brand-copy small: add flex rules
    # It currently looks like: .brand-copy small{display:block;margin-top:2px;color:#51605c;font:700 .66rem/1.45 "Noto Sans Thai",sans-serif;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
    content = re.sub(
        r'(\.brand-copy small\{)display:block;',
        r'\1display:flex;align-items:center;gap:6px;',
        content,
        count=1
    )
    # Add pseudo element after it
    content = re.sub(
        r'(\.brand-copy small\{[^\}]+\})',
        r'\1.brand-copy small span:first-child:after{content:"\00B7"} ',
        content,
        count=1
    )

    # 2. Desktop line-icon-only (replace old .book / .line-mark)
    # Old .book looks like: .book{display:inline-flex;...}
    # Old .line-mark looks like: .line-mark{...}
    content = re.sub(r'\.book\{[^\}]+\}', '', content)
    content = re.sub(r'\.line-mark\{[^\}]+\}', '', content)
    content = re.sub(r'\.book-text\{[^\}]+\}', '', content)
    content = re.sub(r'\.book-text span\{[^\}]+\}', '', content)
    
    line_css = (
        ".line-icon-only{display:flex;align-items:center;justify-content:center;width:44px;height:44px;background:#06c755;color:#fff!important;border-radius:50%;font-family:'Noto Sans Thai',sans-serif;font-weight:800;font-size:.85rem;text-decoration:none;box-shadow:0 4px 12px rgba(6,199,85,.3);transition:transform .2s ease} "
        ".line-icon-only:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(6,199,85,.4)} "
    )
    content = re.sub(r'(\.links a:hover\{[^\}]+\})', r'\1' + line_css, content, count=1)

    # 3. Mobile layout
    # Currently mobile media query has: .book{order:2} (or we injected it)
    # We want brand-copy small to stack, remove bullet.
    mobile_css = (
        ".brand-copy small{flex-direction:column;align-items:flex-start;gap:0} "
        ".brand-copy small span:first-child:after{display:none} "
        ".brand{margin-right:auto} "
        ".book{order:2;margin-right:12px} "
    )
    content = re.sub(r'(@media\s*\(\s*max-width:\s*[89]00px\s*\)\s*\{)', r'\1' + mobile_css, content, count=1)
    
    # We might have `.book{order:2}` from before. Let's clean up any redundant `.book{order:2}`
    # but be careful not to delete ours. Ours is `.book{order:2;margin-right:12px}`.
    # The old one was just `.book{order:2}` followed by space or `.`
    content = re.sub(r'\.book\{order:2\}\s*', '', content)
    
    # Remove any old mobile .brand-copy small font-size tweaks that conflict
    content = re.sub(r'\.brand-copy small\{font-size:[^\}]+\}', '', content)
    content = re.sub(r'\.brand-copy small span\{display:block;font-size:[^\}]+\}', '', content)

    with open(filename, 'w') as f:
        f.write(content)

