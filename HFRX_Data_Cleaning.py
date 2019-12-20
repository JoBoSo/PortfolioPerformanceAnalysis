# Method:
# 1. Seperate the master df into dfs contatining index specific data
# 2. Merge all index specific dfs on common date so each index has its own NAV
#    and Change cols
# 3. Finally, create two dfs, one storing NAVs and the other storing changes.

# Motivation: to convert HRFX index data into a form that is comparable with
#             my portfolio data. I want to use this to find the index that 
#             has the highest correlation with my portfolio and to compute
#             performance and risk metrics.

# Visual:
#
# DataFrame: nav
# Date      HFRXAR  HFRXEHV  HFRXEW  ...
# 20191030  NAV1    NAV2     NAV3    ...
# 20191029  NAV4    NAV5     NAV6    ...
#
# DataFrame: change
# Date      HFRXAR  HFRXEHV  HFRXEW  ...
# 20191030  change1 change2  change3 ...
# 20191029  change4 change5  change6 ...

import pandas as pd
import numpy as np
import math
from functools import reduce

data = pd.read_excel("HFRX Data.xlsx")

# Get the set of indicies
indicies = set(data['Ticker'].values)

# Seperate data by index.
# Name the seperated DataFrames according to their unique ticker stored in 
#   indicies.
# Drop 'Index' and 'Ticker', since they are irrelevant now.
# Format col headers as Ticker NAV and Ticker Change
# Store dfs in a list, so we can merge all dfs in that list
index_dfs = []
for index in indicies:
    locals()[index] = data.loc[data['Ticker'] == index]
    locals()[index] = locals()[index].drop(columns = ['Index', 'Ticker'])
    locals()[index] = locals()[index].rename(columns={'Change': '{} Change'.format(index), 'NAV': '{} NAV'.format(index)})
    index_dfs += [locals()[index]]
    
# Merge seperated indicies on 'Date'
# Now, each index will have its own Change and NAV column
all_one = reduce(lambda left, right: pd.merge(left, right, on=['Date'],
                                              how='outer'), index_dfs)

# Seperate all_one into two datasets. One stores NAVs, the other stores Changes.
# Cols are now simply the ticker name, since one dataset is entirely dedicated
#   to NAV and the other to change
all_cols = all_one.columns
nav_cols = ['Date']
change_cols = ['Date']
for col in all_cols:
    if col[-3:] == 'NAV':
        nav_cols += [col]
    elif col[-6:] == 'Change':
        change_cols += [col]

nav = all_one[nav_cols]
change = all_one[change_cols]

nav = nav.rename(columns = lambda name: name[:-4] if name[-3:] == 'NAV' else name)
change = change.rename(columns = lambda name: name[:-7] if name[-6:] == 'Change' else name)