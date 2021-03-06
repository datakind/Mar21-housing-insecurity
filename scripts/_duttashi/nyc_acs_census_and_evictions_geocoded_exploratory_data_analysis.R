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
library(caret) # for nearZeroVar()
library(magrittr) # for the pipe operator
library(dplyr) # for data manipulation
library(tidyr) # for drop_na()
library(stringr) # for str_extract()
library(data.table) # for setnames()

# read the raw dataset in memory
df_raw_nycacs <- read.csv("data/acs/nyc_acs5-2018_census.csv", na.strings = NA)
df_raw_nycevict <- read.csv("data/raw/nyc_evictions_geocoded.csv", na.strings = NA)

# 1. Exploratory Data Analysis

# 1.1. check data dimension
dim(df_raw_nycacs) # 2167 rows in 1034 cols
dim(df_raw_nycevict) # [1] 60788 rows in  23 cols

# 1.2. check for missing data
sum(is.na(df_raw_nycacs)) # 0 missing values
sum(is.na(df_raw_nycevict)) # [1] 26645 missing values

# 1.3 Find variables with zero variance for df_raw_nycacs datafile
excluded_vars  <- df_raw_nycacs %>%
  summarise_all(var) %>%
  select_if(function(.) . == 0) %>% 
  names() ## Finding: 50 variables with zero variance 

# remove the 50 variables with zero variance for df_raw_nycacs datafile
df_raw_nycacs<- df_raw_nycacs %>%
  select(-one_of(excluded_vars))
dim(df_raw_nycacs) # [1] 2167  984

# Check for near zero variance variables for df_raw_nycacs datafile
badCols<- nearZeroVar(df_raw_nycacs)
dim(df_raw_nycacs[,badCols]) # 108 variables with nearzero variance
names(df_raw_nycacs[,badCols])
# remove the nearzero variance cols
df_raw_nycacs<- df_raw_nycacs[, -badCols]

# 1.4 Find variables with zero variance for df_raw_nycevict datafile
excluded_vars  <- df_raw_nycevict %>%
  summarise_all(var) %>%
  select_if(function(.) . == 0) %>% 
  names() ## Finding: 50 variables with zero variance 

# Check for near zero variance variables
badCols<- nearZeroVar(df_raw_nycevict)
dim(df_raw_nycevict[,badCols]) # 3 variables with nearzero variance
names(df_raw_nycevict[,badCols]) # [1] "RESIDENTIAL_COMMERCIAL_IND" "STATE" "state_code"
# remove the nearzero variance cols
df_raw_nycevict<- df_raw_nycevict[, -badCols]

# remove missing data from df_raw_nycevict dataframe
df_raw_nycevict <- df_raw_nycevict %>%
  drop_na()
colSums(is.na(df_raw_nycevict))

# Data Engineering

## 1. Creating new columns
df_raw_nycacs <- df_raw_nycacs %>%
  mutate(newcol = str_extract(index, "\\> tract:[0-9]+"))%>%
  mutate(tract_code = str_extract(newcol,"[0-9]+")) %>%
  unnest(index) %>%
  unique
# drop irrelevant cols
df_raw_nycacs$newcol<- NULL

# Cleaning the nvc eviction geocoded data

# clean the EXECUTED_DATE variable
table(df_raw_nycevict$EXECUTED_DATE) # Observation: date is in month/day/year format

df_raw_nycevict<- df_raw_nycevict %>%
  # split variable executed_date into day,month, year cols
  separate(EXECUTED_DATE, into = c("executed_month", 
                                   "executed_day", 
                                   "executed_year"), sep = "/") %>%
  separate(lon_lat, into = c("lon", "lat"), sep=",")

table(df_raw_nycevict$executed_year) # Observation: data from year 2017 to 2020. One garbage value of 70
# remove the year 70 value from executed_year
df_raw_nycevict<- df_raw_nycevict %>%
  filter(!(executed_year=="70"))
table(df_raw_nycevict$executed_year)
# Observation: The year in variable `executed_year` has the format of 1,2,3...12.
# Replace it with 2001,2002,2003...,2012
df_raw_nycevict$executed_month <- plyr::revalue(df_raw_nycevict$executed_month,
                                               c("1"="Jan","2"="Feb","3"="Mar","4"="Apr","5"="May",
                                                 "6"="Jun","7"="Jul","8"="Aug","9"="Sept","10"="Oct",
                                                 "11"="Nov","12"="Dec"))
# I find the variable tract_code is common in both nyc eviction data and nyc acs raw data
df_raw_nycevict$tract_code<- as.character(df_raw_nycevict$tract_code)


# So I'll now join both these files on tract_code
df_raw_nycacsevict <- inner_join(df_raw_nycacs, df_raw_nycevict, by=c("tract_code"))
dim(df_raw_nycacsevict) # [1] 3730 rows with 899 columns
# lowercase column names
lowercase_cols<- function(df){
  for (col in colnames(df)) {
    colnames(df)[which(colnames(df)==col)] = tolower(col)
  }
  return(df)
}
# lower case all variable names
df_raw_nycacsevict <- lowercase_cols(df_raw_nycacsevict)

# write to disc
write.csv(df_raw_nycacsevict, file =  "data//_volunteer_created_datasets//_duttashi/df_raw_nycacs_evict_joined.csv")


