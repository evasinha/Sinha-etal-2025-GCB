import os
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import seaborn as sns

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

my_pal = {'Control':'black',
          '$\mathregular{\Delta T_m}$' :     'yellow',
          '$\mathregular{\Delta T_v}$' :     'orange',
          '$\mathregular{\Delta T_{m+v}}$' : 'red',
          '$\mathregular{\Delta P_m}$' :     'yellow',
          '$\mathregular{\Delta P_v}$' :     'orange',
          '$\mathregular{\Delta P_{m+v}}$' : 'red',
          '$\mathregular{\Delta T_m + \Delta P_m}$' : 'yellow',
          '$\mathregular{\Delta T_v + \Delta P_v}$' : 'orange',
          '$\mathregular{\Delta T_{m+v} + \Delta P_{m+v}}$' : 'red',
          'Mean change': 'yellow',
          'Variability change': 'orange',
          'Mean + variability change': 'red'}

dict_Set = {'Control': 'Control',
            'Set1': '$\mathregular{\Delta T_m}$',
            'Set2': '$\mathregular{\Delta T_v}$',
            'Set3': '$\mathregular{\Delta T_{m+v}}$',
            'Set4': '$\mathregular{\Delta P_m}$',
            'Set5': '$\mathregular{\Delta P_v}$',
            'Set6': '$\mathregular{\Delta P_{m+v}}$',
            'Set7': '$\mathregular{\Delta T_m + \Delta P_m}$',
            'Set8': '$\mathregular{\Delta T_v + \Delta P_v}$',
            'Set9': '$\mathregular{\Delta T_{m+v} + \Delta P_{m+v}}$'}

#----------------------------------------------------------
def plot_ridgeplot_facetgrid(plot_data, row_var, col_var, y_var, hue_var, xlabel, fname, aspect=4, height=0.75, xvline=None):

    plt.rc('axes',   labelsize=15, titlesize=15)
    plt.rc('xtick',  labelsize=15)
    plt.rc('ytick',  labelsize=15)
    plt.rc('axes',   linewidth=1.5)

    # Change directory
    os.chdir('../figures/')

    # in the sns.FacetGrid class, the 'hue' argument is the one that will be represented by colors with 'palette'
    g = sns.FacetGrid(plot_data, row=row_var, col=col_var, hue=hue_var, aspect=aspect, height=height, 
                      palette=my_pal)
        
    # then we add the densities kdeplots for each month
    g.map(sns.kdeplot, y_var, bw_adjust=1, clip_on=False, fill=True, alpha=0.5)

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=1, linestyle="-", color=None, clip_on=False)

    ncol = len(pd.unique(plot_data[col_var]))
    for i, ax in enumerate(g.axes.flat):
      if(xvline is not None):
        ax.axvline(x=0, color='black', linewidth=1.25)
      # Add facet column title
      if (i in range(0, ncol)):
        tmp = ax.get_title().split('=')[2]
        ax.text(0.5, 1.05, dict_Set[tmp.strip()], transform=ax.transAxes, 
                horizontalalignment='left', verticalalignment='center', fontsize=15)
      # Add facet row title only to first plot
      if (i in range(0, ncol*12, ncol)):
        tmp = ax.get_title().split('=')[1]
        tmp = tmp.split('|')[0]
        ax.text(0, 0.2, tmp.strip().title(), transform=ax.transAxes, 
                horizontalalignment='left', verticalalignment='center', fontsize=15)
        
    # we use matplotlib.Figure.subplots_adjust() function to get the subplots to overlap
    g.figure.subplots_adjust(hspace=0.05)

    # Add legend
    g.add_legend()
    sns.move_legend(g, 'upper center', ncol=10, bbox_to_anchor=(0.45, 0.02), facecolor='gainsboro', title=None, frameon=True, fontsize=15)

    # Modify axis labels, yticks and spines
    g.set(xlabel=xlabel, ylabel='', title='')
    g.set(yticks=[])
    g.tick_params(bottom=False)
    g.despine(bottom=True, left=True)
    
    plt.savefig(fname, bbox_inches='tight', dpi=300)

    plt.close(fig=None)

    # Change directory
    os.chdir('../workflow/')
#----------------------------------------------------------

# Plotting
set_names = ['Set1', 'Set2', 'Set3', 'Set4', 'Set5', 'Set7']
row_var='Month'
col_var='Plot'
hue_var='Set'
xlabel=''

df_forc_temp_sets_mean = pd.read_csv('../figures/AWEGEN_forc_monthly_mean_temp_sets.csv')
df_forc_temp_sets_std  = pd.read_csv('../figures/AWEGEN_forc_monthly_std_temp_sets.csv')

df_forc_precip_sets_mean = pd.read_csv('../figures/AWEGEN_forc_monthly_mean_precip_sets.csv')
df_forc_precip_sets_std  = pd.read_csv('../figures/AWEGEN_forc_monthly_std_precip_sets.csv')

df_forc_temp_sets_mean['Month'] = df_forc_temp_sets_mean['month'].apply(lambda x: calendar.month_name[x])
df_forc_temp_sets_mean['Plot'] = 'Set1'

df_forc_temp_sets_std['Month'] = df_forc_temp_sets_std['month'].apply(lambda x: calendar.month_name[x])
df_forc_temp_sets_std['Plot'] = 'Set1'

df_forc_precip_sets_mean['Month'] = df_forc_precip_sets_mean['month'].apply(lambda x: calendar.month_name[x])
df_forc_precip_sets_mean['Plot'] = 'Set4'

df_forc_precip_sets_std['Month'] = df_forc_precip_sets_std['month'].apply(lambda x: calendar.month_name[x])
df_forc_precip_sets_std['Plot'] = 'Set4'

# ------ Mean plot -----
set_names = ['Set1', 'Set2', 'Set3']
for ind, set_name in enumerate(set_names):
    row_index = df_forc_temp_sets_mean['Set'].isin(['Control', set_name])
    df_forc_temp_sets_mean.loc[row_index,'Plot'] = set_name
    if(ind == 0):
        plot_data = df_forc_temp_sets_mean[row_index]
    else:
        plot_data = pd.concat([plot_data, df_forc_temp_sets_mean[row_index]])

y_var='TBOT'
fname = 'Mean_TBOT_ridgeline_plot.png'
xlabel = 'Temperature [C]'
plot_data['Set'] = [ dict_Set.get(item,item) for item in plot_data['Set'] ]
plot_ridgeplot_facetgrid(plot_data, row_var, col_var, y_var, hue_var, xlabel, fname)

# ------ Standard deviation plot -----
for ind, set_name in enumerate(set_names):
    row_index = df_forc_temp_sets_std['Set'].isin(['Control', set_name])
    df_forc_temp_sets_std.loc[row_index,'Plot'] = set_name
    if(ind == 0):
        plot_data = df_forc_temp_sets_std[row_index]
    else:
        plot_data = pd.concat([plot_data, df_forc_temp_sets_std[row_index]])

y_var='TBOT'
fname = 'Std_TBOT_ridgeline_plot.png'
xlabel = 'Temperature [C]'
plot_data['Set'] = [ dict_Set.get(item,item) for item in plot_data['Set'] ]
plot_ridgeplot_facetgrid(plot_data, row_var, col_var, y_var, hue_var, xlabel, fname)

# ------ Precip Mean plot -----
set_names = ['Set4', 'Set5', 'Set6']
for ind, set_name in enumerate(set_names):
    row_index = df_forc_precip_sets_mean['Set'].isin(['Control', set_name])
    df_forc_precip_sets_mean.loc[row_index,'Plot'] = set_name
    if(ind == 0):
        plot_data = df_forc_precip_sets_mean[row_index]
    else:
        plot_data = pd.concat([plot_data, df_forc_precip_sets_mean[row_index]])

y_var='PRECTmms'
fname = 'Mean_PRECT_ridgeline_plot.png'
xlabel = 'Precipitation [mm/day]'
plot_data['Set'] = [ dict_Set.get(item,item) for item in plot_data['Set'] ]
plot_ridgeplot_facetgrid(plot_data, row_var, col_var, y_var, hue_var, xlabel, fname)

# ------ Standard deviation plot -----
for ind, set_name in enumerate(set_names):
    row_index = df_forc_precip_sets_std['Set'].isin(['Control', set_name])
    df_forc_precip_sets_std.loc[row_index,'Plot'] = set_name
    if(ind == 0):
        plot_data = df_forc_precip_sets_std[row_index]
    else:
        plot_data = pd.concat([plot_data, df_forc_precip_sets_std[row_index]])

y_var='PRECTmms'
fname = 'Std_PRECT_ridgeline_plot.png'
xlabel = 'Precipitation [mm/day]'
plot_data['Set'] = [ dict_Set.get(item,item) for item in plot_data['Set'] ]
plot_ridgeplot_facetgrid(plot_data, row_var, col_var, y_var, hue_var, xlabel, fname)
