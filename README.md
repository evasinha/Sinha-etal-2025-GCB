_your zenodo badge here_

# Sinha-etal-2025-GCB

**Interactions between climate mean and variability drive future agroecosystem vulnerability**

Eva Sinha<sup>1\*</sup>, Donghui Xu<sup>1</sup>, Kendalynn A. Morris<sup>2</sup>, Beth A. Drewniak<sup>3</sup>, Ben Bond-Lamberty<sup>2</sup>

<sup>1</sup>Pacific Northwest National Laboratory, Richland, WA, United States
<sup>2</sup>Joint Global Change Research Institute, Pacific Northwest National Laboratory, College Park, MD, United States
<sup>3</sup>Argonne National Laboratory, Lemont, IL, United States

\* corresponding author:  eva.sinha@pnnl.gov

## Abstract
Agriculture is crucial for global food supply and dominates the Earth's land surface. It is unknown, however, how slow but relentless changes in climate mean state, versus random extreme conditions arising from changing variability, will affect agroecosystems' carbon fluxes, energy fluxes, and crop production. We used an advanced weather generator to partition changes in mean climate state versus variability for both temperature and precipitation, producing forcing data to drive factorial-design simulations of U.S. Midwest agricultural regions in the Energy Exascale Earth System Model.
We found that an increase in temperature mean lowers stored carbon, plant productivity, and crop yield, and tends to convert agroecosystems from a carbon sink to a source, as expected; it also can cause local to regional cooling in the earth system model through its effects on the Bowen Ratio.
The combined effect of mean and variability changes on carbon fluxes and pools was nonlinear, i.e. greater than each individual case. For instance, gross primary production reduces by 9%, 1%, and 13% due to change in mean temperature, change in temperature variability, and change in both temperature mean and variability, respectively. Overall, the scenario with change in both temperature and precipitation means leads to the largest reduction in carbon fluxes (-16% gross primary production), carbon pools (-35% vegetation carbon), and crop yields (-33% and -22% median reduction in yield for corn and soybean, respectively). By unambiguously parsing the effects of changing climate mean versus variability, and quantifying their non-additive impacts, this study lays a foundation for more robust understanding and prediction of agroecosystems' vulnerability to 21st-century climate change.


## Journal reference
Sinha, E., Xu D., Morris K., Drewniak, B., Bond-Lamberty B., 2025. Interactions between climate mean and variability drive future agroecosystem vulnerability. Global Change Biology.

## Code reference
Sinha, E., Xu D., Morris K., Drewniak, B., Bond-Lamberty B., 2025. Supporting code for Sinha et al., 2024 - Global Change Biology.
References for each minted software release for all code involved.  

## Data reference

### Input data
1. Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A., Muñoz‐Sabater, J., ... & Thépaut, J. N. (2020). The ERA5 global reanalysis. Quarterly Journal of the Royal Meteorological Society, 146(730), 1999-2049. https://doi.org/10.1002/qj.3803 
2. Stefan Lange, Matthias Büchner (2021): ISIMIP3b bias-adjusted atmospheric climate input data (v1.1). ISIMIP Repository.  https://doi.org/10.48364/ISIMIP.842396.1


### Output data
Sinha, E., Xu D., Morris K., Drewniak, B., Bond-Lamberty B., 2025. Interactions between climate mean and variability drive future agroecosystem vulnerability. Global Change Biology. Zenodo http://doi.org/10.5281/zenodo.14675093


## Contributing modeling software
| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| E3SM | v2 | https://github.com/E3SM-Project/E3SM | link to DOI dataset |
| AWE-GEN |  | https://github.com/xdongh/AWE-GEN/tree/evasinha/gen_weather_ELM | link to DOI dataset |

## Reproduce my figures
Use the following scripts found in the `workflow` directory to reproduce the figures used in this publication.


| Script Name | Description | How to Run |
| --- | --- | --- |
| `plot_Fig1_temp_precip_forcing.py` | Ridgeline plot for temperature mean and standard deviation | `plot_Fig1_temp_precip_forcing.py` |
| `plot_Fig2_ts_reg.py` | Script plotting time series of various carbon and energy fluxes | `python plot_Fig2_ts_reg.py` |
| `plot_Fig3_NRMSE.py` | Script for estimating normalized mean error (NME) | `python plot_Fig3_NRMSE.py` |
| `plot_Fig4_NEE.py` | Spatial plot of NEE | `python plot_Fig4_NEE.py` |
| `plot_Fig5_pft_diff_yield.py` | Script for plotting distribution of percentage difference in yield | `python plot_Fig5_pft_diff_yield.py` |

## Figures

1. [Figure 1 - Modification of temperature forcing for the future set](figures/fig_forc_TBOT.png)
2. [Figure 2 - Time series of carbon and energy fluxes for the entire study region](figures/Carbon_Energy_flux_var_ts_select_sets_last20yrs.png)
3. [Figure 3 - Normalized mean error (NME)](figures/NME_heatmap.png)
4. [Figure 4 - Total annual carbon balance](figures/All_sets_NEE.png)
5. [Figure 5 - Distribution of percentage difference in yield](figures/pft_percent_difference_boxplot_DMYIELD.png)
