"""
Minimal helpers
- reading the three sheets from Excel and saving as CSVs
- minimal cleaning functions for ESPECES, GPS-MILIEU and NOM FRANÇAIS sheets
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.proportion import proportion_confint

# ------------------------
# Reading / writing helpers
# ------------------------
def split_excel_to_csvs(xlsx_path: str | Path, out_dir: str | Path, sheet_dict: dict) -> dict:
    """
    Read the three sheets and save them as CSV files in out_dir.
    If out_dir does not exist, it is created.
    Returns a dict of sheet name -> written file path.
    """
    xlsx_path = Path(xlsx_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = {}
    for sheet, filename in sheet_dict.items():
        df = pd.read_excel(xlsx_path, sheet_name=sheet)
        out_path = out_dir / filename
        df.to_csv(out_path, index=False)
        written[sheet] = str(out_path)
    return written


def load_csvs(in_dir: str | Path, sheet_dict: dict) -> dict:
    """Load the three CSVs from in_dir and return a dict sheet name -> DataFrame."""
    in_dir = Path(in_dir)
    frames = {}
    for sheet, filename in sheet_dict.items():
        path = in_dir / filename
        frames[sheet] = pd.read_csv(path, low_memory=False)
    return frames


# ------------------------
# Minimal cleaners (DataFrame in → DataFrame out)
# ------------------------

def clean_especes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean ESPECES sheet passed as a DataFrame.

    - First two columns are filled with (NaN) and must be dropped.
    - The *first row* is *data*, but was mistakenly used as header when reading.
    - Keep the first 3 meaningful columns and rename to
      [ESPECIES_NAME, LATIN_NAME, NATURE].
    """
    # Drop first two empty columns
    tmp = df.iloc[:, 2:].copy()

    # Recover the data that was used as headers during read
    header_as_row = pd.DataFrame([list(tmp.columns)], columns=tmp.columns)
    tmp = pd.concat([header_as_row, tmp], ignore_index=True)

    # Keep only the first 3 columns and rename
    tmp = tmp.iloc[:, :3].copy()
    tmp.columns = ["ESPECIES_NAME", "LATIN_NAME", "NATURE"]

    # Fill NaNs ""
    last_col = "NATURE"
    tmp[last_col] = tmp[last_col].fillna("")

    return tmp


def clean_gps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean GPS-MILIEU sheet passed as a DataFrame.

    - First two columns are filled with (NaN) and must be dropped.
    - Row 0 is NaN 'header filler'; row 1 contains the actual titles.
    - Keep 6 columns in this order and rename accordingly:
      [TRANSECT_NAME, COORDINATE_X, COORDINATE_Y, HABITAT_TYPE, TRANSECT_ID, POINT_ID].
    """
    # Drop first two empty columns
    tmp = df.iloc[:, 2:].copy()

    # Ensure we have at least 6 columns, then select and rename
    tmp = tmp.iloc[:, :6].copy()
    tmp.columns = [
        "TRANSECT_NAME",
        "COORDINATE_X",
        "COORDINATE_Y",
        "HABITAT_TYPE",
        "TRANSECT_ID",
        "POINT_ID",
    ]
    # Drop first row (RID 0), then reset index
    tmp = tmp.iloc[1:].reset_index(drop=True)
    return tmp


def clean_observations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean NOM FRANÇAIS
    - Columns 0..11 are fine.
    - Columns 12..25 must be renamed to the specified headers.
    - Drop the first two rows (RID 0 and RID 1) after fixing headers.
    - Fill NaNs with 0.0 for all columns *except* the last column (COMPANIED),
      which should be filled with the empty string "".
    """
    tmp = df.copy()
    tmp = tmp.rename(columns={"1er, 2e ou 3e passage": "N° passage"})

    # Replace headers for columns 12..25
    right_headers = [
        "AL25",
        "VL25",
        "AL50",
        "VL50",
        "AL100",
        "VL100",
        "AG100",
        "VG100",
        "VOL",
        "TOT_A",
        "TOT_V_sV",
        "TOT_AV_sV",
        "TOT_AV_V",
        "COMPANIED",
    ]
    new_cols = list(tmp.columns)
    new_cols[12:26] = right_headers
    tmp.columns = new_cols

    # Drop first two rows (RID 0 and 1), then reset index
    tmp = tmp.iloc[2:].reset_index(drop=True)

    # Fill NaNs: all except last column -> 0.0; last column (COMPANIED) -> ""
    last_col = "COMPANIED"
    numeric_like_cols = [
        "N° passage","nuages","pluie","vent","visibilité","N° point",
        "AL25","VL25",
        "AL50","VL50",
        "AL100","VL100",
        "AG100","VG100",
        "VOL",
        "TOT_A","TOT_V_sV","TOT_AV_sV","TOT_AV_V",
    ]
    tmp[numeric_like_cols] = tmp[numeric_like_cols].fillna(0)
    tmp[last_col] = tmp[last_col].fillna("")

    tmp[numeric_like_cols] = tmp[numeric_like_cols].apply(lambda col: pd.to_numeric(col, errors="coerce"))
    tmp[numeric_like_cols] = tmp[numeric_like_cols].fillna(0)
    tmp[numeric_like_cols] = tmp[numeric_like_cols].astype(int)

    return tmp

def save_clean_csvs(dfs: dict, out_dir: str | Path) -> dict:
    """
    Save provided cleaned DataFrames to CSV.

    Expected keys in `dfs` (if present): 'ESPECES', 'GPS-MILIEU'.
    Writes files `especes_clean.csv` and `gps_milieu_clean.csv`.
    Returns a dict "logical_name" -> "written path".
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = {}
    if "ESPECES" in dfs:
        p = out_dir / "especes_clean.csv"
        dfs["ESPECES"].to_csv(p, index=False)
        written["especes_clean"] = str(p)
    if "GPS-MILIEU" in dfs:
        p = out_dir / "gps_milieu_clean.csv"
        dfs["GPS-MILIEU"].to_csv(p, index=False)
        written["gps_milieu_clean"] = str(p)

    if "NOM FRANÇAIS" in dfs:
        p = out_dir / "nom_francais_clean.csv"
        dfs["NOM FRANÇAIS"].to_csv(p, index=False)
        written["nom_francais_clean"] = str(p)
    return written


# Helper functions:

# Diversity functions: 
def shannon_index(counts):
    """
    Compute the Shannon diversity index.

    Parameters:  counts (array-like): Species counts or abundances.

    Returns: float: Shannon diversity index (H).
    """
    p = counts / counts.sum()
    return -np.sum(p * np.log(p + 1e-12))

def simpson_index(counts):
    """
    Compute the Simpson diversity index.

    Parameters:counts (array-like): Species counts or abundances.

    Returns:float: Simpson diversity index (1 - D).
    """
    p = counts / counts.sum()
    return 1 - np.sum(p**2)


# Plot functions: 
def plot_indicator_with_ci(df, indicator, color, ylabel):
    """
    Plot annual values of an indicator with its 95% confidence interval.

    Parameters:
        df (DataFrame): Data containing 'year', indicator, and CI columns.
        indicator (str): Name of the indicator column.
        color (str): Color for the line and CI band.
        ylabel (str): Label for the y-axis.
    """
    plt.figure(figsize=(9, 5))
    plt.plot(df["year"], df[indicator], color=color, marker="o", label=indicator)
    plt.fill_between(df["year"], df[f"{indicator}_low"], df[f"{indicator}_high"], 
                     color=color, alpha=0.2, label="95% CI")
    plt.title(f"Annual trend: {indicator}")
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_trend_with_stats(df, indicator, color="tab:blue"):
    """
    Fits a linear trend for the given indicator and plots:
    - Observed annual values
    - Regression line
    - Confidence interval band
    - Annotates slope and p-value
    """
    X = sm.add_constant(df["year"])
    y = df[indicator]
    model = sm.OLS(y, X).fit()

    slope = model.params["year"]
    p_value = model.pvalues["year"]
    r2 = model.rsquared

    # Predictions with confidence intervals
    pred = model.get_prediction(X)
    pred_summary = pred.summary_frame(alpha=0.05)

    # Plot
    plt.figure(figsize=(9, 5))
    plt.plot(df["year"], y, "o", color=color, label="Observed values", alpha=0.7)
    plt.plot(df["year"], pred_summary["mean"], "r-", label="Linear trend")
    plt.fill_between(
        df["year"],
        pred_summary["mean_ci_lower"],
        pred_summary["mean_ci_upper"],
        color="r", alpha=0.2, label="95% CI (model)"
    )
    plt.title(f"Trend in {indicator} (2014-2025)")
    plt.xlabel("Year")
    plt.ylabel(indicator)
    plt.legend(loc="best")
    
    # Annotate slope and p-value
    plt.text(
        0.02, 0.98,
        f"Slope = {slope:.4f}\n"
        f"p-value = {p_value:.3f}\n"
        f"R² = {r2:.3f}",
        transform=plt.gca().transAxes,
        va="top", ha="left",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7)
    )
    plt.tight_layout()
    plt.show()
    
    return model

def plot_transect_panels_with_ci(det_tr_yr, species, n_tr=6):
    """
    Plot detection rate trends with 95% Wilson CIs across multiple transects.

    Parameters:
        det_tr_yr (DataFrame): Detection data per transect and year.
        species (str): Species name to filter.
        n_tr (int): Number of top transects to plot by visit count.
    """

    d_sp = det_tr_yr[det_tr_yr["ESPECE"] == species]
    trs = (d_sp.groupby("Nom transect")["N_visits_tr_year"].sum()
                .sort_values(ascending=False).head(n_tr).index)
    n = len(trs); ncols = 3; nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3*nrows), sharex=True, sharey=True)
    axes = axes.ravel()
    for i, tr in enumerate(trs):
        dd = d_sp[d_sp["Nom transect"] == tr].sort_values("year").copy()
        dd = dd[(dd["N_visits_tr_year"] > 0) & dd["det_rate"].notna()]
        if len(dd) == 0:
            axes[i].set_title(tr + " (no data)"); axes[i].axis("off"); continue
        lohi = dd.apply(lambda r: wilson_ci(r["K_detects"], r["N_visits_tr_year"]), axis=1)
        dd["det_low"], dd["det_high"] = zip(*lohi)
        dd["det_low"] = np.minimum(dd["det_low"].clip(0,1), dd["det_rate"])
        dd["det_high"] = np.maximum(dd["det_high"].clip(0,1), dd["det_rate"])
        yerr_lower = np.clip(np.nan_to_num(dd["det_rate"] - dd["det_low"], nan=0.0), 0, None)
        yerr_upper = np.clip(np.nan_to_num(dd["det_high"] - dd["det_rate"], nan=0.0), 0, None)
        yerr = np.vstack([yerr_lower, yerr_upper])

        axes[i].errorbar(dd["year"], dd["det_rate"], yerr=yerr, fmt="o-", capsize=3)
        axes[i].set_title(tr); axes[i].set_xlabel("Year"); axes[i].set_ylabel("Detection rate")
    for j in range(i+1, len(axes)): axes[j].axis("off")
    fig.suptitle(f"{species} — detection rate per transect (95% CIs)")
    plt.ylim(0, 1); plt.tight_layout(); plt.show()



def plot_transect_with_model(det_tr_yr, species, transect):
    """
    Plot detection rates and logistic trend model for one transect.

    Parameters:
        det_tr_yr (DataFrame): Detection data by species/transect/year.
        species (str): Target species name.
        transect (str): Transect name to plot.
    """
    d = det_tr_yr[(det_tr_yr["ESPECE"] == species) & (det_tr_yr["Nom transect"] == transect)].sort_values("year")
    res, fitted = fit_logistic_trend_per_transect_2(d)
    if res is None:
        print(f"{species} — {transect}: not enough data"); return
    slope = res.params.get("year", np.nan); pval = res.pvalues.get("year", np.nan)

    plt.figure(figsize=(8,5))
    # observed + Wilson CI
    plt.errorbar(d["year"], d["det_rate"],
                 yerr=[d["det_rate"]-d["det_low"], d["det_high"]-d["det_rate"]],
                 fmt="o", capsize=3, label="Observed (95% binomial CI)")
    # fitted line + model CI
    plt.plot(fitted["year"], fitted["fit"], "r-", label="Logistic trend")
    plt.fill_between(fitted["year"], fitted["fit_low"], fitted["fit_high"], color="r", alpha=0.2,
                     label="95% CI (model)")
    plt.title(f"{species} — {transect}\nTrend slope={slope:.4f}, p={pval:.3f}")
    plt.xlabel("Year"); plt.ylabel("Detection rate"); plt.legend(); plt.tight_layout(); plt.show()


#  Bootstrap functions: 
def bootstrap_diversity(df_year, n_boot=1000, seed=42):
    """
    Bootstrap estimates of diversity indices (Shannon, Simpson, Richness).

    Parameters:
        df_year (DataFrame): Data with species counts ('TOT_AV_sV').
        n_boot (int): Number of bootstrap samples.
        seed (int): Random seed.

    Returns: DataFrame: Mean and 95% CI for each diversity index.
    """
    rng = np.random.default_rng(seed)
    results = []
    counts = df_year["TOT_AV_sV"].values
    for _ in range(n_boot):
        sample = rng.choice(counts, size=len(counts), replace=True)
        results.append({
            "Shannon": shannon_index(sample),
            "Simpson": simpson_index(sample),
            "Richness": np.sum(sample > 0)
        })
    boot_df = pd.DataFrame(results)
    ci = boot_df.quantile([0.025, 0.975]).T  # 95% CI
    mean = boot_df.mean()
    out = mean.to_frame("mean").join(ci)
    out.columns = ["mean", "ci_low", "ci_high"]
    return out

def bootstrap_ci(data, func=np.mean, B=1000, alpha=0.05):
    """
    Compute bootstrap confidence interval for a given statistic (func).
    
    Parameters:
        data (array-like): Input data.
        func (callable): Statistic to bootstrap (default: np.mean).
        B (int): Number of bootstrap resamples.
        alpha (float): Significance level for CI (default 0.05).

    Returns: tuple: (estimate, ci_low, ci_high)
    """
    n = len(data)
    if n == 0:
        return np.nan, np.nan, np.nan  # handle empty groups
    
    # Original estimate
    theta_hat = func(data)
    
    # Bootstrap resamples
    boot_estimates = []
    for _ in range(B):
        sample = np.random.choice(data, size=n, replace=True)
        boot_estimates.append(func(sample))
    boot_estimates = np.array(boot_estimates)
    
    # Quantiles of bootstrap distribution
    q_low = np.quantile(boot_estimates, alpha / 2)
    q_high = np.quantile(boot_estimates, 1 - alpha / 2)
    
    # Reflected confidence interval (percentile method)
    ci_low = 2 * theta_hat - q_high
    ci_high = 2 * theta_hat - q_low
    
    return theta_hat, ci_low, ci_high

# Fit functions:
def fit_binom_glm(sub_df):
    """
    sub_df has columns: year, A_sum, T_sum
    Returns pred df, slope, pval 
    """
    df = sub_df.sort_values("year").copy()

    df["year_c"] = df["year"] - df["year"].mean()  
    y = (df["A_sum"] / df["T_sum"]).values
    X = sm.add_constant(df[["year_c"]])
    model = sm.GLM(y, X, family=sm.families.Binomial(), var_weights=df["T_sum"].values)
    res = model.fit(cov_type="HC1")

    pred = res.get_prediction(X)
    ci = pred.conf_int(alpha=0.05)
    df["pred"]   = pred.predicted_mean
    df["ci_low"] = ci[:, 0]
    df["ci_high"]= ci[:, 1]

    slope = float(res.params.get("year_c"))  
    pval  = float(res.pvalues.get("year_c"))
    return df, slope, pval


def fit_logistic_trend_per_transect_1(d):
    """
    d: slice of det_tr_yr for one species & one transect.
       Needs columns year, det_rate, N_visits_tr_year.
    Returns statsmodels result or None if insufficient data.
    """
    mask = (d["N_visits_tr_year"] > 0) & d["det_rate"].notna()
    d2 = d.loc[mask]
    if len(d2) < 3:
        return None
    X = sm.add_constant(d2["year"])
    # Binomial GLM on proportions with frequency weights = #visits
    res = sm.GLM(d2["det_rate"], X, family=sm.families.Binomial(), freq_weights=d2["N_visits_tr_year"]).fit()
    return res

def fit_logistic_trend_per_transect_2(d):
    """
    Fit logistic trend and return fitted values with 95% CI.

    Parameters: d (DataFrame)

    Returns:tuple: (result, fitted_df)
    """
    # keep rows with visits > 0
    d = d[(d["N_visits_tr_year"] > 0) & d["det_rate"].notna()]
    if len(d) < 3:
        return None, None
    X = sm.add_constant(d["year"])
    res = sm.GLM(d["det_rate"], X,
                 family=sm.families.Binomial(),
                 freq_weights=d["N_visits_tr_year"]).fit()
    pred = res.get_prediction(X)
    pred_df = pred.summary_frame()   # columns: mean, mean_ci_lower, mean_ci_upper (on response scale)
    out = d.copy()
    out["fit"] = pred_df["mean"].values
    out["fit_low"] = pred_df["mean_ci_lower"].values
    out["fit_high"] = pred_df["mean_ci_upper"].values
    return res, out



#Wilson function:
def wilson_ci(k, n, alpha=0.05):
    """
    Compute Wilson score confidence interval for a binomial proportion.

    Parameters:
        k (int): Number of successes.
        n (int): Number of trials.
        alpha (float): Significance level (default 0.05 for 95% CI).

    Returns: tuple: (lower_bound, upper_bound)
    """
    if (n is None) or (n == 0):
        return (np.nan, np.nan)
    z = 1.96  # 95% CI
    p = k / n
    denom = 1 + z**2/n
    center = (p + z**2/(2*n)) / denom
    half = z * np.sqrt((p*(1-p) + z**2/(4*n)) / n) / denom
    lo, hi = center - half, center + half
    # enforce [0,1] and monotonic relationship
    lo = max(0.0, min(lo, p))
    hi = min(1.0, max(hi, p))
    return lo, hi
