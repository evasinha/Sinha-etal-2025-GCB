import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

my_pal = {'Mean\nchange': 'yellow',
          'Variability\nchange': 'orange',
          'Mean + variability\nchange': 'red'}

#----------------------------------------------------------
def plot_boxplot_facet(df, fname, x_var, y_var, col_var, row_var, ylabel, hue_var=None, legend_fontsize=15, title=None):
  """Plot timeseries from input xarray
  :param: fname:        file name prefix
  """
  plt.rc('axes',   labelsize=15, titlesize=15)
  plt.rc('xtick',  labelsize=15)
  plt.rc('ytick',  labelsize=15)

  row_index = df[hue_var].isin(['Set1', 'Set4', 'Set7'])
  df.loc[row_index,hue_var] = 'Mean\nchange'
  row_index = df[hue_var].isin(['Set2', 'Set5', 'Set8'])
  df.loc[row_index,hue_var] = 'Variability\nchange'
  row_index = df[hue_var].isin(['Set3', 'Set6', 'Set9'])
  df.loc[row_index,hue_var] = 'Mean + variability\nchange'

  # Change directory
  os.chdir('../figures/')

  g = sns.catplot(data=df, x=x_var, y=y_var, kind='box',
                  col=col_var, row=row_var, legend=False, 
                  showfliers = False, # outliers are NOT shown
                  hue=hue_var, palette=my_pal,
                  height=5, aspect=1.1) #, sharex='col', sharey='row')

  # Vertical offset for labelling
  vertical_offset = abs(df[y_var].median() * 0.2) # offset from median for display

  ncol = len(pd.unique(df[col_var]))
  nrow = len(pd.unique(df[row_var]))
  for i, ax in enumerate(g.axes.flat):
    # Add facet column title
    if (i in range(0, ncol)):
      tmp = ax.get_title().split('=')[2]
      ax.text(0.5, 1.05, tmp.strip(), transform=ax.transAxes, 
              horizontalalignment='center', verticalalignment='center', fontsize=legend_fontsize)
    # Add facet row title only to first plot
    if (i in range(0, ncol*nrow, ncol)):
      tmp = ax.get_title().split('=')[1]
      tmp = tmp.split('|')[0]
      ax.text(0.02, 0.05, tmp.strip().title(), transform=ax.transAxes, 
              horizontalalignment='left', verticalalignment='center', fontsize=legend_fontsize)

    # Set label for median values
    lines = ax.get_lines()
    categories = ax.get_xticks()

    for cat in categories:
      y = round(lines[4+cat*5].get_ydata()[0],1) 
      ax.text(
          cat, 
          y + vertical_offset, 
          f'{y}', 
          ha='center', 
          va='center', 
          fontweight='semibold', 
          size=15,
          color='black',
      )

  if(title is not None):
    g.fig.suptitle(title, horizontalalignment='center', x=0.5, fontsize=legend_fontsize)

  g.set(xlabel='', ylabel=ylabel, title='')


  plt.savefig(fname, bbox_inches='tight', dpi=300)
  plt.close(fig=None)

  # Change directory
  os.chdir('../workflow/')

#----------------------------------------------------------
# Read csv file
df = pd.read_csv('../figures/data_pft_diff_boxplot_DMYIELD.csv')

# ----- Plot showing distribution of difference between Set and Control -----
hue_var='Plot'
x_var  ='Plot'
col_var='Forcing_var'
row_var = 'pft'
y_var  = 'per_diff'
fname = 'pft_percent_difference_boxplot_DMYIELD.png'
ylabel = '% difference in Crop yield [ton/ha]'
plot_boxplot_facet(df, fname, x_var=x_var, y_var=y_var, col_var=col_var, row_var=row_var, ylabel=ylabel, hue_var=hue_var)
