# BankMind — Track A (Data Analyst)

**Author:** Abhinav Atul  
**Track:** A — Data Analyst  
**Live Demo:** 🚀 [https://bankmind-abhinavatul.streamlit.app/](https://bankmind-abhinavatul.streamlit.app/)

## Quick Start

### 1. Get the dataset
Download `bank-full.csv` from:  
👉 https://archive.ics.uci.edu/dataset/222/bank+marketing  
(Click "Download" → extract the zip → copy `bank-full.csv` into the `data/` folder)

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run EDA script (generates chart PNGs)
```bash
python analysis.py
```
Charts are saved to `assets/`.

### 4. Launch the Streamlit dashboard
```bash
streamlit run app.py
```
Opens at http://localhost:8501

## Project Structure
```
task/
├── data/
│   └── bank-full.csv       ← Download this (Ignored in Git)
├── assets/                 ← Auto-generated chart PNGs
├── analysis.py             ← EDA + 4 business questions
├── app.py                  ← Streamlit dashboard
├── EXPLANATION.md          ← Written explanation for submission
└── requirements.txt
```
