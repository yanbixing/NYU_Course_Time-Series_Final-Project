Menglu Cao mc6685@nyu.edu
Jinze Chen jc8344@nyu.edu 
Wanying Xu wx523@nyu.edu

There are two datasets:

1. factors.pkl
 
* DP (Dividend-Price Ratio)
Download: http://www.multpl.com/
* PE (Price-to-Earnings Ratio)
Download: http://www.multpl.com/
* BM (Book-to-Market Ratio)
Download: http://www.multpl.com/
* CAPE (Cyclically Adjusted Price to Earnings Ratio)
Download: http://www.multpl.com/
* PCA-price
Formula: PCAprice=first component of PCA(DP, PE, BM, CAPE)
* DEF (Default Spread)
AAA: Quandl
Baa: Quandl
Formula: DEF = Baa Yield- Aaa Yield
* TERM (Term Spread)
10Y Yield https://fred.stlouisfed.org/series/DGS10Y
3Mon Yield https://fred.stlouisfed.org/series/DGS3MO
Formula: DEF = 10Y Yield- 3Mon Yield
* SIM (Sell in May and Go Away)
Formula: SIM = d/130
where d is the number of days in the next 130 business days that lie between the second business day in May and the 15th business day of October.
* VRP (Variance Risk Premium)
Formula:  VRP = VIX- volforecast(OHLCSPX)
* VIX: Yahoo Finance
OHLC daily SPX prices: Yahoo Finance
* IC (Implied Correlation)
Front Contract & Second Contract: quandl
Formula:  in report
* BDI (Baltic Dry Index)
Download: https://www.investing.com/indices/baltic-dry-historical-data
Formula:  BDI = Baltic Dry IndexBaltic Dry Index 3 month ago
* NOS (New Orders/ Shipments)
Download: https://www.census.gov/manufacturing/m3/index.html
* CPI (Consumer Price Index) 
CPI: quandl
Formula: CPI = percentage change in Consumer Price Index over the last twelve months
* PCR (Ratio of Stock Price to Commodity Price) 
GSCI: datastream
Formula:  in report
* MA (Moving Average)
Formula:  in report
* OIL (Oil Price Shocks)
Contract 1&4: quandl 
Formula:  in report
* SI (Short Interest)
Short Interest: quandl
Formula:  in report

The original paper also included two more factors CAY (Co-integration Residual of Consumption, Assets and Wealth) and PCA Tech (Principal Component of Technical Indicators indicator). Since we were not able to find open source data for these two factors, we decided to ignore them.


2. returns.pkl
* R_1M
SPX 1-month return (20 trading days)
* R_3M
SPX 3-month return (60 trading days)
* R_6M
SPX 6-month return (120 trading days)
* R_12M
SPX 12-month return (240 trading days)
* R_130d
SPX 130 day return (130 trading days)
