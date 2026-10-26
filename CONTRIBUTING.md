# Contributing to Technology Story Notebook

Thanks for looking. This is a small personal notebook for turning what you know about a technology into a confident interview story. It exists in **two independent implementations of the same idea**:

- **Browser version** — one dependency-free `index.html` (vanilla HTML/CSS/JavaScript), data in `localStorage`, published via GitHub Pages.
- **Desktop version** — `start.py`, a Python/Tkinter app storing stories as files under `stories/`.

The two versions do **not** sync (the README says so plainly). Contributions of code, story templates, docs, and bug reports are all welcome.

## Run it locally

Browser version — nothing to install:

```bash
git clone https://github.com/vilaswasnik/technology-story-notebook.git
cd technology-story-notebook
# open index.html in a browser, or:
python3 -m http.server 8000
```

Desktop version — needs Python with Tkinter:

```bash
python start.py
```

## Ground rules

1. **One model, two implementations.** The shared model is: a list of technologies, one story text per technology, a user-controlled order. If you change the model or add a feature, either implement it in both versions or scope your PR clearly to one and say why.
2. **Browser version stays dependency-free.** No frameworks, no build step, no CDN requirements — a single file that works offline and on GitHub Pages.
3. **User notes are sacred.** Both storage formats (`localStorage` keys; `stories/<technology>/story.txt` + `.technology_order.json`) are user data. Changes must migrate or stay backward-compatible — never silently discard existing stories.
4. **Personal notes stay personal.** Real `stories/` content is not sample data; don't commit your own stories as fixtures. Use invented examples.

## Filing an issue

Use GitHub Issues. Say which version (browser/desktop), and for the browser version which browser. For data-loss reports, describe exactly what was saved, where, and what you found afterwards — those get priority.

## PR process

1. Fork, branch from `main`, keep the change focused.
2. Test the version you touched (both, if you changed the shared model), including with pre-existing saved stories.
3. Note in the PR description which version(s) you changed and how you tested.
4. One approval from the maintainer merges; pushes to `main` redeploy the Pages site.

## Good first issues

Concrete, evidence-based starting points (each cites where the gap is):

1. **Add export/import to the browser version.** Today browser stories live only in `localStorage` and can't move to the desktop version (or another browser). A JSON export/import matching the desktop `stories/` layout would close the gap the README calls out.
2. **Add screenshots to the README.** Neither UI is pictured — one screenshot each of the browser and desktop versions would show visitors what they're getting in seconds.
3. **Ship an empty-state story template.** The README's interview-preparation template exists only as documentation; pre-loading it as the placeholder/first-run content in both versions would put it where users actually write.
4. **Guard the desktop order file.** `start.py` reads `stories/.technology_order.json` on startup — a corrupt or hand-edited file shouldn't crash the app. Add a tolerant load with a sensible fallback order.
