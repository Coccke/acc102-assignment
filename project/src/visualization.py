from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(style="whitegrid", palette="Set2")


def _prepare_figure_dir(figures_dir: str | Path) -> Path:
    path = Path(figures_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def plot_sustainability_scores(merged_df, figures_dir: str | Path) -> None:
    output_dir = _prepare_figure_dir(figures_dir)
    ordered = merged_df.sort_values("sustainability_score", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=ordered, x="sustainability_score", y="brand")
    plt.title("Sustainability Messaging Score by Brand")
    plt.xlabel("Sustainability score (keyword count / total words)")
    plt.ylabel("Brand")
    plt.tight_layout()
    plt.savefig(output_dir / "sustainability_score_bar.png", dpi=300)
    plt.close()


def plot_controversy_counts(merged_df, figures_dir: str | Path) -> None:
    output_dir = _prepare_figure_dir(figures_dir)
    ordered = merged_df.sort_values("controversy_news_count", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=ordered, x="controversy_news_count", y="brand")
    plt.title("Environmental Controversy Proxy Count by Brand")
    plt.xlabel("Curated controversy news count")
    plt.ylabel("Brand")
    plt.tight_layout()
    plt.savefig(output_dir / "controversy_count_bar.png", dpi=300)
    plt.close()


def plot_scatter(merged_df, figures_dir: str | Path) -> None:
    output_dir = _prepare_figure_dir(figures_dir)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=merged_df,
        x="sustainability_score",
        y="controversy_news_count",
        hue="brand",
        s=140,
    )
    for _, row in merged_df.iterrows():
        plt.text(
            row["sustainability_score"] + 0.001,
            row["controversy_news_count"] + 0.2,
            row["brand"],
            fontsize=9,
        )
    plt.title("Sustainability Messaging vs Controversy Proxy")
    plt.xlabel("Sustainability score")
    plt.ylabel("Curated controversy news count")
    plt.tight_layout()
    plt.savefig(output_dir / "scatter_messaging_vs_controversy.png", dpi=300)
    plt.close()


def plot_gap_scores(merged_df, figures_dir: str | Path) -> None:
    output_dir = _prepare_figure_dir(figures_dir)
    ordered = merged_df.sort_values("gap_score", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=ordered, x="gap_score", y="brand")
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Gap Score Ranking")
    plt.xlabel("Gap score (normalized messaging - normalized controversy)")
    plt.ylabel("Brand")
    plt.tight_layout()
    plt.savefig(output_dir / "gap_score_ranking.png", dpi=300)
    plt.close()


def generate_all_figures(merged_df, figures_dir: str | Path = "figures") -> None:
    plot_sustainability_scores(merged_df, figures_dir)
    plot_controversy_counts(merged_df, figures_dir)
    plot_scatter(merged_df, figures_dir)
    plot_gap_scores(merged_df, figures_dir)
