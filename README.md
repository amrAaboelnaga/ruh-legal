# ruh-legal

Static legal pages for the **Rūh** iOS app.

Served via GitHub Pages:

- `privacy.html` → Privacy Policy
- `terms.html` → Terms of Service
- `index.html` → landing page linking to both

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Swapping to a custom domain

When a domain is ready, add a `CNAME` file to the repo root with the domain
name and point the DNS at the GitHub Pages IPs. Update the `PRIVACY_POLICY_URL`
and `TERMS_URL` constants in `app/settings/about.tsx` of the main app.
