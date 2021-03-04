## Findings for data file named, `nyc_acs-2018-census.csv`

Note: variables/columns are synonyms in this report.

|S.No.|Metric|Finding/Observation|
|-----|----|-----|
|1.|Original data shape| 2167 rows, 1034 variables|
|2.|Missing data| None|
|3.|Variables with zero or constant variance|"DP02_0015PE" "DP02_0016PE" "DP02_0038PE" "DP02_0039PE" "DP02_0040PE" "DP02_0041PE" "DP02_0042PE" "DP03_0009E" "DP03_0062PE" "DP03_0086PE" "DP03_0090PE" "DP03_0092PE" "DP03_0093PE" "DP03_0094PE" "DP03_0119E"  "DP03_0120E" "DP03_0121E"  "DP03_0122E"  "DP03_0123E"  "DP03_0124E" "DP03_0125E"  "DP03_0126E"  "DP03_0127E"  "DP03_0128E" "DP03_0129E"  "DP03_0130E"  "DP03_0131E"  "DP03_0132E" "DP03_0133E"  "DP03_0134E"  "DP03_0135E"  "DP03_0136E"  "DP03_0137E"  "DP04_0004PE" "DP04_0005PE" "DP04_0037PE" "DP04_0048PE" "DP04_0049PE" "DP04_0089PE" "DP04_0101PE" "DP04_0109PE" "DP04_0116PE" "DP04_0125PE" "DP04_0134PE" "DP04_0135PE" "DP04_0143PE" "DP05_0004PE" "DP05_0018PE" "DP05_0028PE" "DP05_0032PE"| 


Post removing the 50 variables with zero variance, I selected the following 18 variables for further analysis. Note, initially this selection is based on work-experience and gut-feeling only.

|S.No.|Original variable name|New friendly name|explanation|min value|max value|
|-----|----|-----|-----|-----|------|
|1|dp03_0052e|huse_incm_less10K|Total households Less than $10,000|15566|130230|
|2|dp03_0062e|huse_incm_median|Total households median income|15566|130230|
|3|dp03_0066e|huse_with_ssn| Total households with social security|54|1405|
|4|dp03_0068e|huse_incm_retr| Total households with retirement income|0|903|
|5|dp03_0074e|huse_incm_with_fdstmp| Total households with food-stamps in past 12 months|7|1412|
|6|dp03_0075e|fmlys| Families|238|3111|
|7|dp03_0076e|fmly_incm_less10K| Families with less than $10,000|0|520|
|8|dp03_0086e|fmly_incm_median| median family income|21205|156757|
|9|dp03_0093e|wrkr_erng_male| Median earnings for male full-time, year-round worker|21975|101292|
|10|dp03_0094e|wrkr_erng_female| Median earnings for female full-time, year-round worker|23448|81705|
|11|dp04_0117e|huse_mrtg_no| House without mortgage|0|1308|
|12|dp04_0136e|huse_incm_by_rent| Gross rent as percentage of household income|35|3352|
|13|dp04_0137e|huse_incm_by_rent_less15pct| Gross rent as percentage of household income less than 15%|0|423|
|14|dp04_0138e|huse_incm_by_rent_less20pct| Gross rent as percentage of household income less than 20%|0|437|
|15|dp04_0139e|huse_incm_by_rent_less25pct| Gross rent as percentage of household income less than 25%|0|423|
|16|dp04_0140e|huse_incm_by_rent_less30pct| Gross rent as percentage of household income less than 30%|0|785|
|17|dp04_0141e|huse_incm_by_rent_less35pct| Gross rent as percentage of household income less than 35%|0|519|
|18|dp04_0142e|huse_incm_by_rent_more35pct| Gross rent as percentage of household income more than 35%|0|1448|

## Findings for data file named, `nyc_evictions_geocoded.csv`

|S.No.|Metric|Finding/Observation|
|-----|----|-----|
|1.|Original data shape|60788 rows, 23 variables|
|2.|Missing data| 26645 values|
|3.|Missing data variable names, missing value count|`tiger_line_id`:5329; `state_code`:5329; `county_code`:5329; `tract_code`: 5329; `block_code`:5329|

- It seems the missing data is systematic and not random. So, I removed the missing data from further analysis. 

### Clean data file location

- data file `nyc_evictions_geocoded.csv` is cleaned and saved to folder, `data\_volunteer_created_datasets\df_nycevict_raw.csv`
- data file `nyc_acs-2018-census.csv` and `nyc_evictions_geocoded` are merged and subsetted as `data\_volunteer_created_datasets\df_nycacs_evict_raw_subset.csv`


