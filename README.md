# Unicorn Overlord SEO Engine

A search-engine-optimized tactical RPG fan site for *Unicorn Overlord*. Each page maps gear, AP/PP tactics and formation roles to a playable squad, connected to an interactive team builder that generates shareable URLs.

## Live preview

Open `index.html` with any static server (e.g. `python -m http.server 8000`) and visit `http://localhost:8000`.

## Project structure

```
my-website/
├── index.html              # Homepage
├── guides/                 # Wiki-style site index (70 characters by faction)
│   └── index.html
├── characters/
│   └── alain/              # Character build page
├── classes/
│   └── warrior/            # Class guide page
├── equipment/
│   └── kingsblade/         # Equipment page
├── teams/
│   └── alain-frontline/    # Team composition page
├── team-builder/           # Interactive squad planner (save + share URL)
│   └── index.html
├── assets/
│   ├── site.css            # Global styles (dark gold tactics theme)
│   ├── data.js             # Unit data
│   ├── builder.js          # Team builder logic
│   └── chars/              # 70 local character portraits
├── scripts/                # Python generators (extract data → build pages)
└── PROMPT.md               # Original content requirements
```

## Tech stack

- Vanilla HTML / CSS / JS (no build step, no framework)
- Python scripts to scrape + generate pages
- Mobile responsive (720px / 460px breakpoints)

## SEO features

- Unique `title` + `meta description` on every page
- Correct H1 → H2 → H3 heading hierarchy
- JSON-LD structured data (`TechArticle`) on key pages
- Internal link network between characters, classes, equipment and teams
- Conversion hooks pointing to the Team Builder

## License

Unofficial fan reference. *Unicorn Overlord* is a trademark of its respective owner.
