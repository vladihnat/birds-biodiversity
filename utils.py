"""
Minimal helpers
- reading the three sheets from Excel and saving as CSVs
- minimal cleaning functions for ESPECES, GPS-MILIEU and NOM FRANÇAIS (TBD) sheets
"""
from pathlib import Path
import pandas as pd

# Fixed dict: sheet name -> output CSV filename
SHEETS_TO_CSV = {
    "ESPECES": "especes.csv",
    "GPS-MILIEU": "gps_milieu.csv",
    "NOM FRANÇAIS": "observations.csv",
}


def split_excel_to_csvs(xlsx_path: str | Path, out_dir: str | Path) -> dict:
    """
    Read the three sheets and save them as CSV files in out_dir.
    If out_dir does not exist, it is created.
    Returns a dict of sheet name -> written file path.
    """
    xlsx_path = Path(xlsx_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = {}
    for sheet, filename in SHEETS_TO_CSV.items():
        df = pd.read_excel(xlsx_path, sheet_name=sheet)
        out_path = out_dir / filename
        df.to_csv(out_path, index=False)
        written[sheet] = str(out_path)
    return written


def load_csvs(in_dir: str | Path) -> dict:
    """Load the three CSVs from in_dir and return a dict sheet name -> DataFrame."""
    in_dir = Path(in_dir)
    frames = {}
    for sheet, filename in SHEETS_TO_CSV.items():
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
    return tmp


def save_clean_csvs(dfs: dict, out_dir: str | Path) -> dict:
    """
    Save provided cleaned DataFrames to CSV.

    Expected keys in `dfs` (if present): 'ESPECES', 'GPS-MILIEU'.
    Writes files `especes_clean.csv` and `gps_milieu_clean.csv`.
    Returns a mapping logical_name -> written path.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written: dict[str, str] = {}
    if "ESPECES" in dfs:
        p = out_dir / "especes_clean.csv"
        dfs["ESPECES"].to_csv(p, index=False)
        written["especes_clean"] = str(p)
    if "GPS-MILIEU" in dfs:
        p = out_dir / "gps_milieu_clean.csv"
        dfs["GPS-MILIEU"].to_csv(p, index=False)
        written["gps_milieu_clean"] = str(p)
    return written

