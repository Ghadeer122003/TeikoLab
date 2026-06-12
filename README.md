# 🧬 TeikoLab

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Built for Bob Loblaw at Loblaw Bio to analyze immune cell data from an ongoing clinical trial for his drug candidate miraclib.

## Overview

Bob Loblaw is a drug developer at Loblaw Bio running a clinical trial for his drug candidate miraclib on melanoma patients. He needed a way to analyze how the drug affects immune cell populations across patients who respond to treatment versus those who don't.

This platform takes raw cytometry data from the trial, loads it into a structured SQLite database, runs statistical analysis to find patterns, and displays everything in an interactive dashboard Bob can explore directly. 

The analysis found that cd4_t_cell frequencies are significantly different between responders and non-responders (p = 0.0133, Mann-Whitney U test), making it a potential biomarker for predicting miraclib response in melanoma patients.

## File Structure

```
TeikoLab/
├── load_data.py       # initializes the SQLite database & loads cell-count.csv 
├── summary.py         # computes the relative frequency of each cell population per sample
├── stat_analysis.py   # compares responders vs. non-responders & runs the stats test
├── subset.py          # queries the database for baseline melanoma miraclib PBMC samples
├── dashboard.py       # the interactive dashboard Bob uses to explore the data
├── cell-count.csv     # the raw clinical trial data
├── cell-count.db      # the SQLite database built from cell-count.csv
├── boxplot.png        # the boxplot saved from the statistical analysis
├── requirements.txt   # all the Python packages needed to run this project
├── Makefile           # three commands to set up, run, & launch the dashboard
└── README.md          # this file (you are here!)
```

## How to Run

...

## Schema

...

## Dashboard

...