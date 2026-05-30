import re, os

base = r'C:\Users\grend\Documents\saturnplaner'
files = [
    'index.html','about.html','agb.html','blog.html','community.html',
    'datenschutz.html','impressum.html','journal-prompts.html',
    'juni-challenge.html','planeten.html','tipps.html','newsletter.html'
]

NEW_CSS = (
    '  [data-theme="dark"] html{background:#1E1428;}\n'
    '  [data-theme="dark"] body{filter:invert(0.92) hue-rotate(180deg) brightness(1.1);}\n'
    '  [data-theme="dark"] img,[data-theme="dark"] video,[data-theme="dark"] iframe,'
    '[data-theme="dark"] .banner,[data-theme="dark"] footer,'
    '[data-theme="dark"] #cookieBanner{filter:invert(1) hue-rotate(180deg);}'
)

NEW_JS = (
    "function toggleTheme(){var isDark=document.documentElement.getAttribute('data-theme')==='dark';"
    "var t=isDark?'light':'dark';document.documentElement.setAttribute('data-theme',t);"
    "var btn=document.getElementById('theme-toggle');"
    "if(btn)btn.textContent=isDark?'\U0001F319':'☀️';"
    "localStorage.setItem('theme',t);}\n"
    "document.addEventListener('DOMContentLoaded',function(){var saved=localStorage.getItem('theme')||'light';"
    "var btn=document.getElementById('theme-toggle');"
    "if(btn)btn.textContent=saved==='dark'?'☀️':'\U0001F319';});"
)

# Matches the old complex dark mode CSS block (stops just before the blank line + </style>)
css_pat = re.compile(
    r'  \[data-theme="dark"\] html,\[data-theme="dark"\] body\{background:#1C1028.*?(?=\n\n</style>)',
    re.DOTALL
)

# Matches the entire old theme-toggle JS block in index.html (// Theme Toggle ... }); blank line before // Mobile Menu)
js_pat = re.compile(
    r'// Theme Toggle\n(?:var|const) DARK = \{.*?\}\);\n(?=\n// Mobile Menu)',
    re.DOTALL
)

for fname in files:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Fix CSS
    content, n = css_pat.subn(NEW_CSS, content)
    css_status = f'CSS: {n} replacement(s)' if n else 'CSS: NO MATCH'

    # Fix JS (index.html only)
    js_status = ''
    if fname == 'index.html':
        new_block = '// Theme Toggle\n' + NEW_JS + '\n'
        content, n2 = js_pat.subn(new_block, content)
        js_status = f' | JS: {n2} replacement(s)' if n2 else ' | JS: NO MATCH'

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'[FIXED] {fname} — {css_status}{js_status}')
    else:
        print(f'[SKIP]  {fname} — {css_status}{js_status}')

print('\nDone!')
