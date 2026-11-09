# PROJECT_AUDIT — Clustering ML Learning Documentation

Phase 1 (read-only audit) · Date: 2026-11-09 · Repository: `D:\ucup\Workspace\blog\materi-clustering`

No existing file was modified. `PROJECT_AUDIT.md` is the only file added. No build was run (see §2.5).

## 1. Existing architecture

Pipeline: Markdown in `docs/` → MkDocs 1.6 → Material theme → `site/` → GitHub Pages via `mkdocs gh-deploy` (documented, never run).

```
mkdocs.yml                 site identity, theme, nav, extensions, assets
requirements.txt           mkdocs>=1.6,<2 · mkdocs-material>=9.5,<10 · pymdown-extensions>=10.8,<13
docs/
  index.md                 landing page (grid cards)
  getting-started/index.md
  curriculum/index.md, sample-chapter.md      <- sample chapter format
  authoring/{index,code,math,components}.md
  examples/{index,mermaid}.md
  stylesheets/extra.css    55 lines, theme-aware overrides
  javascripts/mathjax.js, mermaid-config.js
  assets/vendor/mermaid/   vendored Mermaid 11.17.2 (+ LICENSE, VERSION.txt)
examples/                  NOT published; included via pymdownx.snippets (base_path: examples)
  programming/{hello.py,.c,.cpp,.js,.sh,Hello.java,students.sql}, mathematics/sigmoid.md
PRD.md, TECHNICAL_DESIGN.md, VALIDATION_REPORT.md, README.md, PROMPT_MKDOCS_TEMPLATE.md   (template-era docs)
```

Git: branch `main`, one commit (`5348860 first init`), remote `origin = git@github.com:TopekoX/mkdocs-template.git`. 

Not present: `.github/` workflows, build scripts, `overrides/` (theme partials), `mkdocs-jupyter`/nbconvert plugin, any datasets, any notebooks, any images in `docs/` (besides vendored Mermaid), `.venv/`, `site/`.

## 2. Current MkDocs configuration

### 2.1 Identity
- `site_name: Programming Course Template` and `site_description` are still the template defaults.
- **Uncommitted change** to `mkdocs.yml` (already present before this audit): `site_url`, `repo_url`, `repo_name` were repointed from `mkdocs-template` to `materi-clustering`. The git `origin` still points at `mkdocs-template`.
- `edit_uri: edit/main/docs/`.

### 2.2 Theme (`material`)
- `language: en`; `font: false` (system fonts, no Google Fonts).
- Features: `navigation.sections`, `navigation.indexes`, `navigation.path`, `navigation.footer`, `navigation.top`, `navigation.tracking`, `toc.follow`, `search.highlight`, `search.suggest`, `content.code.copy`, `content.code.annotate`, `content.tabs.link`, `content.action.edit`.
- Palette: three-state System / Light / Dark, indigo primary and accent.
- Note: `navigation.instant` is **not** enabled, although `mathjax.js` handles it via `document$`.

### 2.3 Plugins and Markdown extensions
- Plugins: `search` only.
- Extensions: `admonition`, `attr_list`, `def_list`, `footnotes`, `md_in_html`, `tables`, `toc` (permalink), `pymdownx.{arithmatex(generic), betterem, details, emoji(twemoji), highlight(anchor_linenums, line_spans, pygments_lang_class), inlinehilite, keys, mark, snippets(base_path: [examples], check_paths), superfences(mermaid fence), tabbed(alternate_style), tasklist(custom_checkbox)}`.

### 2.4 Custom assets and validation
- CSS: `stylesheets/extra.css`.
- JS (order matters): vendored Mermaid → `mermaid-config.js` → `mathjax.js` → **MathJax 3.2.2 from `cdn.jsdelivr.net`** (network needed).
- MathJax: delimiters `\(...\)` / `\[...\]` (plus `$` via arithmatex generic); only `.arithmatex` elements are processed.
- `validation`: `omitted_files`, `absolute_links`, `unrecognized_links`, `anchors` all `warn` (so `--strict` fails on any of them).

### 2.4a `nav`
Home, Getting Started, Curriculum (index + Sample Chapter), Authoring Guide (4 pages), Examples (index + Mermaid). Template placeholders; "EDIT PER SUBJECT" comments mark the intended edit points.

### 2.5 Local environment
- Python: Anaconda 3.14.7. **mkdocs, mkdocs-material, pymdown-extensions, pandas, numpy, scikit-learn, seaborn, matplotlib, jupyter, nbformat/nbconvert and ipykernel are not installed** in that interpreter. No `.venv` exists. A build and notebook execution therefore cannot be verified until a venv is created (Phase 2/3 prerequisite).
- The prior `VALIDATION_REPORT.md` records a clean `mkdocs build --strict` with mkdocs 1.6.1, Material 9.7.7, pymdown-extensions 12.3 (Python 3.14.8). Material prints an upstream "MkDocs 2.0" notice on each build; it does not fail `--strict`.

## 3. Existing theme and features

Available and reusable: light/dark/system toggle; sidebar sections and section index pages; breadcrumbs; prev/next footer; search; copy button; code annotations; titled/line-numbered code blocks; admonitions and collapsible details; content tabs; task lists (used for learning objectives in the sample chapter); tables with zebra rows; footnotes; definition lists; keyboard keys; mark; Material icons/emoji; grid cards (`md_in_html`); Mermaid (strict, theme-aware); MathJax (display scrolls horizontally inside its block); reduced-motion and focus-visible styling; mobile word-wrapping.

## 4. Existing content structure

- All content is English template placeholder text (programming-language samples: Java/C/C++/Python, loops). `curriculum/sample-chapter.md` ("Loops") is the existing chapter pattern: Learning objectives → Concept → Syntax and example (tabs, snippets) → Expected output → Cost/math → Step-by-step → Common mistakes (admonitions) → Exercises → Summary.
- Gap versus the required 14-part chapter standard: missing Introduction, Detailed Explanation, Code Explanation, How to Run, Practical Examples, Troubleshooting, References as separate sections.
- `docs/authoring/*` documents the available components and is directly reusable as the author reference.

## 5. Integration opportunities

1. **Curriculum section:** rewrite `docs/curriculum/index.md` as the 8-level roadmap; add `data-exploration-and-preprocessing/` as a section (`navigation.indexes` already supports `index.md` landing pages).
2. **Chapter template:** extend the existing sample-chapter pattern to the 14-part standard rather than inventing a new layout.
3. **Notebooks:** `pymdownx.snippets` (`base_path: [examples]`) can include `.py` excerpts from non-published sources with `check_paths: true`. Notebook source can live in a new top-level `notebooks/` (unpublished) and be linked as downloads.
4. **Dataset:** put Mall Customers under a new `data/` (or `examples/`) directory; no dataset is present now.
5. **Math:** arithmatex is configured; clustering formulas (Euclidean distance, z-score, min-max, IQR, Mahalanobis) need no config change.
6. **Diagrams:** Mermaid fits pipeline/flow figures; plots from notebooks would be static PNGs in `docs/assets/`.
7. **CSS:** a small, additive block in `extra.css` (e.g. exercise/expected-output styling) is possible, but existing admonitions probably suffice.

## 6. Potential conflicts and risks

| # | Item | Risk / Detail | Proposed handling |
|---|---|---|---|
| C1 | **`PRD.md` already exists** (template PRD, dated 2026-10-17) | The Phase 2 request to create `PRD.md` would overwrite it, violating the "do not overwrite" rule | Need your decision (see §8): e.g. `docs-project/PRD.md`, or `PRD_CLUSTERING.md`, or rename the old one to `PRD_TEMPLATE.md` |
| C2 | `TECHNICAL_DESIGN.md`, `VALIDATION_REPORT.md`, `README.md` describe the generic template | Will become stale after content changes | Leave; update `README.md` only by explicit approval |
| C3 | Uncommitted `mkdocs.yml` change; `origin` points at `mkdocs-template` | A push could target the wrong repo; `gh-deploy` would deploy to the template's repo | Do not commit/push/deploy without confirmation; ask whether to repoint `origin` |
| C4 | `site_name`, `site_description`, `language: en` are template defaults | Indonesian site with `language: en` affects search language and UI strings | Change `site_name`/`description` at integration; `theme.language: id` is supported by Material 9.x, but needs approval since it alters existing config |
| C5 | MathJax from CDN | Math requires network; QA cannot verify rendering offline | Accept (documented), or vendor later; do not change in this project without approval |
| C6 | Python 3.14 + scientific stack | pandas/numpy/scikit-learn/Jupyter wheel availability on 3.14 is unverified here; the spec targets 3.12-compatible code | Create a separate venv for notebooks; verify installability before Phase 5. A second `requirements-notebooks.txt` keeps the docs `requirements.txt` untouched |
| C7 | `mkdocs-material` pinned `<10` and in maintenance mode | Upstream notice about MkDocs 2.0 | Keep the existing caps |
| C8 | Notebooks in MkDocs | No jupyter plugin installed; adding `mkdocs-jupyter` modifies plugins and requirements | Prefer authoring Markdown chapters with code blocks, and shipping `.ipynb` as unpublished/downloadable files; ask before adding a plugin |
| C9 | Mall Customers dataset licensing/availability | Not in repo; it's a Kaggle-hosted dataset (license varies by uploader) | Need your decision on source; do not fabricate data. A synthetic equivalent could be generated by a script if allowed |
| C10 | `.shots$4.png` (80 KB) is tracked in git but its name contains `$` | It is tracked (`git ls-files`) yet resolves poorly in the shell; `.gitignore` covers `.shots/`, not this file. Looks like a stray screenshot artifact | Out of scope; flag only, do not delete without approval |
| C11 | No `navigation.instant` | none currently; if added later, `mathjax.js` already handles it | None |
| C12 | `PROMPT_MKDOCS_TEMPLATE.md` | Original template spec | Preserve untouched |

## 7. Recommended implementation strategy

1. **Environment first:** create `.venv`, install `requirements.txt`, run `mkdocs build --strict` to confirm the baseline builds before any change; record the result. Separately create a notebook venv.
2. **Planning docs (Phase 2):** resolve C1, then create `IMPLEMENTATION_PLAN.md`, `CLAUDE.md`, and the PRD under the chosen name.
3. **Structure (Phase 3), additive only:**
   ```
   docs/curriculum/index.md                  # roadmap (edit existing placeholder)
   docs/data-exploration-and-preprocessing/index.md          # Level 2 landing
   docs/data-exploration-and-preprocessing/01-introduction-to-data-exploration.md ... 12-dataset-preparation-for-clustering.md
   docs/assets/level-2/                       # figures
   data/mall_customers.csv                    # dataset (pending C9)
   notebooks/level-2/NN-*.ipynb               # executable notebooks
   ```
   Chapter template = the sample-chapter pattern extended to the 14 required sections, with `[x]` task-list objectives, tabs for code/output, admonitions for troubleshooting, arithmatex for math. Keep `sample-chapter.md` as-is (or move only on approval).
4. **Config edits limited to `nav:`** (add Level 2 entries; keep existing entries) plus approved identity fields (C4). No theme, plugin, extension, JS change planned.
5. **Chapters one at a time**, each validated with `mkdocs build --strict`, with its notebook executed via `jupyter nbconvert --execute` and its code run before the next chapter starts.
6. **QA/Release:** strict build, link/anchor check (already enforced by `validation`), notebook execution, dataset presence, manual check of math rendering (needs network), then document leftovers. No commit/push/deploy without your explicit instruction.

## 8. Decisions needed before Phase 2

1. **PRD.md collision (C1):** which name/location for the new PRD (and should the old one be renamed)?
2. **Mall Customers source (C9):** do you have the CSV, or should I use a Kaggle download / a clearly labelled synthetic replica?
3. **Site language (C4):** OK to set `theme.language: id` and update `site_name`/`site_description`?
4. **Git remote (C3):** should `origin` be repointed to `materi-clustering`?
5. **Notebook handling (C8):** ship `.ipynb` as downloadable files alongside Markdown chapters (recommended), or add the `mkdocs-jupyter` plugin?

## Stopping point

Audit complete; per the execution rules I'm stopping here for your review.
