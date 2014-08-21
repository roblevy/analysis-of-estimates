# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 16:18:53 2014

@author: rob
"""

import pandas as pd
import numpy as np
from rainbowplot import *
from scipy.stats import gaussian_kde

#%%
# Prepare the data
est_v_data = pd.read_csv('estimates_vs_data.csv',
                         true_values='t', false_values='f')

# Sum over multiple FD and investment values:
# -------------------------------------------
est_v_data.to_sector[est_v_data.is_final_demand] = 'Final Demand'
est_v_data.to_sector[est_v_data.is_investment] = 'Investment'
est_v_data.drop(['is_final_demand', 'is_investment'], axis=1, inplace=True)
est_v_data.set_index(
    [c for c in est_v_data.columns.tolist() if c != 'flow_amount'],
    inplace=True)
# Sum over duplicate index levels
est_v_data = est_v_data.groupby(level=est_v_data.index.names).sum()
# -------------------------------------------
# Drop estimates which don't have associated data points
est_v_data = est_v_data.unstack(level='is_estimate')
est_v_data = est_v_data.dropna()

#%%
# Get two separate series
#est = est_v_data.xs(True, level='is_estimate')
#data = est_v_data.xs(False, level='is_estimate')
logged = np.log(est_v_data[est_v_data >= 1])
#%%
# Plot
fig, ax = subplots()
#rainbow_scatter(ax, np.log(est), np.log(data))
group_scatter(ax, df=np.log(est_v_data[est_v_data >= 1]), 
              groupby_args={'level':'country_iso3'},
              legend_args={'ncol':3, 'loc':'lower right'})
ax.set_xlabel('WIOD data (log)')
ax.set_ylabel('Estimated data (log)')
fig.set_size_inches(17, 12)
fig.savefig('est_v_data.svg')
#%%
# Density plot
ax = logged.plot(x=0, y=1, kind='hexbin',
            gridsize=40,
            colormap=SpectralBlack)
fig = ax.get_figure()
fig.set_size_inches(17, 12)
fig.savefig('est_v_data_density.svg')