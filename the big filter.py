import pandas as pd
import yfinance as yf
import os

#PARAMETERS CONFIGURATION

MIN_ROE = 0.15
MAX_PE = 30
MAX_NET_DEBT_EBITDA = 3.0
MIN_CURRENT_RATIO = 0.8 #Consumer stocks usually have low current ratios therefore we'll lower it globally then sort it out manually with the stocks the program finds us
MIN_REV_GROWTH = 0.05
REQ_FCF_POS = True

#THE CANDIDATE LIST

print(f"Looking for the tickers file in: {os.getcwd()}")

tickers = []
print("Fetching the sp500 list from wikipedia...")
try:
    if  os.path.exists ("tickers.csv"):
        print("Found tickers.csv")
        df = pd.read_csv("tickers.csv") 
    else: 
        raise FileNotFoundError ("non trovo ne 'tickers.csv' ne 'tickers.xlsx' ")
                                 
    
    raw_tickers = df.iloc[:,0].astype(str).str.strip().str.upper().tolist()

    tickers = [t for t in raw_tickers if t != "NAN" and len(t) >0]

    print(f" LOADED {len(tickers)} companies from file")

except Exception as e:
      print(f"Error loading tickers: {e}")
      print("be sure to have a file named 'tickers.csv' or 'tickers.xlsx' in the current directory with a list of ticker symbols in the first column.")
      exit()


print("analyzing fundamentals this may take a while...")
print("-" *60)

screener_results = []


for ticker_symbol in tickers:
    try:
        ticker_symbol = ticker_symbol.replace(".", "-")
        stock=yf.Ticker(ticker_symbol)
        info=stock.info
        name=info.get("ShortName",ticker_symbol)
        price=info.get("currentPrice",None)
        sector = info.get("sector", "Unknown")
        roe=info.get("returnOnEquity",None)
        PE =info.get("trailingPE",None)
        debt_to_equity = info.get("debtToEquity", None)
        current_ratio = info.get("currentRatio", None)
        revenue_growth = info.get("revenueGrowth", None)
        fcf = info.get("freeCashflow", None)

        #NET DEBT/EBITDA
        total_debt = info.get("totalDebt", 0)
        total_cash= info.get("totalCash",0)
        ebitda = info.get("ebitda", 0)

        net_debt_ebitda = 999

        if ebitda and ebitda > 0:
            net_debt_ebitda = (total_debt - total_cash) / ebitda
        elif ebitda is None: 
            net_debt_ebitda = None    

           

        score = 0
        Missed= []    

        #The final judgment

        #Check ROE

        if roe is not None and roe >= MIN_ROE: score+=1
        else: Missed.append("Low ROE")

        #Check PE
        if PE is not None and PE <= MAX_PE: score +=1
        else:   Missed.append("High PEG (Too expensive)")

        #NET DEBT / EBITDA
        if net_debt_ebitda is not None and net_debt_ebitda <= MAX_NET_DEBT_EBITDA: score += 1
        else:    Missed.append("High Leverage")

        #Check Current Ratio
        if current_ratio is not None and current_ratio >= MIN_CURRENT_RATIO: score += 1
        else:    Missed.append("Low liquidity")
        
        #Check Revenue Growth
        if revenue_growth is not None and revenue_growth >= MIN_REV_GROWTH: score += 1
        else:    Missed.append("Low Revenue Growth")
        
        #Check FCF
        if fcf is  not None and fcf > 0: score += 1
        else:    Missed.append("Negative Free Cash Flow")


        #If it passed everything, we add it to the results
        if score >= 4:
            print(f"{ticker_symbol}PASSED!")
            screener_results.append({
                "Ticker": ticker_symbol,
                "Score": score,
                "Name": name,
                "Price ($)": price,
                "ROE (%)": round(roe * 100,2) if roe else 0,
                "P/E": round(PE, 1) if PE else None,
                "NetDebt/EBITDA": round(net_debt_ebitda,2) if (net_debt_ebitda is not None) else 99,
                "Current Ratio": current_ratio,
                "Revenue Growth": round(revenue_growth *100 ,2) if revenue_growth else 0,
                "Free Cash Flow": fcf
            })
        

    except Exception as e:
        pass


#THE FINAL RESULTS

print("-" *60)
if len(screener_results) >0:
    df_results = pd.DataFrame(screener_results)
    df_results = df_results.sort_values(by=["Score", "P/E"], ascending = [False, True])
    print(f"\n TOP PLAYERS ({len(df_results)}) out of {len(tickers)}")
    print(df_results.to_string(index=False))
    df_results.to_csv("Winners_screener.csv", index=False)
    print("---Results correctly save on Winners_screener.csv!---")

else:
    print("dang that was a total disaster!")

    

    
