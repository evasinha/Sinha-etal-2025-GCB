import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

plt.rc('figure', titlesize=20)
plt.rc('legend', fontsize=20)
plt.rc('axes',   labelsize=20, titlesize=20)
plt.rc('xtick',  labelsize=20)
plt.rc('ytick',  labelsize=20)
plt.rc('figure', figsize=(11, 8.5))

dict_Set_newlines = {'Set1': '$\mathregular{\Delta T_m}$',
            'Set2': '$\mathregular{\Delta T_v}$',
            'Set3': '$\mathregular{\Delta T_{m+v}}$',
            'Set4': '$\mathregular{\Delta P_m}$',
            'Set5': '$\mathregular{\Delta P_v}$',
            'Set6': '$\mathregular{\Delta P_{m+v}}$',
            'Set7': '$\mathregular{\Delta T_m}$ +\n$\mathregular{\Delta P_m}$',
            'Set8': '$\mathregular{\Delta T_v}$ +\n$\mathregular{\Delta P_v}$',
            'Set9': '$\mathregular{\Delta T_{m+v}}$ +\n$\mathregular{\Delta P_{m+v}}$'}

myDict_label_nounits = {'NEE':         'Net Ecosystem Exchange',
                        'NPP':         'Net Primary Production',
                        'GPP':         'Gross Primary Production',
                        'ER':          'Ecosytem Respiration',
                        'NET_NMIN':    'Net Rate of N Mineralization',
                        'NET_PMIN':    'Net Rate of P Mineralization',
                        'TOTECOSYSC':  'Total Ecosystem Carbon',
                        'TOTVEGC':     'Total Vegetation Carbon',
                        'TOTSOMC':     'Total SOM Carbon',
                        'EFLX_LH_TOT': 'Latent Heat Flux',
                        'FSH':         'Sensible Heat Flux'}
# -----------------------------------------------------------

# Make sns heatmap
def sns_heatmap(df, fname, xlabel=None, ylabel=None, title=None, cmap='YlOrRd', center=None):

   # Change directory    
   os.chdir('../figures/')

   fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 10), constrained_layout=True)

   g = sns.heatmap(data=df, annot=True, fmt='.2f', cmap=cmap, center=center,
                   annot_kws = {'size': 20},
                   cbar_kws  = {'label': title})

   g.set(xlabel=xlabel, ylabel=ylabel)

   plt.text(-4.0, 1.5, 'Carbon fluxes', fontsize = 20, ha='center', va='center', rotation=90)
   ax.plot([-3.9,-3.9],[0.25,2.75], color='k', clip_on=False)

   plt.text(-4.0, 4, 'N&P fluxes', fontsize = 20, ha='center', va='center', rotation=90)
   ax.plot([-3.9,-3.9],[3.25,4.75], color='k', clip_on=False)

   plt.text(-4.0, 6.5, 'C Storage', fontsize = 20, ha='center', va='center', rotation=90)
   ax.plot([-3.9,-3.9],[5.25,7.75], color='k', clip_on=False)

   plt.text(-4.4, 9, 'Energy', fontsize = 20, ha='center', va='center', rotation=90)
   plt.text(-4.0, 9, 'fluxes', fontsize = 20, ha='center', va='center', rotation=90)
   ax.plot([-3.9,-3.9],[8.25,9.75], color='k', clip_on=False)

   plt.text(1.5, -1.3, 'Temperature sets', fontsize = 20, ha='center', va='center')
   ax.plot([0.25,2.75],[-1.1,-1.1], color='k', clip_on=False)

   plt.text(4.5, -1.3, 'Precipitation sets', fontsize = 20, ha='center', va='center')
   ax.plot([3.25,5.75],[-1.1,-1.1], color='k', clip_on=False)

   plt.text(7.5, -1.3, 'Temp + precip sets', fontsize = 20, ha='center', va='center')
   ax.plot([6.25,8.75],[-1.1,-1.1], color='k', clip_on=False)

   ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
   #plt.yticks(rotation=0)

   plt.savefig(fname, bbox_inches='tight', dpi=300)

   plt.close(fig=None)

   # Change directory
   os.chdir('../workflow/')

# -----------------------------------------------------------
varnames = ['NPP', 'GPP', 'ER',
            'NET_NMIN', 'NET_PMIN',
            'TOTECOSYSC', 'TOTVEGC','TOTSOMC', 'EFLX_LH_TOT', 'FSH']

# Read data
df = pd.read_csv('../figures/NME_stats.csv')
df = df[df['index'].isin(['NEE', 'NBP']) == False]

df.set_index('index', inplace=True)
df = df.loc[varnames,]
df = df.rename(index = myDict_label_nounits)
df = df.rename(columns = dict_Set_newlines)

sns_heatmap(df, fname='NME_heatmap.png', title='Normalized Mean Error', cmap='bwr', center=0)
