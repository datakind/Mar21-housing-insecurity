### Data Dictionary

The following dictionary was created using two data files, namely:
1. nyc_acs5-2018_census.csv with `2167` rows in `1034` variables or columns, 
2. nyc_evictions_geocoded.csv with `60788` rows in  `23` columns

- I merged the above two files based on a common variable `tract_code`. 
	- This resulted in `3730` rows with `1060` columns. 
	- Thereafter, I selected a few variables of interest and it resulted in `3730` rows in `54` columns.
- I then performed data cleaning steps on these `54` variables of interest.
- 
Note: Following is the nomenclature for understanding abbreviated names used in the R script titled, `housing_insecurity_EDA.R`:

- huse - house
- incm - income
- retr - retirement
- fdstmp - foodstamp
- fmly - family
- wrkr - worker
- bpl - below poverty line
- cple - couple
- HOD - head of family
- mrtg - mortgage


|S.No.|variable|abbreviated name (in code)|data-type|explanation|min value|max value|
|-----|----|-----|----|----|----|----|
|1|DP03_0052E|huse_incm_less10K|integer|Total households Less than $10,000|0|709|
|2|DP03_0062E|huse_incm_median|integer|Total households median income|15566|130230|
|3|DP03_0066E|huse_with_ssn|integer|Total households with social security|54|1405|
|4|DP03_0068E|huse_incm_retr|integer|Total households with retirement income|0|903|
|5|DP03_0074E|huse_incm_with_fdstmp|integer|Total households with food-stamps in past 12 months|7|1412|
|6|DP03_0075E|fmlys|integer|Families|238|3111|
|7|DP03_0076E|fmly_incm_less10K|integer|Families with less than $10,000|0|520|
|8|DP03_0086E|fmly_incm_median|integer|median family income|21205|156757|
|9|DP03_0093E|wrkr_erng_male|integer|Median earnings for male full-time, year-round worker|-666666666|101292|
|10|DP03_0094E|wrkr_erng_female|integer|Median earnings for female full-time, year-round worker|23448|81705|
|11|DP03_00120E|bpl_fmly_child_less18YR|float|Below poverty line families with children less than 18 years age|-888888888|-888888888|
|12|DP03_00121E|bpl_fmly_child_less5YR|float|Below poverty line families with children less than 5 years age|-888888888|-888888888|
|13|DP03_00123E|bpl_fmly_cple_child_less18YR|float|Married couple with related children less than 18 years age|-888888888|-888888888|
|14|DP03_00124E|bpl_fmly_child_less5YR|float|Married couple with related children less than 5 years age|-888888888|-888888888|
|15|DP03_00125E|bpl_fmly_HOD_female|float|Below poverty line families with female as head of family|-888888888|-888888888|
|16|DP03_00126E|bpl_fmly_HOD_female_child_less18YR|float|Below poverty line families with female as head of family and children less than 18 years age|-888888888|-888888888|
|17|DP03_00129E|bpl_fmly_all_less18YR|float|Below poverty line families with all members below 18 years age|-888888888|-888888888|
|18|DP03_00130E|bpl_fmly_all_child_less18YR|float|Below poverty line families with all children below 18 years age|-888888888|-888888888|
|19|DP03_00131E|bpl_fmly_all_child_less5YR|float|Below poverty line families with all children below 5 years age|-888888888|-888888888|
|20|DP03_00132E|bpl_fmly_all_child_5YR-17YR|float|Below poverty line families with all children between 5-17 years age|-888888888|-888888888|
|21|DP04_0117E|huse_mrtg_no|integer|House without mortgage|0|1308|
|22|DP04_0136E|huse_incm_by_rent|integer|Gross rent as percentage of household income|35|3352|
|23|DP04_0137E|huse_incm_by_rent_less15pct|integer|Gross rent as percentage of household income less than 15%|0|423|
|24|DP04_0138E|huse_incm_by_rent_less20pct|integer|Gross rent as percentage of household income less than 20%|0|437|
|25|DP04_0139E|huse_incm_by_rent_less25pct|integer|Gross rent as percentage of household income less than 25%|0|423|
|26|DP04_0140E|huse_incm_by_rent_less30pct|integer|Gross rent as percentage of household income less than 30%|0|785|
|27|DP04_0141E|huse_incm_by_rent_less35pct|integer|Gross rent as percentage of household income less than 35%|0|519|
|28|DP04_0142E|huse_incm_by_rent_more35pct|integer|Gross rent as percentage of household income more than 35%|0|1448|
