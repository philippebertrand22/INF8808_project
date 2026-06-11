# Dash application — Mapping the evolution of global music trends

Scrollable, article-like Dash application for the INF8808E project
(team 5). Current state : article header, introduction and
visualisation 1 (audio characteristics over time, with major global
crises highlighted). The other visualisations will be added one section
at a time.

## Running the app

```bash
cd src
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 server.py
```

Then open http://127.0.0.1:8050/ in a browser.

**No raw data needed** : the aggregated tables used by the figures are
committed in `assets/data/`, so the app runs out of the box. The raw
dataset (`data/tracks.csv`, stored with Git LFS) is only needed to
rebuild those tables after a change to `preprocess.py` — delete the
cached CSV and restart the app.

## Structure

| File | Role |
| --- | --- |
| `server.py` | Flask failsafe server (entry point) |
| `app.py` | Dash application : page layout and story text |
| `preprocess.py` | Data aggregation and caching |
| `line_chart.py` | Visualisation 1 — characteristics over time and crises |
| `hover_template.py` | Tooltip templates |
| `helper.py` | Shared colors and layout adjustments |
| `assets/` | CSS, fonts and cached aggregated data (auto-served by Dash) |
