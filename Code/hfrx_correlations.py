from hfrx_data_cleaning import nav
import pandas as pd
import numpy as np

portfolio = pd.read_excel('Input-Daily NAV.xlsx')
portfolio = portfolio[['Date', 'Portfolio']]

data = pd.merge(portfolio, nav, how = 'outer', on = 'Date')

corr = data.corr()['Portfolio']
corr = corr.to_frame()
corr = corr.drop(['Date', 'Portfolio'], axis=0)
corr.index.name = 'Index'
corr.columns = ['Correlation']
corr = corr.sort_values(by = 'Correlation', ascending = False)
corr.to_excel('Output-HFRX Correlations.xlsx')