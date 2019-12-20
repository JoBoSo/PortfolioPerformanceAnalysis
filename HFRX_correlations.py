from HFRX_Data_Cleaning import nav
import pandas as pd
import numpy as np

portfolio = pd.read_excel('Input - Daily NAV.xlsx')
portfolio = portfolio[['DATE', 'Portfolio']]

data = pd.merge(portfolio, nav, how = 'outer', left_on = 'DATE', right_on = 'Date')

consolidated_dates = []
for i, row in data.iterrows():
    if pd.isna(row['Date']):
        consolidated_dates += [row['DATE']]
    else:
        consolidated_dates += [row['Date']]
        
data['DATE'] = consolidated_dates
data = data.drop(columns='Date')

corr = data.corr()['Portfolio']
corr = corr.to_frame()
corr = corr.drop(['DATE', 'Portfolio'], axis=0)
corr.index.name = 'Index'
corr.columns = ['Correlation']
corr = corr.sort_values(by = 'Correlation', ascending = False)
corr.to_excel('Output - HFRX Correlations.xlsx')