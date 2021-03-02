# Exploratory Data analysis for housing insecurity
# Objective: To determine variables relevant to hosuing insecurity prediction
# required data files: nyc_acs5-2018_census.csv, nyc_evictions_geocoded.csv
# Script author: Ashish Dutt
# Script create date: 02/3/2021
# Script last modified date: 02/3/2021
# Email: ashish.dutt8@gmail.com

# clean the workspace
rm(list = ls())
# required libraries
library(tidyverse)

# load the data tract only data file for cleaning
df_nycacs_raw <- read.csv("data/acs/nyc_acs5-2018_census.csv")
df_nycevict_raw <- read.csv("data/raw/nyc_evictions_geocoded.csv")

colnames(df_nycacs_raw)
colnames(df_nycevict_raw)

# lowercase column names
lowercase_cols<- function(df){
  for (col in colnames(df)) {
    colnames(df)[which(colnames(df)==col)] = tolower(col)
  }
  return(df)
}

# df_nycacs_raw <- lowercase_cols(df_nycacs_raw)
df_nycevict_raw <- lowercase_cols(df_nycevict_raw)
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
colnames(df_nycevict_raw)
df_nycevict_raw$tract_code<- as.character(df_nycevict_raw$tract_code)

df_nycevict_raw<- df_nycevict_raw %>%
  # split variable executed_date into day,month, year cols
  separate(executed_date, into = c("executed_year", 
                                   "executed_month", 
                                   "executed_day"), sep = "/") %>%
  separate(lon_lat, into = c("lon", "lat"), sep=",")

# I find the variable tract_code is common in both nyc eviction data and nyc acs raw data
# So I'll now join both these files on tract_code
df_nycacs_evict_raw <- inner_join(df_nycacs_raw, df_nycevict_raw, by=c("tract_code"))
dim(df_nycacs_evict_raw) # [1] 3730 rows with 1060 columns
write.csv(df_nycacs_evict_raw, file =  "data//raw//df_nycacs_evict_raw.csv")
# subset the data based on identified variables from the data dictionary
subset_vars <- c("DP03_0052E", "DP03_0062E", "DP03_0066E", "DP03_0068E", "DP03_0074E", 
                 "DP03_0075E", "DP03_0076E", "DP03_0086E", "DP03_0093E", "DP03_0094E", 
                 "DP03_0120E", "DP03_0121E", "DP03_0123E", "DP03_0124E", "DP03_0125E", 
                 "DP03_0126E", "DP03_0129E", "DP03_0130E", "DP03_0131E", "DP03_0132E", 
                 "DP04_0110E", "DP04_0117E", "DP04_0136E", "DP04_0137E", "DP04_0138E", 
                 "DP04_0139E", "DP04_0140E", "DP04_0141E", "DP04_0142E",
                 "court_index_number", "docket_number","eviction_address","eviction_apt_num",
                 "executed_year","executed_month" ,"executed_day", "marshal_first_name",
                 "marshal_last_name","residential_commercial_ind","borough","eviction_zip",
                 "address.cleaned", "state","input_address","match_indicator" ,"match_type",
                 "matched_address","lon","lat","tiger_line_id","side", "state_code",
                 "county_code", "tract_code", "block_code")

df_subset<- df_nycacs_evict_raw[,subset_vars]
# lowercase all cols
df_subset<- lowercase_cols(df_subset)
colnames(df_subset)
