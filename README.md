# Project: Bird-biodiversity 
LEIVA Martin (22205863), PEÑA CASTAÑO Javier (22203616), HERRERA NATIVI Vladimir (22205706)

Quantifying how biodiversity indicators of birds population evolved over time, with statistical uncertainty assessments and species-specific narratives from a birds monitoring dataset.

---

## Repository structure

```
Project Bird-biodiversity/
├─ README.md                         # You are here
├─ main.ipynb                        # Entry-point notebook (repro pipeline) — TBD
├─ utils.py                          # Reusable helpers for I/O, cleaning, metrics — TBD
├─ technical_report.ipynb            # Methods and helpers for main.ipynb
├─ data/
│  ├─ raw/                           # Original workbook (read-only)
│  ├─ filtered/                      # 3 partitions of Original woorbook 
│  └─ cleaned/                       # Cleaned partitions
├─ requirements.txt                  # File for environmment reproduction
└─ figures/                          # Plots supporting findings (PNG)
```

---

## Objectives

* Compute biodiversity indicators over time (e.g., species richness, Shannon, evenness, occupancy/abundance indices).
* Provide principled uncertainty (e.g., bootstrap CIs).
* Surface species-specific stories (trends, changepoints, habitat associations, detectability patterns).

---

## Environment & tooling

> See requirements.txt

Create environment (example with conda):

```bash
conda create -n birds-bio python=3.11.0
conda activate birds-bio
pip install -r requirements.txt  
```

---

## Reproduction: quick start

1. **Place the raw workbook** (read-only) at: `data/raw/<Observations-2012-2025.xlsx>`.

2. **Create needed repositories in root** : `data/filtered` ,  `data/cleaned`,  `figures/`

3. **Launch Jupyter** and open `main.ipynb`:
   
   ```bash
   jupyter lab  # or: code . (for vscode) 
   ```
4. **Set ```first_execution``` to ```True```**

5.  **Run all cells** in `main.ipynb`.

   * The notebook will:
     * load and validate schemas (`utils.py`),
     * produce filtered/cleaned datasets into `data/filtered/` or `data/cleaned/`,
     * compute biodiversity indicators + uncertainty estimates,
    
6. **Read the write-up** in `technical_report.ipynb` (the .md version does not display the mathematical formulas)

---

## Indicators & analysis plan (high level)

* **Richness & diversity**: annual species counts; Shannon/Simpson
* **Abundance indices**: normalised counts, site-level occupancy.
* **Uncertainty**: usage of bootstraping.
* 
Outputs land in:

* `figures/`: exploratory plots
  
---

## Entry points

* `main.ipynb`: Constitutes the end-to-end workflow (EDA -> indicators -> uncertainty). Includes a top-level **Parameters** cell for paths and toggles.
* `utils.py`: helpers for:

  * cleaning & validation,
  * indicator computation & bootstraps,
  * plotting.

---

## Citations & attribution

* Dataset: "Martinique Breeding Bird Monitoring, 2012–2025".
* Course: Applied Statistics M1

