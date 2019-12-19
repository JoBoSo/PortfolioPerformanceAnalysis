# This program takes NAV data by day for a portfolio and benchmark indicies and 
# computes performance and risk metrics.

import pandas as pd
import numpy as np
import math



# the excel storing columns: date, portfolio NAV, benchmark NAV
returns = pd.read_excel("Input - Daily NAV.xlsx")



# the names of the columns storing daily NAV for the portfolio and benchmark
portfolio = 'Portfolio'
benchmark = 'HFRXEH'


# cleaning: set null values equal to last available value
# purpose: account for days exxchanges were not closed
# assumes first row has no null values

prev_port = None
prev_bench = None

for i, row in returns.iterrows():
    curr_port = row[portfolio]
    curr_bench = row[benchmark]

    if pd.isnull(curr_port):
        returns.at[i, portfolio] = prev_port
        
    if pd.isnull(curr_bench):
        returns.at[i, benchmark] = prev_bench
        
    prev_port = curr_port
    prev_bench = curr_bench 
        


# Add return column 
# return = 1 + change over last period

prev_port = None
prev_bench = None

for i, row in returns.iterrows():
    curr_port = row[portfolio]
    curr_bench = row[benchmark]
    
    if prev_port == None:
        returns.at[i, 'Portfolio Return'] = 1
        returns.at[i, 'Benchmark Return'] = 1
    
    else:
        def change(curr, prev):
            return 1 + ((curr - prev) / prev)

        return_port = change(curr_port, prev_port)
        return_bench = change(curr_bench, prev_bench)
        
        returns.at[i, 'Portfolio Return'] = return_port
        returns.at[i, 'Benchmark Return'] = return_bench
    
    prev_port = curr_port
    prev_bench = curr_bench


     
# Add alpha col
for i, row in returns.iterrows():
    alpha = row['Portfolio Return'] - row['Benchmark Return']
    returns.at[i, 'Alpha'] = alpha



# Add cumulative returns column

returns['Portfolio Cumulative Return'] = None
returns['Portfolio Cumulative Return'] = pd.to_numeric(returns['Portfolio Cumulative Return'])

prev = None
for i, row in returns.iterrows():
    curr = row['Portfolio Return']
    if prev == None:
        returns.at[i, 'Portfolio Cumulative Return'] = curr
        prev = curr
    else:
        cum = prev * curr
        returns.at[i, 'Portfolio Cumulative Return'] = cum
        prev = cum
        


returns['Benchmark Cumulative Return'] = None
returns['Benchmark Cumulative Return'] = pd.to_numeric(returns['Benchmark Cumulative Return'])

prev = None
for i, row in returns.iterrows():
    curr = row['Benchmark Return']
    if prev == None:
        returns.at[i, 'Benchmark Cumulative Return'] = curr
        prev = curr
    else:
        cum = prev * curr
        returns.at[i, 'Benchmark Cumulative Return'] = cum
        prev = cum



returns.to_excel('Output - Daily.xlsx')



# DataFrame containing monthly averages for data in returns

monthly = returns.copy()

monthly['DATE'] = monthly['DATE'].apply(lambda date: str(date)[0:4] + '-' + str(date)[4:6])

monthly = monthly.groupby(['DATE']).mean()

monthly.to_excel('Output - Monthly Average.xlsx')



# DataFrame containing annual returns

annual_returns = returns.copy()

annual_returns = annual_returns[['DATE', 'Portfolio Return', 'Benchmark Return']]

annual_returns['DATE'] = annual_returns['DATE'].apply(lambda date: str(date)[0:4])

annual_returns = annual_returns.groupby(['DATE']).prod() - 1

annual_returns.to_excel('Output - Annual Returns.xlsx')



def beta(data):
    cov = data.cov().at['Portfolio Return', 'Benchmark Return']
    var = data['Benchmark Return'].var()
    beta = cov / var
    return beta



# Portfolio metrics

beta = beta(returns)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

corr = returns.corr().at['Portfolio Return', 'Benchmark Return']

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
## annualized - nov 1, 2013 to dec 12 

years = 5 + (42 / 365)

periods = returns.shape[0]

periods_per_year = periods / years

stdev = returns.std()['Portfolio Return'] * math.sqrt(periods_per_year)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

risk_free = 0.01605

cum_return = returns.product()['Portfolio Return'] - 1

ann_return = (1 + cum_return) ** (periods_per_year / periods) - 1

sharpe = (ann_return - risk_free) / stdev

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

## cumultive alpha
alpha = returns.sum()['Alpha']

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

# Best month / worst month

'''
first_last = returns[['DATE', 'Portfolio Return']]

all_months = {}
curr_month = {}
prev_month = str(int((first_last.iloc[0]['DATE'])))[:-2]
for i, row in first_last.iterrows():
    date = str(int(row['DATE']))
    if date[:-2] == '01':
        curr_month.append({date: row[portfolio]})
    elif date[:-2]) != prev:
        curr_month.append({date: row[portfolio]})
    if len(curr_month) == 2:
        all_months += {date[:-2]: (curr_month[1].value - curr_month[0].value) / curr_month[0].value}
    prev = date[:-2]

best_month = max(all_months)
worst_month = min(all_months)
'''
        

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

# summary

summ = ({'Beta': [beta],
         'Cumulative Alpha': alpha,
         'Correlation': corr,
         'Standard Deviation': stdev,
         'Cumulative Return': cum_return,
         'Annualized Return': ann_return,
         'Sharpe Ratio': sharpe})

summary = pd.DataFrame(summ)

summary = summary.transpose()

summary.columns = [portfolio]

summary.to_excel('Output - Summary.xlsx')