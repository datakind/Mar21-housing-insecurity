# Readme

Explanation of the analysis can be found in hb_vs_nyc_correlation_of_se_factors.ipynb. It seems to have some trouble loading in the Github notebook viewer, so I recommend to open directly in Jupyter. Below I have copied the introduction from the begining of the notebook, with links to the dashboards on Tableau Public.

## Are the key socio-demographic and economic  characteristics of individuals who lose their homes different for Hillsborough County compared to New York City?

Compare evictions in Hillsborough County to NYC using DP02-04 variables (see census data dictionary)

### Contact

Zach Rowland

[linkedin](https://www.linkedin.com/in/zcrowland/) - [github](https://github.com/zrowland885)

### Introduction

In this analysis I created heatmaps of the correlation between key housing insecurity variables for NYC and Hillsborough county, Florida (which I refer to as HB) with their respective socio-economic data from ACS5. I then compare the highest correlations for both locales to see if there are differences in which S-E factors are correlated with housing insecurity in the two locales.<br>

I have created the following two Tableau dashboards to enable data exploration and interpretation of the results of this analysis:
- [Compare different ACS5 factors in NYC and HB](https://public.tableau.com/views/DataKindMar21-housing-insecurityExplorer/Dash?:language=en-GB&:display_count=y&:origin=viz_share_link)
- [Compare correlations between different housing insecurity and socio-economic factors in NYC and HB](https://public.tableau.com/shared/BHXW4RSHF?:display_count=y&:origin=viz_share_link)

### Future work, caveats

Please note that I made this in a weekend and its probable there are mistakes in the analysis, so this should all be checked thoroughly before drawing any definite conclusion. I would first recommend considering what to control for, and any hidden influences on the correlations noted here. For example: <i>DP04_0066E+Estimate!!HOUSE HEATING FUEL!!Occupied housing units!!Fuel oil, kerosene, etc.</i> is slightly correlated with <i>avg-evictions</i> in NYC (0.521), but not in HB (-0.015). But this could just be because these methods of heating are much more common in one of the locales.

### Specific acknowledgements

Thanks to ahopejasen and jhirner who merged the processed data and the ACS5 data for NYC and HB, which I have either used or used the generation code in this analysis. I also got some of the ideas for the heatmaps from snnehete's work.
