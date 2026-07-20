import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace HTML Button
    content = re.sub(
        r'<a class="book"[^>]*>.*?</a>',
        '<a class="book line-icon-only" href="#contact" aria-label="Contact us via LINE">LINE</a>',
        content,
        flags=re.DOTALL
    )

    # 1. Desktop brand-copy small: add flex rules
    content = re.sub(
        r'(\.brand-copy small\{)display:block;',
        r'\1display:flex;align-items:center;gap:6px;',
        content,
        count=1
    )
    # Add pseudo element after it
    content = re.sub(
        r'(\.brand-copy small\{[^\}]+\})',
        r'\1.brand-copy small span:first-child:after{content:"·"} ',
        content,
        count=1
    )

    # 2. Desktop line-icon-only
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
    mobile_css = (
        ".brand-copy small{flex-direction:column;align-items:flex-start;gap:0} "
        ".brand-copy small span:first-child:after{display:none} "
        ".brand{margin-right:auto} "
        ".book{order:2;margin-right:12px} "
    )
    content = re.sub(r'(@media\s*\(\s*max-width:\s*[89]00px\s*\)\s*\{)', r'\1' + mobile_css, content, count=1)
    
    content = re.sub(r'\.book\{order:2\}\s*', '', content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

