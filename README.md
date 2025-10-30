# Project: Bird-biodiversity 
LEIVA Martin (n°etu), PEÑA CASTAÑO Javier (n°etu), HERRERA NATIVI Vladimir (22205706)

Quantifying how biodiversity indicators have evolved over time, with statistical uncertainty assessments and species-specific narratives from a birds monitoring dataset.

> **Status:** initial draft (README model). Replace all `TBD` blocks as the project matures.

---

## Repository structure

```
Project Bird-biodiversity/
├─ README.md                         # You are here
├─ main.ipynb                        # Entry-point notebook (repro pipeline) — TBD
├─ utils.py                          # Reusable helpers for I/O, cleaning, metrics — TBD
├─ technical_report.md               # Methods & results write-up (submission artifact) — TBD
├─ data/
│  ├─ raw/                           # Original workbook (read-only)
│  ├─ filtered/                      # 3 partitions of Original woorbook 
│  └─ cleaned/                       # Cleaned partitions
├─ figures/                          # Plots supporting findings (PNG/SVG/PDF)
└─ results/                          # Tables, metrics, model outputs
```

---

## Objectives (from assignment)

* Compute biodiversity indicators over time (e.g., species richness, Shannon, evenness, occupancy/abundance indices).
* Provide principled uncertainty (e.g., bootstrap CIs, Bayesian credible intervals, resampling across sites/years/observers).
* Surface species-specific stories (trends, changepoints, habitat associations, detectability patterns).

---

## Environment & tooling

> See requirements.txt — **link/location TBD**.

Create environment (example with conda):

```bash
conda create -n birds-bio python=TBD
conda activate birds-bio
pip install -r requirements.txt  
```

---

## Reproduction: quick start

1. **Place the raw workbook** (read-only) at: `data/raw/<Observations-2012-2025.xlsx>`.

2. **Launch Jupyter** and open `main.ipynb`:

   ```bash
   jupyter lab  # or: vscode 
   ```
3. **Run all cells** in `main.ipynb`.

   * The notebook will:

     * load and validate schemas (`utils.py`),
     * produce filtered/normalized datasets into `data/filtered/`,
     * compute biodiversity indicators + uncertainty estimates,
     * write tables to `results/` and figures to `figures/`.
4. **Read the write-up** in `technical_report.md` for methods & key results — **TBD**.

> For fully scripted runs (CI-friendly), add a `scripts/` or `make` target later — **TBD**.

---

## Data expectations & contracts

* **Read-only raw**: Never modify files in `data/raw/`. All transformations must write to `data/filtered/`.
* **Schema checks**: `utils.py` will host validators for column presence/types and referential joins across tabs — **TBD**.
* **Joins**:

  * `NOM FRANÇAIS` ↔ `ESPECES`: by species code/name (decide canonical key; document in `utils.py`) — **TBD**.
  * `NOM FRANÇAIS` ↔ `GPS-MILIEU`: by transect/point IDs — **TBD**.
* **Naming conventions** for derivatives (example):

  * `data/filtered/observations_clean.csv`
  * `data/filtered/species_lookup.csv`
  * `data/filtered/site_catalog.csv`

---

## Indicators & analysis plan (high level)

* **Richness & diversity**: annual species counts; Shannon/Simpson; rarefaction — **TBD** choices.
* **Abundance/occupancy indices**: effort-normalised counts; site-level occupancy with detection models — **TBD**.
* **Uncertainty**: stratified bootstrap (by site/year/observer) and/or Bayesian models — **TBD**.
* **Species stories**: per-species trend lines, changepoint detection, habitat associations — **TBD**.
* **Sensitivity & robustness**: cross-checks vs detection modality, observer effects, missingness — **TBD**.

Outputs land in:

* `figures/`: exploratory & publication-ready plots
* `results/`: tidy tables (CSV/Parquet) and model summaries (e.g., `.json`, `.txt`)

---

## Entry points

* `main.ipynb`: orchestrates the end-to-end workflow (EDA → indicators → uncertainty → export). Includes a top-level **Parameters** cell for paths and toggles — **TBD**.
* `utils.py`: helpers for:

  * file paths & I/O (Excel → tidy tables),
  * cleaning & validation,
  * indicator computation & bootstraps,
  * plotting wrappers (consistent styles & saving) — **TBD**.

---

## Runtime considerations

* **Excel I/O**: requires `openpyxl`; large workbooks may be slow the first time.
* **Memory/CPU**: `TBD` (record count, footprint, and typical runtime once profiled).
* **Randomness**: set global seeds in `main.ipynb` for reproducible bootstraps — **TBD**.
* **Locale/timezone**: timestamps are interpreted in `Europe/Paris` unless specified — **TBD**.

---

## Data documentation

* **Overview note**: short description of the 3 tabs and observation protocol — location **TBD**.
* **Data dictionary**: enumerate columns and types after first load — add to `results/` or `docs/` — **TBD**.

---

## Citations & attribution

* Dataset: "Martinique Breeding Bird Monitoring, 2012–2025" — **formal citation TBD**.
* Course: Applied Statistics M1 — **assignment link/location TBD**.

