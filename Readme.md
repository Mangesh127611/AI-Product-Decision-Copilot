# AI Product Decision Copilot

A product analytics dashboard built with Python, Streamlit, and Pandas to help product teams prioritize features, analyze customer feedback, and identify improvement opportunities.

## Overview

Product teams receive feature requests and customer feedback every day. Choosing what to build next can be challenging when engineering time and resources are limited.

AI Product Decision Copilot helps organize this information into a simple dashboard for better product decision-making.

**Note:** This version uses rule-based analysis and sample data. It does not use an external AI model or API.

## Features

- **Feature Prioritization:** Score features based on impact, confidence, strategic fit, and effort.
- **Customer Feedback Analysis:** Categorize customer feedback using keyword-based rules.
- **Opportunity Scoring:** Rank common customer problems using frequency and scoring assumptions.
- **Executive Dashboard:** Display key metrics and suggested next steps.
- **CSV Export:** Download analysis results.
- **Executive Summary:** Export a summary for product discussions.

## Tech Stack

- Python
- Streamlit
- Pandas

## Installation and Usage

### 1. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/AI-Product-Decision-Copilot.git
cd AI-Product-Decision-Copilot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The dashboard should open in your browser.

## How to Use

1. Review and score product features.
2. Upload customer feedback as a CSV file with a `Feedback` column, or use the sample data.
3. Explore feedback categories and product opportunities.
4. Review the executive dashboard.
5. Export results for further analysis.

## Limitations

- Feedback categorization is based on keywords, not a machine learning model.
- Opportunity scores use illustrative assumptions and should be validated with real data.
- Sample data does not represent measured business results.

## Future Improvements

- Semantic customer feedback analysis.
- Integration with real product analytics data.
- Customizable prioritization weights.
- Historical trend analysis.
- Improved recommendation and reporting capabilities.

## Project Goal

This project demonstrates practical skills in Python development, data analysis, interactive dashboard creation, and product prioritization.

**Built as a product analytics portfolio project.**