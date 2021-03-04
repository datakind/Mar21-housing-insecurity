# Exploratory Data analysis for housing insecurity
# Objective: To determine variables relevant to hosuing insecurity prediction
# required data files: nyc_acs5-2018_census.csv, nyc_evictions_geocoded.csv
# Script author: Ashish Dutt
# Script create date: 02/3/2021
# Script last modified date: 04/3/2021
# Email: ashish.dutt8@gmail.com

# clean the workspace
rm(list = ls())
# required libraries
library(tidyverse)
library(data.table) # for setnames()


# load the data tract only data file for cleaning
df_nycacs_raw <- read.csv("data/acs/nyc_acs5-2018_census.csv")
df_nycevict_raw <- read.csv("data/raw/nyc_evictions_geocoded.csv")

dim(df_nycacs_raw) # 2167 rows in 1034 cols
dim(df_nycevict_raw) # [1] 60788 rows in  23 cols

# Data Engineering

## 1. Creating new columns
df_nycacs_raw <- df_nycacs_raw %>%
  mutate(newcol = str_extract(index, "\\> tract:[0-9]+"))%>%
  mutate(tract_code = str_extract(newcol,"[0-9]+")) %>%
  unnest(index) %>%
  unique
# drop irrelevant cols
df_nycacs_raw$newcol<- NULL

# Cleaning the nvc eviction geocoded data

# clean the EXECUTED_DATE variable
table(df_nycevict_raw$EXECUTED_DATE) # Observation: date is in month/day/year format

df_nycevict_raw<- df_nycevict_raw %>%
  # split variable executed_date into day,month, year cols
  separate(EXECUTED_DATE, into = c("executed_month", 
                                   "executed_day", 
                                   "executed_year"), sep = "/") %>%
  separate(lon_lat, into = c("lon", "lat"), sep=",")

table(df_nycevict_raw$executed_year) # Observation: data from year 2017 to 2020. One garbage value of 70
# remove the year 70 value from executed_year
df_nycevict_raw<- df_nycevict_raw %>%
  filter(!(executed_year=="70"))
table(df_nycevict_raw$executed_year)
# Observation: The year in variable `executed_year` has the format of 1,2,3...12.
# Replace it with 2001,2002,2003...,2012
df_nycevict_raw$executed_month <- plyr::revalue(df_nycevict_raw$executed_month,
                                               c("1"="Jan","2"="Feb","3"="Mar","4"="Apr","5"="May",
                                                 "6"="Jun","7"="Jul","8"="Aug","9"="Sept","10"="Oct",
                                                 "11"="Nov","12"="Dec"))
# I find the variable tract_code is common in both nyc eviction data and nyc acs raw data
df_nycevict_raw$tract_code<- as.character(df_nycevict_raw$tract_code)
# So I'll now join both these files on tract_code
df_nycacs_evict_raw <- inner_join(df_nycacs_raw, df_nycevict_raw, by=c("tract_code"))
dim(df_nycacs_evict_raw) # [1] 3730 rows with 1060 columns
# lowercase column names
lowercase_cols<- function(df){
  for (col in colnames(df)) {
    colnames(df)[which(colnames(df)==col)] = tolower(col)
  }
  return(df)
}
# lower case all variable names
df_nycacs_evict_raw <- lowercase_cols(df_nycacs_evict_raw)
# Rename the column names for acs data file

#df_temp <- df_nycacs_evict_raw
setnames(df_nycacs_evict_raw, 
         old = c("dp03_0052e", "dp03_0062e", "dp03_0066e", "dp03_0068e",
                 "dp03_0074e", "dp03_0075e", "dp03_0076e", "dp03_0086e",
                 "dp03_0093e", "dp03_0094e", "dp03_0120e", "dp03_0121e", 
                 "dp03_0123e", "dp03_0124e", "dp03_0125e", "dp03_0126e", 
                 "dp03_0129e", "dp03_0130e", "dp03_0131e", "dp03_0132e",
                 "dp04_0117e", "dp04_0136e", "dp04_0137e","dp04_0138e", 
                 "dp04_0139e", "dp04_0140e", "dp04_0141e", "dp04_0142e"),
         
         new = c("huse_incm_less10K", "huse_incm_median","huse_with_ssn","huse_incm_retr",
                 "huse_incm_with_fdstmp","fmlys","fmly_incm_less10K","fmly_incm_median",
                 "wrkr_erng_male", "wrkr_erng_female","bpl_fmly_child_less18YR","bpl_fmly_child_less5YR",
                 "bpl_fmly_cple_child_less18YR","bpl_fmly_cple_child_less5YR","bpl_fmly_HOD_female","bpl_fmly_Headfemale_child_less18YR",
                 "bpl_fmly_all_less18YR","bpl_fmly_all_child_less18YR","bpl_fmly_all_child_less5YR", "bpl_fmly_all_child_5YR-17YR",
                 "huse_mrtg_no","huse_incm_by_rent","huse_incm_by_rent_less15pct","huse_incm_by_rent_less20pct",
                 "huse_incm_by_rent_less25pct","huse_incm_by_rent_less30pct","huse_incm_by_rent_less35pct","huse_incm_by_rent_more35pct"
                 )
         )

# subset the data based on identified variables from the data dictionary
subset_vars <- c("huse_incm_less10K", "huse_incm_median","huse_with_ssn","huse_incm_retr",
                 "huse_incm_with_fdstmp","fmlys","fmly_incm_less10K","fmly_incm_median",
                 "wrkr_erng_male", "wrkr_erng_female","bpl_fmly_child_less18YR","bpl_fmly_child_less5YR",
                 "bpl_fmly_cple_child_less18YR","bpl_fmly_cple_child_less5YR","bpl_fmly_HOD_female","bpl_fmly_Headfemale_child_less18YR",
                 "bpl_fmly_all_less18YR","bpl_fmly_all_child_less18YR","bpl_fmly_all_child_less5YR", "bpl_fmly_all_child_5YR-17YR",
                 "huse_mrtg_no","huse_incm_by_rent","huse_incm_by_rent_less15pct","huse_incm_by_rent_less20pct",
                 "huse_incm_by_rent_less25pct","huse_incm_by_rent_less30pct","huse_incm_by_rent_less35pct","huse_incm_by_rent_more35pct",
                 "court_index_number", "docket_number","eviction_address","eviction_apt_num",
                 "executed_year","executed_month" ,"executed_day", "marshal_first_name",
                 "marshal_last_name","residential_commercial_ind","borough","eviction_zip",
                 "address.cleaned", "state","input_address","match_indicator" ,"match_type",
                 "matched_address","lon","lat","tiger_line_id","side", "state_code",
                 "county_code", "tract_code", "block_code")
write.csv(df_nycacs_evict_raw, file =  "data//_volunteer_created_datasets//df_nycacs_evict_raw.csv")

# Take a subset of nycacs_evict_raw file by using the variables identified above (see "subset_vars" variable) for further analysis
df_subset<- df_nycacs_evict_raw[,subset_vars]
# lowercase all cols
df_subset<- lowercase_cols(df_subset)
write.csv(df_subset, file =  "data//_volunteer_created_datasets//df_nycacs_evict_raw_subset.csv")
dim(df_subset) # [1] 3730 rows in 54 cols
names(df_subset)
str(df_subset) # 1:28 are numeric cols

# data summary for continuous variables
summary(df_subset[,c(1:28)])
