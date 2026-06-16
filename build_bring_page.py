#!/usr/bin/env python3
"""
build_bring_page.py — regenerate index.html from bring_items.txt (standalone repo).

Run after editing the shopping list:
    python build_bring_page.py
Then:  git add . && git commit -m "update list" && git push
GitHub Pages redeploys automatically; the Bring! import link always pulls the latest.
"""
import html
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ITEMS = os.path.join(ROOT, "bring_items.txt")
OUT = os.path.join(ROOT, "index.html")


def load_items():
    items = []
    with open(ITEMS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" in line:
                name, spec = (p.strip() for p in line.split("|", 1))
            else:
                name, spec = line, ""
            items.append(f"{spec} {name}".strip())  # amount first, e.g. "600 g turkey mince"
    return items


def main():
    items = load_items()
    ld = ",\n      ".join(f'"{html.escape(i)}"' for i in items)
    li = "\n    ".join(f"<li>{html.escape(i)}</li>" for i in items)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Weekly Grocery List</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
    li {{ margin: .15rem 0; }}
    .btn {{ display: inline-block; background: #e30613; color: #fff; text-decoration: none;
           font-weight: 600; padding: .9rem 1.4rem; border-radius: 10px; font-size: 1.05rem; }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Recipe",
    "name": "Weekly Grocery List",
    "recipeYield": "1 week",
    "recipeCategory": "Groceries",
    "recipeInstructions": "Add all items to your Bring! list, then shop.",
    "recipeIngredient": [
      {ld}
    ]
  }}
  </script>
</head>
<body>
  <h1>🛒 Weekly Grocery List</h1>
  <p>
    <a class="btn" href="https://api.getbring.com/rest/bringrecipes/deeplink?url=https%3A%2F%2Friedd2.github.io%2Fbring-import%2F&amp;source=web">
      🛒 Import to Bring!
    </a>
  </p>
  <ul>
    {li}
  </ul>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Wrote {len(items)} items to {OUT}")


if __name__ == "__main__":
    main()
