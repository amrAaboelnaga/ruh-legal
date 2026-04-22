#!/usr/bin/env python3
"""Convert PRIVACY.md and TERMS.md (from the app repo) to HTML pages in this
folder, substituting the values we know.
"""
import pathlib
import markdown

HERE = pathlib.Path(__file__).parent
APP = pathlib.Path('/Users/amraboelnaga/Desktop/reciting-app-mob')

REPLACEMENTS = [
    ('[App Name]', 'Rūh'),
    ('[Developer Legal Name]', 'Amr Aboelnaga'),
    ('[Developer Legal Name TBD]', 'Amr Aboelnaga'),
    ('[contact@example.com — TBD]', 'amr@verific.ai'),
    ('[TBD — fill in before publishing]', '21 April 2026'),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rūh — {title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="wrap">
    <a class="back" href="index.html">&larr; Rūh Legal</a>
    <article>
{body}
    </article>
    <footer>
      <p><a href="index.html">Rūh Legal</a> &middot; {other_link}</p>
    </footer>
  </main>
</body>
</html>
"""

def convert(md_filename: str, out_filename: str, title: str, other_link: str):
    src = (APP / md_filename).read_text(encoding='utf-8')
    # Strip the internal "Items the developer must fill in" section at the
    # end — it's internal pre-publish notes, not user-facing content.
    for marker in ('## Items the developer must fill in before publishing',
                   '## Operational items (NOT part of the terms text',
                   '## Legal note'):
        idx = src.find(marker)
        if idx >= 0:
            src = src[:idx]

    # Apply known substitutions.
    for a, b in REPLACEMENTS:
        src = src.replace(a, b)

    # Normalise dash-lists that follow a colon-terminated intro without a
    # blank line — the default markdown parser treats those as a single
    # paragraph rather than a list.
    import re
    src = re.sub(r'(:\s*\n)(- )', r'\1\n\2', src)

    # TERMS.md links to PRIVACY.md with a relative markdown path — rewrite
    # to the published HTML filename for the hosted site.
    src = src.replace('./PRIVACY.md', 'privacy.html')
    src = src.replace('(PRIVACY.md)', '(privacy.html)')
    src = src.replace('THIRD_PARTY_NOTICES.md', 'third-party-notices.html')

    html = markdown.markdown(
        src,
        extensions=['extra', 'sane_lists', 'smarty', 'tables'],
    )
    # Remove the leading h1 so it doesn't duplicate the page title baked in
    # article styling.
    # Actually keep it — article h1 is the page title by design.

    out = (HERE / out_filename)
    out.write_text(TEMPLATE.format(title=title, body=html, other_link=other_link), encoding='utf-8')
    print(f"wrote {out_filename}")

convert('PRIVACY.md', 'privacy.html', 'Privacy Policy',
        '<a href="terms.html">Terms of Service</a>')
convert('TERMS.md', 'terms.html', 'Terms of Service',
        '<a href="privacy.html">Privacy Policy</a>')

# THIRD_PARTY_NOTICES — short, same treatment
src = (APP / 'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
for a, b in REPLACEMENTS:
    src = src.replace(a, b)
html = markdown.markdown(src, extensions=['extra', 'sane_lists', 'smarty', 'tables'])
(HERE / 'third-party-notices.html').write_text(
    TEMPLATE.format(title='Third-Party Notices', body=html,
                    other_link='<a href="privacy.html">Privacy Policy</a> &middot; <a href="terms.html">Terms of Service</a>'),
    encoding='utf-8',
)
print('wrote third-party-notices.html')
