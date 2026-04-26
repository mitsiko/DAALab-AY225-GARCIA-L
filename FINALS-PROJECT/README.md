
# Gaming & Mental Health — Data Analysis Report

A collaborative data science project analyzing the relationship between gaming habits and mental health indicators using a large-scale behavioral dataset.

---

## Project Overview

This project explores how daily gaming hours, stress levels, sleep patterns, and other lifestyle factors correlate with mental health outcomes such as depression, anxiety, and addiction. The analysis is performed on a **random sample of 10,000 respondents** drawn from a dataset of approximately **1,000,000 records** with **40 features**.

### Key Research Questions
- Is there a correlation between daily gaming hours and depression scores?
- How do stress levels distribute across the sampled population?
- Can we predict depression scores from gaming hours using linear regression?
- What percentage of respondents show signs of high stress or gaming addiction?

---

## Dataset

- **Source:** [Gaming and Mental Health Behavioral Dataset](https://www.kaggle.com/datasets/sharmajicoder/gaming-and-mental-health) on Kaggle
- **Original size:** ~1,000,000 rows × 40 columns
- **Analysis sample:** 10,000 randomly selected rows (uniform random sampling)
- **Key variables:** `daily_gaming_hours`, `depression_score`, `stress_level`, `sleep_hours`, `addiction_level`, `anxiety_score`, `social_interaction_score`, `loneliness_score`, `happiness_score`, and more

### Selected Features for Analysis
| Feature | Description | Range |
|---------|-------------|-------|
| `daily_gaming_hours` | Average daily time spent gaming | 0–24 hrs |
| `depression_score` | Self-reported depression level | 0–10 |
| `stress_level` | Self-reported stress level | 0–10 |
| `sleep_hours` | Average sleep per night | 0–12 hrs |
| `addiction_level` | Gaming addiction indicator | 0–10 |
| `anxiety_score` | Self-reported anxiety level | 0–10 |
| `age` | Respondent age | 18–65 |
| `gender` | Self-identified gender | Male / Female / Other |

---

## Project Structure
```
gaming-mental-health-analysis/
├── index.html # Main application (HTML + CSS + JavaScript)
├── README.md # This file
├── .gitignore # Git ignore rules
└── data/
└── gaming_mental_health_sampled.csv # Pre-sampled dataset (10,000 rows)
```
---

## How to Run


### Option 1: Local Development (Recommended)

### 1. Clone the repository
```
 git clone https://github.com/mitsiko/DAALab-AY225-GARCIA-L.git
```
### 2. Navigate into the project folder

```
 cd DAALab-AY225-GARCIA-L/FINALS-PROJECT
```
----------

### 3. Ensure dataset is in correct location

Make sure this file exists:
```
 FINALS-PROJECT/data/gaming_mental_health_sampled.csv
```
----------

### 4. Start a local server

#### Python (recommended)
```
 python -m http.server 8000
```
#### VS Code Live Server

- Right-click `index.html` → Open with Live Server

#### Node.js (optional)
 ```
  npx http-server -p  8000
```
----------

### 5. Open in browser
```
 http://localhost:8000
```
----------

### Option 2: GitHub Pages (Production)

This project is designed for static deployment using GitHub Pages.
### To access: https://mitsiko.github.io/DAALab-AY225-GARCIA-L/FINALS-PROJECT/
**Note:** GitHub Pages must be enabled on the `main` branch in the repository settings. The CSV file must also be present in the `main` branch.

----------

## 🛠️ Tech Stack

| Technology | Purpose | Loading Method |
|-----|-----|-----|
|**HTML5 + CSS3**| Structure and styling | — |
|**Vanilla JavaScript**| Application logic | — |
|**PapaParse 5.4.1**| CSV parsing | CDN |
|**Chart.js 4.4.1**| Data visualization | CDN |
|**Google Fonts**| Playfair Display + IBM Plex Mono | CDN |
|**GitHub Pages**| Deployment | Static hosting |

### Why Client-Side Only?

-   No backend required — runs entirely in the browser
-   No `npm install` or build steps needed
-   Works on any static hosting (GitHub Pages, Netlify, Vercel)
-   All data processing happens locally after CSV download

----------

## Features

### Section 1: Dataset Explorer (Account 1)

-   **CSV Loading:** Dynamic loading via PapaParse with progress indicator
    
-   **Data Cleaning:** Automatic removal of null/invalid rows, numeric type validation
    
-   **Random Sampling:** Uniform sampling to 10,000 rows for performance
    
-   **Paginated Table:** 50 rows per page with Previous/Next navigation
    
-   **Filtering:** Filter by gender (dropdown) and age range (min–max)
    
-   **Sorting:** Sort by 14 fields with separate ↑ Ascending and ↓ Descending buttons
    
-   **Summary Cards:** Mean gaming hours, mean depression, high stress rate, high addiction rate, mean sleep hours, mean stress level
    
-   **Integer Formatting:** Age, weekly sessions, years gaming, and stress level display without trailing decimals
    

### Section 2: Visualizations (Account 2)

-   **Bar Chart:** Top 10 respondents by daily gaming hours (horizontal)
    
-   **Scatter Plot:** Daily gaming hours vs depression score with regression line overlay
    
-   **Doughnut Chart:** Stress level distribution (Low 0–3, Medium 4–6, High 7–10)
    

### Section 3: Statistical Analysis (Account 2)

-   **Descriptive Statistics:** Sample size, mean, median, variance, standard deviation, min–max range
    
-   **Correlation Analysis:** Pearson r for gaming→depression and gaming→sleep, with strength/direction interpretation
    
-   **Linear Regression:** Gaming hours predicting depression score (equation, slope, intercept, R², interpretation)
    
-   **Narrative Insights:** Auto-generated data-driven summary with highlighted key findings
    
-   **Disclaimer:** Correlation does not imply causation
    

----------
## Important Notes


-   **Correlation ≠ Causation:** The relationships identified in this analysis are statistical associations, not proven causal effects. Many unmeasured confounding variables (e.g., pre-existing mental health conditions, socioeconomic factors) may influence both gaming behavior and mental health outcomes.
    
-   **Self-Reported Data:** The dataset is based on self-reported survey responses, which may be subject to recall bias and social desirability bias.
    
-   **Sample Limitation:** Analysis is performed on a random sample of 10,000 rows from a larger dataset. While statistically valid for exploratory analysis, results may not perfectly represent the full population.
    

----------

## License

This project is created for educational purposes as part of a Git collaboration exercise. The dataset is publicly available on Kaggle.

----------
## Contributors
-   **Account 1:** Lee Michiko Garcia — michikogarciasp@gmail.com
-   **Account 2:** Samuel Angelo Arnaiz — leumasolegnazianra@gmail.com
