import re
from pathlib import Path

import numpy as np
import pandas as pd


SUSTAINABILITY_KEYWORDS = [
    "sustainable",
    "sustainability",
    "eco",
    "green",
    "recycled",
    "ethical",
    "carbon",
    "climate",
    "circular",
    "net zero",
]


def count_words(text: str) -> int:
    return len(re.findall(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", str(text)))


def count_keywords(text: str, keywords: list[str] | None = None) -> int:
    keywords = keywords or SUSTAINABILITY_KEYWORDS
    lowered = str(text).lower()
    total = 0
    for keyword in keywords:
        pattern = rf"\b{re.escape(keyword)}\b"
        total += len(re.findall(pattern, lowered))
    return total


def build_text_metrics(texts_df: pd.DataFrame, keywords: list[str] | None = None) -> pd.DataFrame:
    keywords = keywords or SUSTAINABILITY_KEYWORDS
    metrics = texts_df.copy()
    metrics["total_words"] = metrics["clean_text"].apply(count_words)
    metrics["sustainability_keyword_count"] = metrics["clean_text"].apply(
        lambda value: count_keywords(value, keywords)
    )

    brand_metrics = (
        metrics.groupby("brand", as_index=False)
        .agg(
            total_words=("total_words", "sum"),
            sustainability_keyword_count=("sustainability_keyword_count", "sum"),
            source_count=("source_url", "nunique"),
        )
        .sort_values("brand")
        .reset_index(drop=True)
    )

    brand_metrics["sustainability_score"] = (
        brand_metrics["sustainability_keyword_count"] / brand_metrics["total_words"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)
    return brand_metrics


def min_max_normalize(series: pd.Series) -> pd.Series:
    minimum = series.min()
    maximum = series.max()
    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - minimum) / (maximum - minimum)


def assign_quadrant(message_score: float, controversy_score: float) -> str:
    message_level = "High Messaging" if message_score >= 0.5 else "Low Messaging"
    controversy_level = "High Controversy" if controversy_score >= 0.5 else "Low Controversy"
    return f"{message_level} / {controversy_level}"


def build_merged_metrics(
    text_metrics_df: pd.DataFrame,
    controversy_summary_df: pd.DataFrame,
    brand_info_df: pd.DataFrame,
) -> pd.DataFrame:
    merged = text_metrics_df.merge(controversy_summary_df, on="brand", how="left")
    merged = merged.merge(brand_info_df, on="brand", how="left")

    merged["normalized_sustainability_score"] = min_max_normalize(merged["sustainability_score"])
    merged["normalized_controversy_score"] = min_max_normalize(merged["controversy_news_count"])
    merged["gap_score"] = (
        merged["normalized_sustainability_score"] - merged["normalized_controversy_score"]
    )
    merged["interpretation_label"] = merged.apply(
        lambda row: assign_quadrant(
            row["normalized_sustainability_score"], row["normalized_controversy_score"]
        ),
        axis=1,
    )
    merged = merged.sort_values("gap_score", ascending=False).reset_index(drop=True)
    return merged


def build_brand_rankings(merged_df: pd.DataFrame) -> pd.DataFrame:
    rankings = merged_df.copy()
    rankings.insert(0, "rank", rankings["gap_score"].rank(ascending=False, method="dense").astype(int))
    rankings = rankings.sort_values(["rank", "brand"]).reset_index(drop=True)
    return rankings
