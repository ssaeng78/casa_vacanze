import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the LINE text with the SVG
    content = content.replace(
        '<a class="book line-icon-only" href="#contact" aria-label="Contact us via LINE">LINE</a>',
        '<a class="book line-icon-only" href="#contact" aria-label="Contact us via LINE"><svg viewBox="0 0 24 24"><path d="M19.365 9.863c0-2.929-3.3-5.311-7.365-5.311-4.065 0-7.365 2.382-7.365 5.311 0 2.639 2.665 4.856 6.136 5.234.241.053.567.162.648.371.073.189.048.481.022.671l-.161.972c-.021.127-.1.5.438.273.538-.228 2.9-1.708 3.992-2.95.892-1.018 1.655-2.091 1.655-4.571zm-9.351 1.709h-1.638V7.558h.682v3.332h.956v.682zm1.884 0h-.682V7.558h.682v4.014zm3.842 0h-.696l-1.464-2.223v2.223h-.682V7.558h.696l1.464 2.223V7.558h.682v4.014zm2.148 0h-1.637v-1.328h1.637v-.681h-1.637v-1.324h1.637v-.681h-2.319v4.014h2.319v-.681z"/></svg></a>'
    )

    # 2. Update the CSS for .line-icon-only
    old_css = ".line-icon-only{display:flex;align-items:center;justify-content:center;width:44px;height:44px;background:#06c755;color:#fff!important;border-radius:50%;font-family:'Noto Sans Thai',sans-serif;font-weight:800;font-size:.85rem;text-decoration:none;box-shadow:0 4px 12px rgba(6,199,85,.3);transition:transform .2s ease} .line-icon-only:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(6,199,85,.4)}"
    new_css = ".line-icon-only{display:flex;align-items:center;justify-content:center;width:44px;height:44px;color:#06c755!important;text-decoration:none;transition:transform .2s ease,filter .2s ease} .line-icon-only svg{width:100%;height:100%;fill:currentColor} .line-icon-only:hover{transform:translateY(-2px);filter:drop-shadow(0 4px 10px rgba(6,199,85,.35))}"
    
    content = content.replace(old_css, new_css)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replaced LINE button with SVG in all files.")
