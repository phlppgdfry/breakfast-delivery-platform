from html.parser import HTMLParser
from pathlib import Path
import unittest


class LocalAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if (
                key in ("href", "src")
                and value
                and not value.startswith(("https:", "http:", "#"))
            ):
                self.references.append(value)


class ShowcaseTests(unittest.TestCase):
    def test_public_showcase_assets_and_identity_are_complete(self):
        root = Path(__file__).resolve().parents[1]
        parser = LocalAssets()
        page = (root / "index.html").read_text()
        parser.feed(page)
        for reference in parser.references:
            self.assertTrue((root / reference).exists(), reference)
        self.assertEqual(
            (root / "favicon.svg").read_bytes(),
            (root / "demo/web/favicon.svg").read_bytes(),
        )
        self.assertIn('rel="canonical"', page)
        self.assertIn("Local application", page)
