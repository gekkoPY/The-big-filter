# 🦁 The Big Filter - S&P 500 Value Screener

Welcome to **The Big Filter**!
This Python tool analyzes the S&P 500 companies fundamentally to find the best "Value" stocks hidden in the market. It uses a **Scoring System (0-6)** based on solid financial metrics (Buffett/Graham style).

## 🚀 How it Works
The script downloads real-time financial data from Yahoo Finance for 500+ companies and scores them based on:
1.  **ROE (Return on Equity):** > 15% (Profitability)
2.  **P/E Ratio:** < 30 (Valuation)
3.  **Net Debt/EBITDA:** < 3.0 (Financial Health)
4.  **Current Ratio:** > 0.8 (Liquidity)
5.  **Revenue Growth:** > 5% (Growth)
6.  **Free Cash Flow:** Must be Positive (Cash Generation)

## 📂 Project Structure
To run this tool, you need **both** files in the same folder:

* `the_big_filter.py`: The main script engine.
* `tickers.csv`: **REQUIRED.** Contains the list of S&P 500 tickers. The script *needs* this file to know what to analyze.

## 🛠️ Installation & Usage

1.  **Clone the repository** (or download the ZIP):
    ```bash
    git clone [https://github.com/TUO_USERNAME/The-Big-Filter.git](https://github.com/TUO_USERNAME/The-Big-Filter.git)
    ```
2.  **Install dependencies:**
    You need `pandas` and `yfinance`.
    ```bash
    pip install pandas yfinance openpyxl
    ```
3.  **Run the script:**
    Make sure you are in the project folder and `tickers.csv` is present.
    ```bash
    python the_big_filter.py
    ```

## 📊 Output
The script will print the process in the terminal and, at the end, it will generate a file named **`Winners_screener.csv`** (or `.xlsx`) containing the ranked list of the best companies found (The "Top Players").

## ⚠️ Disclaimer
This tool is for educational purposes only. Do not use this as your sole financial advice. Always do your own research (DYOR).

---
*Built with ❤️ and Python.*
