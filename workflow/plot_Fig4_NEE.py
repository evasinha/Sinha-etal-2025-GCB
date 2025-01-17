"""
Python modules for making spatial plots of ELM outputs
"""
import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

plt.rc('figure', titlesize=20)
plt.rc('legend', fontsize=20)
plt.rc('axes',   labelsize=20, titlesize=20)
plt.rc('xtick',  labelsize=20)
plt.rc('ytick',  labelsize=20)
plt.rc('figure', figsize=(11, 8.5))

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

# -----------------------------------------------------------
def facet_plot_US(da_plot, subplot_titles, colplot, colwrap, cmap_col, cbar_label, fig_wt, fig_ht, vmin, fig_extent, show_states, fname, main_title='', stipple_data=None, ref_set=None):

    # Change directory
    os.chdir('../figures/')

    if(fig_wt < 6):
       cbar_aspect = 25
    else:
       cbar_aspect = 60

    # facetting using xarray
    fg = da_plot.plot(
        col         = colplot,
        col_wrap    = colwrap,
        transform   = ccrs.PlateCarree(), # coordinate system of data
        subplot_kws = {'projection': ccrs.LambertConformal(central_longitude=-95, central_latitude=37.5)},
        cmap        = cmap_col,
        vmin        = vmin,
        extend      = 'both',
        cbar_kwargs = {
            'label':       cbar_label,
            'orientation': 'horizontal',
            'shrink':      0.8,
            'aspect':      cbar_aspect,
            'pad':         0.02, # fraction of original axes between colorbar and new image axes
        },
        figsize     =  (fig_wt, fig_ht)
    )

    plt.suptitle(main_title, y=0.99)

    for ax, title in zip(fg.axes.flat, subplot_titles):
       ax.set_title(title)

    # Add stippling
    for ax in fg.axes.flat:
      sel_set = ax.get_title().split('=')[1].strip()
      if(sel_set != ref_set):
        if stipple_data is not None:
          stipple_data_set = stipple_data.sel(Set = sel_set)
          mask = stipple_data_set <= 0.05
          tmp = mask.values
          tmp = tmp[tmp == True]
          ax.contourf(stipple_data_set.lon, stipple_data_set.lat, mask,  1, hatches=['', 'xx'], alpha=0,
                    transform=ccrs.PlateCarree())

    # Iterate thorugh each axis
    for ax in fg.axes.flat:

       # Modify column title
       if (colplot in ['month', 'Set', 'pft', 'col','cft']):
           if ax.get_title():
               tmp = ax.get_title().split('=')[1]
               if(colplot in ['month', 'pft', 'col']):
                   # Add original title to the right of the plot as text
                   ax.text(1.0, 0.5, tmp.title(), transform=ax.transAxes, rotation=-90,fontsize=20)
                   # Remove the original title
                   ax.set_title(label='')
               elif(colplot in ['Set']):
                   ax.set_title(dict_Set[tmp.strip()], fontsize=20)
               else:
                   ax.set_title(tmp.title(), fontsize=20)

    # Define map extent
    fg.map(lambda: plt.gca().set_extent(fig_extent))

    # Add additional features like coastlines, ocean, and lakes
    fg.map(lambda: plt.gca().coastlines())
    fg.map(lambda: plt.gca().add_feature(cfeature.OCEAN))
    fg.map(lambda: plt.gca().add_feature(cfeature.LAND, facecolor ='gainsboro')) # To add a background grey color
    fg.map(lambda: plt.gca().add_feature(cfeature.LAKES, edgecolor='black'))
    if(show_states):
       fg.map(lambda: plt.gca().add_feature(cfeature.STATES, edgecolor='black'))

    plt.savefig(fname, bbox_inches='tight', dpi=300)

    plt.close(fig=None)

    # Change directory
    os.chdir('../workflow/')

# -----------------------------------------------------------

ref_set = 'Control'
fig_extent  = [-99.5, -82, 36.75, 47.25]

ds_plot = xr.open_mfdataset('../figures/All_sets_NEE.nc')
p_values = xr.open_mfdataset('../figures/p_values_NEE.nc')

# Create facet plot showing results for various sets in different columns
cmap_col = 'jet'
vmin = -0.3
cbar_label = 'Net Ecosystem Exchange\n[$\mathregular{gC~m^{-2}~day^{-1}}$]'

facet_plot_US(ds_plot['NEE'], subplot_titles='', colplot='Set', colwrap=2,
                 cmap_col=cmap_col, cbar_label=cbar_label, fig_wt=4.9*2+0.3, fig_ht=2*(4.9+0.6),
                 vmin=vmin, fig_extent=fig_extent, show_states=True, fname='All_sets_NEE.png',
                    stipple_data = p_values['p_values'], ref_set=ref_set)
