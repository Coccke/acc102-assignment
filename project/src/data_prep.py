from pathlib import Path
import re

import pandas as pd


BRAND_NAME_MAP = {
    "zara": "Zara",
    "h&m": "H&M",
    "hm": "H&M",
    "shein": "Shein",
    "uniqlo": "Uniqlo",
    "primark": "Primark",
    "boohoo": "Boohoo",
}


RAW_DATA_DIR = Path("data") / "raw"
PROCESSED_DATA_DIR = Path("data") / "processed"
FIGURES_DIR = Path("figures")


def ensure_output_dirs(base_dir: Path | None = None) -> None:
    project_dir = Path(base_dir) if base_dir else Path(".")
    (project_dir / PROCESSED_DATA_DIR).mkdir(parents=True, exist_ok=True)
    (project_dir / FIGURES_DIR).mkdir(parents=True, exist_ok=True)


def standardize_brand_name(value: str) -> str:
    if pd.isna(value):
        return value
    cleaned = str(value).strip()
    key = cleaned.lower()
    return BRAND_NAME_MAP.get(key, cleaned)


def clean_text(value: str) -> str:
    if pd.isna(value):
        return ""
    text = str(value).lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_raw_data(base_dir: Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    project_dir = Path(base_dir) if base_dir else Path(".")
    texts = pd.read_csv(project_dir / RAW_DATA_DIR / "brand_sustainability_texts.csv")
    controversies = pd.read_csv(project_dir / RAW_DATA_DIR / "brand_controversy_counts.csv")
    brand_info = pd.read_csv(project_dir / RAW_DATA_DIR / "brand_info.csv")
    return texts, controversies, brand_info


def clean_sustainability_texts(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["brand"] = cleaned["brand"].apply(standardize_brand_name)
    cleaned["year"] = pd.to_numeric(cleaned["year"], errors="coerce").astype("Int64")
    cleaned["access_date"] = pd.to_datetime(cleaned["access_date"], errors="coerce")
    cleaned["text"] = cleaned["text"].fillna("").astype(str).str.strip()
    cleaned["clean_text"] = cleaned["text"].apply(clean_text)
    cleaned = cleaned.drop_duplicates(subset=["brand", "year", "source_url", "text"]).reset_index(drop=True)
    return cleaned


def clean_controversy_counts(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["brand"] = cleaned["brand"].apply(standardize_brand_name)
    cleaned["year"] = pd.to_numeric(cleaned["year"], errors="coerce").astype("Int64")
    cleaned["controversy_news_count"] = pd.to_numeric(
        cleaned["controversy_news_count"], errors="coerce"
    ).fillna(0).astype(int)
    cleaned["access_date"] = pd.to_datetime(cleaned["access_date"], errors="coerce")
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    return cleaned


def clean_brand_info(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["brand"] = cleaned["brand"].apply(standardize_brand_name)
    cleaned = cleaned.drop_duplicates(subset=["brand"]).reset_index(drop=True)
    return cleaned


def aggregate_controversies(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("brand", as_index=False)
        .agg(
            controversy_news_count=("controversy_news_count", "sum"),
            first_year=("year", "min"),
            last_year=("year", "max"),
        )
        .sort_values("controversy_news_count", ascending=False)
        .reset_index(drop=True)
    )
    summary["period"] = summary["first_year"].astype(str) + "-" + summary["last_year"].astype(str)
    return summary


def save_dataframe(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
