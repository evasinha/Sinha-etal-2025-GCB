"""
Python modules for making spatial plots of ELM outputs
"""
import os
import sys 
import pandas as pd
import xarray as xr
import seaborn as sns
import matplotlib as mpl 
import matplotlib.pyplot as plt
mpl.use('Agg')

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'


myDict_units = {'GPP':       'Gross Primary\nProduction\n[$\mathregular{PgC~yr^{-1}}$]',
                'NEE':       'Net Ecosystem\nExchange\n[$\mathregular{PgC~yr^{-1}}$]',
                'NPP':       'Net Primary\nProduction\n[$\mathregular{PgC~yr^{-1}}$]',
                'TOTVEGC':   'Total Vegetation\nCarbon\n[PgC]',
                'EFLX_LH_TOT':'Latent heat\nflux\n[$\mathregular{W~m^{-2}}$]',
                'FSH':        'Sensible heat\nflux\n[$\mathregular{W~m^{-2}}$]'}

my_pal = {'Control':'black',
          'Mean change': 'yellow',
          'Variability change': 'orange',
          'Mean + variability change': 'red'}

line_style = {'Control':'solid',
          'Mean change': 'solid',
          'Variability change': 'solid',
          'Mean + variability change': 'solid'}

line_width = {'Control':1.5,
          'Mean change': 1.25,
          'Variability change': 1.25,
          'Mean + variability change': 1.25}

#----------------------------------------------------------
def plot_facet_relplot(df, fname, x_var, y_var, col_var, row_var, hue_order, hue_var=None, legend_fontsize=15, title=None):
  """Plot timeseries from input xarray
  :param: fname:        file name prefix
  """
  plt.rc('axes',   labelsize=15, titlesize=15)
  plt.rc('xtick',  labelsize=15)
  plt.rc('ytick',  labelsize=15)
  plt.rcParams['axes.facecolor'] = 'gainsboro'

  if('Set2' in hue_order):
    hue_order = ['Control', 'Mean change', 'Variability change', 'Mean + variability change']

    row_index = df['Set'].isin(['Set1', 'Set4', 'Set7'])
    df.loc[row_index,'Set'] = 'Mean change'
    row_index = df['Set'].isin(['Set2', 'Set5', 'Set8'])
    df.loc[row_index,'Set'] = 'Variability change'
    row_index = df['Set'].isin(['Set3', 'Set6', 'Set9'])
    df.loc[row_index,'Set'] = 'Mean + variability change'

  hue_color = []
  hue_style = []
  hue_width = []
  for hue in hue_order:
    hue_color.append(my_pal[hue])
    hue_style.append(line_style[hue])
    hue_width.append(line_width[hue])

  # Change directory
  os.chdir('../figures/')

  g = sns.FacetGrid(data=df, col=col_var, row=row_var, 
                    hue=hue_var, hue_order=hue_order,
                    hue_kws= {'color':hue_color, 'linestyle' : hue_style, 'linewidth':hue_width},
                    height=2, aspect=2.5, sharex='col', sharey='row')
  g.map(plt.plot, x_var, y_var).add_legend()

  ncol = len(pd.unique(df[col_var]))
  nrow = len(pd.unique(df[row_var]))
  for i, ax in enumerate(g.axes.flat):
    # Add horizontal line at y=0 only for the top row showing NEE
    tmp = ax.get_title().split('=')[1]
    tmp = tmp.split('|')[0]
    if (tmp.strip() == 'Net Ecosystem\nExchange\n[$\mathregular{gC~m^{-2}~yr^{-1}}$]' or tmp.strip() == 'Net Ecosystem\nExchange\n[$\mathregular{PgC~yr^{-1}}$]'):
      ax.axhline(y=0, color='black', ls='--')

    # Add facet column title
    if (i in range(0, ncol)):
      tmp = ax.get_title().split('=')[2]
      ax.text(0.5, 0.9, tmp.strip(), transform=ax.transAxes, 
              horizontalalignment='center', verticalalignment='center', fontsize=legend_fontsize)

    # Add facet row title only to first plot
    if (i in range(0, ncol*nrow, ncol)):
      tmp = ax.get_title().split('=')[1]
      tmp = tmp.split('|')[0]
      ax.text(-0.4, 0, tmp.strip(), transform=ax.transAxes, rotation=90,
              horizontalalignment='left', verticalalignment='bottom', fontsize=legend_fontsize)

    if(i in [(len(g.axes.flat) - 3), (len(g.axes.flat) - 2), (len(g.axes.flat) - 1)]):
      ax.text(0.04, -0.2, 2080, transform=ax.transAxes,
                horizontalalignment='center', verticalalignment='top', fontsize=legend_fontsize)
      ax.text(0.28, -0.2, 2085, transform=ax.transAxes,
                horizontalalignment='center', verticalalignment='top', fontsize=legend_fontsize)
      ax.text(0.52, -0.2, 2090, transform=ax.transAxes,
                horizontalalignment='center', verticalalignment='top', fontsize=legend_fontsize)
      ax.text(0.76, -0.2, 2095, transform=ax.transAxes,
                horizontalalignment='center', verticalalignment='top', fontsize=legend_fontsize)

  # we use matplotlib.Figure.subplots_adjust() function to get the subplots to overlap
  g.figure.subplots_adjust(hspace=0.03)

  if(title is not None):
    g.fig.suptitle(title, horizontalalignment='center', x=0.5, fontsize=legend_fontsize)

  g.set(xlabel='', ylabel='', title='')
  sns.move_legend(g, 'upper center', ncol=4, bbox_to_anchor=(0.4, 0.01), facecolor='gainsboro', title=None, frameon=True, fontsize=legend_fontsize)

  plt.savefig(fname, bbox_inches='tight', dpi=300)
  plt.close(fig=None)

  # Change directory
  os.chdir('../workflow/')

# -----------------------------------------------------------

hue_order = ['Historical', 'Set1', 'Set2', 'Set3','Set4', 'Set5', 'Set6', 'Set7', 'Set8', 'Set9', 'Control']

fname_start = 'Carbon_flux_var'
input_file = '_ts.csv'
title       = None  

varnames = ['NEE', 'NPP', 'GPP', 'TOTVEGC', 'EFLX_LH_TOT', 'FSH']
fname_start = 'Carbon_Energy_flux_var'

x_var='year'
y_var='value'
row_var='variable'
hue_var='Set'

for ind, var in enumerate(varnames):
    df_var = pd.read_csv('../figures/' + var + input_file)
    df_var['year'] = pd.DatetimeIndex(df_var['year']).year
    if (ind == 0):
        df = df_var
    else:
        df = pd.merge(df, df_var, on = ['Set', 'year'])

df = df[~df['year'].isin(range(1850, 1950))]

# Convert to long format
df = pd.melt(df, id_vars=['Set','year'])

time_period = 'Annual'
for var in pd.unique(df[row_var]):
  row_index = df[row_var].isin([var])
  df.loc[row_index,row_var] = myDict_units[var]

# Add new column for historical and future time period
df['Time_period'] = '2070-2099'
row_index = df['Set'].isin(['Historical', 'Control'])
df.loc[row_index,'Time_period'] = '1950-2010'

# replace 2070-2099 values to 1980-2009
df['year'] = df.apply((lambda x: x['year'] if x['year'] < 2010 else x['year']-90), axis=1)

# Add new column for historical and future time period
df['Forcing_var'] = 'Temperature sets'

row_index = df['Set'].isin(['Set4', 'Set5', 'Set6'])
df.loc[row_index,'Forcing_var'] = 'Precipitation sets'

row_index = df['Set'].isin(['Set7', 'Set8', 'Set9'])
df.loc[row_index,'Forcing_var'] = 'Temperature + Precipitation sets'

# Drop historical
df = df[~df['Set'].isin(['Historical'])]

# Add Control set under both Forcing variables
df_tmp1 = df[df['Set'].isin(['Control'])]
row_index = df_tmp1['Set'].isin(['Control'])
df_tmp1.loc[row_index,'Forcing_var'] = 'Precipitation sets'

df_tmp2 = df[df['Set'].isin(['Control'])]
row_index = df_tmp2['Set'].isin(['Control'])
df_tmp2.loc[row_index,'Forcing_var'] = 'Temperature + Precipitation sets'

# Combine in to a single df
df = pd.concat([df, df_tmp1, df_tmp2])

df = df[df['variable'].isin(['Net Ecosystem\nExchange\n[$\mathregular{PgC~yr^{-1}}$]',
                               'Net Primary\nProduction\n[$\mathregular{PgC~yr^{-1}}$]' ,
                               'Gross Primary\nProduction\n[$\mathregular{PgC~yr^{-1}}$]',
                               'Total Vegetation\nCarbon\n[PgC]',
                               'Latent heat\nflux\n[$\mathregular{W~m^{-2}}$]',
                               'Sensible heat\nflux\n[$\mathregular{W~m^{-2}}$]'])]

hue_order = ['Control', 'Set1', 'Set2', 'Set3','Set4', 'Set5', 'Set6', 'Set7', 'Set8', 'Set9']

# Remove first ten years
df = df[df['year'].isin(range(1990, 2010))]
fname = fname_start + '_ts_select_sets_last20yrs.png'
plot_facet_relplot(df, fname, x_var=x_var, y_var=y_var, col_var='Forcing_var', row_var=row_var, hue_order=hue_order, hue_var=hue_var, title=title)
