import re

files = ['index.html', 'explore-villa.html', 'toscana-valley.html']

new_header = """<header class="topbar"><nav class="wrap"><a class="brand" href="https://casavacanze-khaoyai.com/"><span class="monogram">CV</span><span class="brand-copy">Casa Vacanze<small><span>Toscana Valley</span><span>Khao Yai · Thailand</span></small></span></a><div class="nav-right"><div class="menu-container"><button class="menu-btn" aria-label="Toggle menu" onclick="this.nextElementSibling.classList.toggle('is-open')"><svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg><span class="menu-text">Menu</span></button><div class="menu-dropdown"><div class="dropdown-header">BROWSE</div><a href="https://casavacanze-khaoyai.com/">Main Entrance</a><a href="https://casavacanze-khaoyai.com/explore-villa">Explore the Villa</a><a href="https://casavacanze-khaoyai.com/toscana-valley">About toscana-valley</a></div></div><a class="book line-icon-only" href="#contact" aria-label="Contact us via LINE"><svg viewBox="0 0 24 24"><path d="M19.365 9.863c0-2.929-3.3-5.311-7.365-5.311-4.065 0-7.365 2.382-7.365 5.311 0 2.639 2.665 4.856 6.136 5.234.241.053.567.162.648.371.073.189.048.481.022.671l-.161.972c-.021.127-.1.5.438.273.538-.228 2.9-1.708 3.992-2.95.892-1.018 1.655-2.091 1.655-4.571zm-9.351 1.709h-1.638V7.558h.682v3.332h.956v.682zm1.884 0h-.682V7.558h.682v4.014zm3.842 0h-.696l-1.464-2.223v2.223h-.682V7.558h.696l1.464 2.223V7.558h.682v4.014zm2.148 0h-1.637v-1.328h1.637v-.681h-1.637v-1.324h1.637v-.681h-2.319v4.014h2.319v-.681z"/></svg></a></div></nav></header>"""

new_css = """
.nav-right{display:flex;align-items:center;gap:12px;margin-left:auto}
.menu-container{position:relative}
.menu-btn{display:flex;align-items:center;gap:8px;background:none;border:none;cursor:pointer;padding:6px 10px;color:#073d37;font-family:'Noto Sans Thai',sans-serif;font-weight:700;font-size:.95rem;border-radius:8px;transition:background .2s}
.menu-btn:hover{background:rgba(7,61,55,.06)}
.menu-dropdown{position:absolute;top:100%;right:0;margin-top:12px;width:240px;background:#24262b;border-radius:16px;box-shadow:0 12px 34px rgba(0,0,0,.25),inset 0 1px 0 rgba(255,255,255,.1);padding:10px;display:none;flex-direction:column;z-index:100;color:#fff}
.menu-dropdown.is-open{display:flex}
.dropdown-header{font-size:.7rem;font-weight:700;letter-spacing:.1em;color:rgba(255,255,255,.4);margin:8px 12px 10px}
.menu-dropdown a{display:block;padding:12px 16px;color:#e4e6ea;text-decoration:none;font-size:.95rem;font-family:'Noto Sans Thai',sans-serif;border-radius:10px;transition:all .2s ease;font-weight:500}
.menu-dropdown a:hover,.menu-dropdown a[aria-current="page"]{background:rgba(255,255,255,.12);color:#fff}
"""

mobile_css = """
@media(max-width:800px){
  .menu-text{display:none}
  .menu-btn{padding:6px 2px}
  .menu-dropdown{position:fixed;top:74px;left:12px;right:12px;width:auto;box-shadow:0 24px 48px rgba(0,0,0,.5)}
}
"""

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Header
    content = re.sub(r'<header class="topbar">.*?</header>', new_header, content, flags=re.DOTALL)

    # 2. Clean old css
    # Desktop
    content = re.sub(r'\.mobile-menu-toggle\{[^\}]+\}', '', content)
    content = re.sub(r'\.links\{[^\}]+\}', '', content)
    content = re.sub(r'\.links a:hover\{[^\}]+\}', '', content)
    content = re.sub(r'\.nav-right\{[^\}]+\}', '', content)
    content = re.sub(r'\.menu-container\{[^\}]+\}', '', content)
    content = re.sub(r'\.menu-btn\{[^\}]+\}', '', content)
    content = re.sub(r'\.menu-btn:hover\{[^\}]+\}', '', content)
    content = re.sub(r'\.menu-dropdown\{[^\}]+\}', '', content)
    content = re.sub(r'\.menu-dropdown\.is-open\{[^\}]+\}', '', content)
    content = re.sub(r'\.dropdown-header\{[^\}]+\}', '', content)
    content = re.sub(r'\.menu-dropdown a\{[^\}]+\}', '', content)
    content = re.sub(r'\.menu-dropdown a:hover,\.menu-dropdown a\[aria-current="page"\]\{[^\}]+\}', '', content)

    # Mobile
    content = re.sub(r'\.mobile-menu-toggle\{display:block;order:3\}', '', content)
    content = re.sub(r'\.links\{display:none !important\}', '', content)
    content = re.sub(r'\.links\.is-open\{[^\}]+\}', '', content)
    content = re.sub(r'\.links\{width:100%;[^\}]+\}', '', content)
    content = re.sub(r'\.links a\{display:inline-block!important;font-size:0\.8rem\}', '', content)
    content = re.sub(r'\.book\{order:2;margin-right:12px\}', '', content)
    content = re.sub(r'\.brand\{margin-right:auto\}', '', content)

    # 3. Inject new CSS
    # Add desktop CSS after nav{...}
    content = re.sub(r'(nav\{height:74px;display:flex;align-items:center;justify-content:space-between;gap:24px\})', r'\1' + new_css.replace('\n', ' '), content, count=1)
    
    # Add mobile CSS before </style>
    content = content.replace('</style>', mobile_css.replace('\n', ' ') + '</style>')

    # 4. In case the current page needs aria-current
    if filename == 'explore-villa.html':
        content = content.replace('<a href="https://casavacanze-khaoyai.com/explore-villa">Explore the Villa</a>', '<a href="https://casavacanze-khaoyai.com/explore-villa" aria-current="page">Explore the Villa</a>')
    elif filename == 'toscana-valley.html':
        content = content.replace('<a href="https://casavacanze-khaoyai.com/toscana-valley">About toscana-valley</a>', '<a href="https://casavacanze-khaoyai.com/toscana-valley" aria-current="page">About toscana-valley</a>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Applied dropdown menu redesign.")
