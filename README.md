# Introduction
Housing insecurity is a looming crisis in the U.S. Nearly 5 million Americans lose their homes through eviction and foreclosure. Volunteers will derive insights, create visualizations, and recommend action for two U.S. localities - Hillsborough County, FL and NYC.

# Key Questions for the DataDive Event
1. What is the overall trend of housing loss in these counties over the three-year period? Can any seasonality in housing loss be detected?
2. Which parts of these counties are experiencing the most acute housing loss? For which areas are evictions more prevalent per capita than foreclosures, and vice versa? 
3. For New York City counties, which school districts see the highest rates of eviction?
4. What are some of the key socio-demographic and economic characteristics of individuals who lose their homes to eviction and mortgage foreclosure? Which variables are most closely associated with housing loss, and which are less relevant? Is this different for Hillsborough County compared to New York City? 
5. When during the year are people experiencing evictions? Does this differ by location (NYC and Hillsborough)? 
6. Research Opportunity: Besides the American Community Survey, what other public datasets can you find that contain information potentially relevant to housing loss in these areas (e.g., unemployment, prevalence of residents receiving assistance such as SNAP)? Create a document summarizing their contents and where they can be found.
7. Research Opportunity: What qualitative information, or local context, can be added to this data? What questions arise from looking at the quantitative data or working with the data sources? For instance, how does the eviction process differ in New York City and Hillsborough County? Can you identify any major events from the past few years (prior to 2020) that may have impacted people’s ability to remain housed?

# Datasets with Suggested Uses
This section gives a very brief overview of the files in the `data` folder.
### acs/data_dictionary.csv
Use this file to find 'human-readable' names for the ACS variables in the Hillsborough County and NYC files below.
### acs/hillsborough_acs5-2018_census.csv
Use this file to generate tract-level summaries of demographic and socioeconomic variables for Hillsborough County. It may also be useful for modeling the drivers behind housing loss in Hillsborough County, as the "processed" datasets contain only a small number of the variables found in this file.
### acs/nyc_acs5-2018_census.csv
Use this file to generate tract-level summaries of demographic and socioeconomic variables for New York City counties (boroughs). It may also be useful for modeling the drivers behind eviction in NYC, as the "processed" datasets contain only a small number of the variables found in this file.
### geo/florida_sdist_2021.zip
This shapefile contains Florida senate voting district boundaries for 2021. Use this file if you would like to generate a map of housing loss for Hillsborough County using senate voting districts rather than, or in addition to, census tracts. Sourced from: https://www.fgdl.org/metadataexplorer/explorer.jsp
### geo/florida_usdist_2021.zip
This shapefile contains Florida congressional district boundaries for 2021. Use this file if you would like to generate a map of housing loss for Hillsborough County using congressional districts rather than, or in addition to, census tracts. Sourced from: https://www.fgdl.org/metadataexplorer/explorer.jsp
### geo/hillsborough_fl_2010_tracts_formatted.geojson
This GeoJSON file contains census tract boundaries for Hillsborough County. Use it to generate census tract-level maps of housing loss.
### geo/nyc_2010_tracts_formatted.geojson
This GeoJSON file contains census tract boundaries for all NYC boroughs. Use it to generate census tract-level maps of housing loss.
### geo/nyc_school_districts.geojson
This GeoJSON file contains school district boundaries for all NYC boroughs. Use it to generate school district-level maps of evictions for New York City.
### processed/hillsborough_fl_processed_2017_to_2019_20210225.csv
This file contains data aggregated from the raw Hillsborough County eviction, mortgage foreclosure, and tax lien foreclosure data (see the `raw` folder for these files) together with select variables from the American Community Survey. Use this file to build maps of housing loss for Hillsborough County, or to perform basic statistical analysis of the drivers of housing loss in this locality.
### processed/hillsborough_fl_processed_timeseries_2017_to_2019_20210225.csv
This file contains data aggregated from the raw Hillsborough County eviction, mortgage foreclosure, and tax lien foreclosure data (see the `raw` folder for these files) and consists of monthly time series for housing loss. Use this file to generate time series plots of housing loss for Hillsborough County.
### processed/nyc_processed_2017_to_2019_20210225.csv
This file contains data aggregated from the raw New York City eviction data (see the `raw` folder for this file) together with select variables from the American Community Survey. Use this file to build maps of housing loss for New York City, or to perform basic statistical analysis of the drivers of housing loss in this locality.
### processed/nyc_processed_timeseries_2017_to_2019_20210225.csv
This file contains data aggregated from the raw New York City eviction data (see the `raw` folder for these files) and consists of monthly time series for housing loss. Use this file to generate time series plots of housing loss for New York City. Note: the `eviction-filings` column is an estimate, as only disposed and fully executed evictions are present in the raw dataset provided by the city (in other words, eviction cases that did not result in the tenant's removal are not found in that dataset). These estimates were derived using The Eviction Lab's counts of eviction filings and evictions for NYC from 2014-2016, found here: https://data-downloads.evictionlab.org/
### raw/hillsborough_county_evictions_geocoded.csv
This file contains individual eviction-level information for Hillsborough County evictions from 2017-2019, sourced from Hillsborough County's Open Data portal: https://www.hillsclerk.com/Records-and-Reports/Public-Data-Files. Specifically, records from the `AlphaIndex` were used for this analysis. Addresses were cleaned and run through the census.gov batch geocoder to retrieve census tracts for most rows. This file was used to produce the `processed` dataset above.
### raw/hillsborough_county_mortgage_foreclosures_geocoded.csv
This file contains individual eviction-level information for Hillsborough County foreclosures from 2017-2019, sourced from Hillsborough County's Open Data portal: https://www.hillsclerk.com/Records-and-Reports/Public-Data-Files. Specifically, records from the `AlphaIndex` were used for this analysis. Addresses were cleaned and run through the census.gov batch geocoder to retrieve census tracts for most rows. This file was used to produce the `processed` dataset above.
### raw/hillsborough_county_tax_liens_geocoded.csv
This file contains individual eviction-level information for Hillsborough County tax lien foreclosures from 2017-2019, sourced from Hillsborough County's Open Data portal: https://www.hillsclerk.com/Records-and-Reports/Public-Data-Files. Specifically, records from the `AlphaIndex` were used for this analysis. Addresses were cleaned and run through the census.gov batch geocoder to retrieve census tracts for most rows. This file was used to produce the `processed` dataset above.
### nyc_evictions_geocoded.csv
This file contains individual eviction-level information for NYC evictions from 2017-2019, sourced from NYC's Open Data portal: https://data.cityofnewyork.us/City-Government/Evictions/6z8x-wfk4. Addresses were cleaned and run through the census.gov batch geocoder to retrieve census tracts for most rows. This file was used to produce the `processed` dataset above.
### tax_lien_prediction/nyc_census_tracts_to_neighborhoods.xlsx
This file contains a mapping of census tracts to New York City neighborhoods. Use this file in conjunction with the Zillow data file to get estimates of home values over time for the census tracts that make up a particular NYC neighborhood. 
### tax_lien_prediction/nyc_tax_lien_sale_list.csv
This file contains properties eligible to be included in a tax lien sale due to unpaid utilities or property taxes. Use this file to build a model that predicts tax lien sale events. Sourced from: https://data.cityofnewyork.us/City-Government/Tax-Lien-Sale-Lists/9rz4-mjek
### tax_lien_prediction/zillow_nyc_neighborhoods_typical_home_values_time_series.xlsx
This file contains roughly 25 year of monthly time series for "typical" home values by neighborhood in NYC. Sourced from: https://www.zillow.com/research/data/. Notes: according to Zillow, these values represent homes in the 35th to 65th percentile; very low-valued home and very high-valued homes are excluded. Additionally, the neighborhood names in this file do *not* directly map to the neighborhood names in the `nyc_census_tracts_to_neighborhoods.xlsx` file - some manual adjustments may be needed to ensure that neighborhood names are consistent across all files.
