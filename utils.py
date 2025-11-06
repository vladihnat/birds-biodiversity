"""
Minimal helpers
- reading the three sheets from Excel and saving as CSVs
- minimal cleaning functions for ESPECES, GPS-MILIEU and NOM FRANÇAIS sheets
"""
from pathlib import Path
import pandas as pd

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

