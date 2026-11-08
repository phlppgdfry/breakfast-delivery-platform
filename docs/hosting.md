# Public project page

URL: https://phlppgdfry.github.io/breakfast-delivery-platform/

GitHub Pages serves the repository root from main with `.nojekyll`. `index.html`, `showcase.css`, root branding assets and the screenshots in docs are static. There is no server-side execution on Pages.

The public page explains the product, displays actual screenshots and a reproducible synthetic baseline, and links to the source, architecture, validation and run instructions. The interactive Python/SQLite application runs locally with `python3 -m demo.server`. The page explicitly distinguishes those two surfaces.

Root favicons, SVG logo, Apple touch icon, manifest with relative scope/start URL, canonical URL, Open Graph image, mobile layout and a custom 404 page are included. The browser suite starts a separate static server and checks the public page, main anchor, screenshot and three viewport widths. `test_showcase.py` checks local asset references and shared brand identity.

To update the public page, edit the root HTML/CSS and push main. The Pages deployment appears under GitHub Actions. Do not place private runtime data in tracked files; var and node_modules stay ignored.
