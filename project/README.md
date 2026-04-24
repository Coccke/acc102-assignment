# Green Claims vs Environmental Controversies: A Data Analysis of Fast Fashion Brands

## 1. Project Title
This ACC102 Track 2 project investigates whether fast fashion brands with stronger sustainability messaging also face more environmental controversy signals.

## 2. Problem Statement
Fast fashion brands often publish sustainability claims, but users may still question whether those claims are aligned with wider environmental controversy indicators. This project uses a small curated dataset to compare official sustainability messaging with manually curated public controversy counts across six brands.

## 3. Target Users
- Consumers who want to judge whether sustainability claims appear trustworthy
- Investors who want to identify possible ESG reputation risk
- Media and NGOs who want a simple evidence base for further investigation

## 4. Business Relevance
The project has business relevance because sustainability communication affects brand image, customer trust, and investor perception. Comparing messaging with controversy signals can help users think more critically about possible disclosure–performance gaps.

## 5. Data Sources
The repository includes three raw datasets stored in `data/raw/`:
- `brand_sustainability_texts.csv`: curated sustainability messaging excerpts or summaries based on official corporate sustainability pages
- `brand_controversy_counts.csv`: manually curated environmental controversy proxy counts for 2022–2025
- `brand_info.csv`: basic context about each brand

The selected brands are Zara, H&M, Shein, Uniqlo, Primark, and Boohoo.

## 6. Data Construction Notes
This is a curated educational dataset assembled for a student analysis project.

- Sustainability messaging texts are short excerpts or concise summaries based on official corporate sustainability pages and are stored with source metadata and access dates.
- Controversy counts are not taken from a validated private database. They are manually curated public-signal proxy counts based on a documented search approach.
- The controversy variable should not be interpreted as proof of actual environmental harm or misconduct.
- The project is designed for transparency and reproducibility rather than exhaustive coverage.

## 7. Methodology
The notebook uses a simple and explainable Python workflow:
- Load raw CSV files with relative paths
- Clean brand names, dates, and text fields
- Apply a keyword-based sustainability text analysis
- Aggregate controversy counts by brand
- Merge both measures into a brand-level comparison table
- Construct normalized indicators and a `gap_score`
- Generate bar charts and a scatter plot to support interpretation

The sustainability keyword list includes terms such as `sustainable`, `sustainability`, `recycled`, `carbon`, `climate`, `circular`, and `net zero`.

## 8. Key Findings
Using the curated sample:
- Uniqlo, H&M, and Zara show relatively stronger sustainability messaging scores
- Shein and Boohoo show the highest controversy proxy counts
- Stronger messaging does not automatically imply lower controversy exposure
- Some brands may display a possible disclosure–performance gap, but the evidence is exploratory and should be interpreted cautiously

## 9. Repository Structure
```text
project_root/
├── README.md
├── requirements.txt
├── notebook.ipynb
├── reflection_report.md
├── demo_video_script.md
├── generate_outputs.py
├── data/
│   ├── raw/
│   │   ├── brand_sustainability_texts.csv
│   │   ├── brand_controversy_counts.csv
│   │   └── brand_info.csv
│   └── processed/
│       ├── text_metrics.csv
│       ├── merged_brand_metrics.csv
│       └── brand_rankings.csv
├── figures/
│   ├── sustainability_score_bar.png
│   ├── controversy_count_bar.png
│   ├── scatter_messaging_vs_controversy.png
│   └── gap_score_ranking.png
└── src/
    ├── data_prep.py
    ├── text_analysis.py
    └── visualization.py
```

## 10. How to Run
1. Clone or download the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Open `notebook.ipynb` in Jupyter.
4. Run the notebook from top to bottom.

Optional command-line workflow:
```bash
python generate_outputs.py
```

This regenerates the processed CSV files in `data/processed/` and the charts in `figures/`.

All paths in the project are relative paths.

## 11. Limitations
- Small sample of six brands
- Curated educational dataset rather than a full production dataset
- Proxy-based controversy measure
- Manual data construction and search decisions may affect results
- Messaging quantity does not equal actual sustainability performance
- Controversy counts depend on public visibility and search method

## 12. Demo Video
A short demo script is provided in `demo_video_script.md` for the required 1–3 minute presentation.

## 13. Course / Assignment Context
This repository was created for ACC102 Mini Assignment, Track 2: GitHub Data Analysis Project. The notebook is the main analytical workflow for marking, supported by Python modules, curated data files, and reproducible outputs.
