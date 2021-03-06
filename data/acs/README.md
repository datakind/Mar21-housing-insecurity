# Datasets with Suggested Uses
This section (copied from the main readme) gives a very brief overview of the files in the `data/acs` folder.
### acs/data_dictionary.csv
Use this file to find 'human-readable' names for the ACS variables in the Hillsborough County and NYC files below. There are over 1,000 variables in the American Community Survey datasets, but half correspond to count estimates (these end in just 'E', e.g., `DP02_002E`) and half correspond to percentage estimates (these end in 'PE', e.g., `DP02_002PE`). In other words, `DP02_002E` and `DP02_002PE` represent the same information, only in different formats. Hence, depending on whether or not you choose to work with counts or rates in your analysis, it may only be necessary to work with half of these variables.

For more precise definitions of the concepts described in the data dictionary, please see this very thorough documentation provided by the Census Bureau: https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2019_ACSSubjectDefinitions.pdf
### acs/hillsborough_acs5-2018_census.csv
Use this file to generate tract-level summaries of demographic and socioeconomic variables for Hillsborough County. It may also be useful for modeling the drivers behind housing loss in Hillsborough County, as the "processed" datasets contain only a small number of the variables found in this file.
### acs/nyc_acs5-2018_census.csv
Use this file to generate tract-level summaries of demographic and socioeconomic variables for New York City counties (boroughs). It may also be useful for modeling the drivers behind eviction in NYC, as the "processed" datasets contain only a small number of the variables found in this file.
