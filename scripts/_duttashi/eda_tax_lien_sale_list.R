# Exploratory Data analysis for housing insecurity
# Objective: To determine variables relevant to housing insecurity prediction
# required data files: nyc_tax_lien_sale_list_processed_acs.csv
# dataset description: Unpaid property taxes, water bills, and other charges against a property become tax liens that may be sold in a tax lien sale. 

# Script author: Ashish Dutt
# Script create date: 07/3/2021
# Script last modified date: 12/3/2021
# Email: ashish.dutt8@gmail.com
# data dictionary: https://data.cityofnewyork.us/City-Government/Tax-Lien-Sale-Lists/9rz4-mjek

# clean the workspace
rm(list = ls())

# required libraries
library(magrittr) # for the pipe operator
library(dplyr) # for data manipulation
library(tidyr) # for separate()
library(stringr) # for str_replace() and other functions

# Read the raw nyc acs evict data file
df_raw_nyc_taxlien_sale<- read.csv( "data/_volunteer_created_datasets/nyc_tax_lien_sale_list_processed_acs.csv",
                           na.strings = NA)
# make a copy
df<- df_raw_nyc_taxlien_sale

# lowercase column names
lowercase_cols<- function(df){
  for (col in colnames(df)) {
    colnames(df)[which(colnames(df)==col)] = tolower(col)
  }
  return(df)
}
# lower case all variable names
df <- lowercase_cols(df)
# rename the column names
names(df)<- gsub("\\.", "_", names(df))
colnames(df)
# split month into date
df<- df %>%
  # split variable executed_date into day,month, year cols
  separate(month, into = c("month", "date", "year"), sep = "/")
# recode the months
df <- df %>%
  mutate(month = recode(month,'2'='feb')) %>%
  mutate(month = recode(month,'3'='mar')) %>%
  mutate(month = recode(month,'04'='apr')) %>%
  mutate(month = recode(month,'05'='may')) %>%
  mutate(month = recode(month,'06'='jun')) %>%
  mutate(month = recode(month,'07'='jul')) %>%
  mutate(month = recode(month,'7'='jul')) %>%
  mutate(month = recode(month,'08'='aug')) %>%
  mutate(month = recode(month,'10'='oct'))
# recode the year
df<- df %>%
  # split variable year
  separate(year, into = c("year", "time"), sep = " ")
# change data type
df$borough <- as.character(df$borough)
df <- df %>%
  mutate(borough = recode(borough,'1'='manhattan')) %>%
  mutate(borough = recode(borough,'2'='bronx')) %>%
  mutate(borough = recode(borough,'3'='brooklyn')) %>%
  mutate(borough = recode(borough,'4'='queens')) %>%
  mutate(borough = recode(borough,'5'='statenisld'))

# rename variable names
colnames(df)
# df<-df %>%
#   dplyr::rename(tax_code = tax_class_code) %>%
#   dplyr::rename(bldg_code = building_class) %>%
#   dplyr::rename(cmunty_board = community_board) %>%
#   dplyr::rename(dist_cuncl = council.district) %>%
#   dplyr::rename(huse_num = house.number) %>%
#   dplyr::rename(strt_name = street.name) %>%
#   dplyr::rename(zip_code = zip.code) %>%
#   dplyr::rename(water_debt = water.debt.only) %>%
#   dplyr::rename(tract_code = census.tract.code)

df$tax_class_code <- as.character(df$tax_class_code)
table(df$tax_class_code)
df <- df %>%
  mutate(tax_class_code = recode(tax_class_code,'1'='unit_residency')) %>%
  mutate(tax_class_code = recode(tax_class_code,'2'='apartment')) %>%
  mutate(tax_class_code = recode(tax_class_code,'4'='all_others'))

df <- df %>%
  mutate(water_debt_only = recode(water_debt_only,'YES'='yes')) %>%
  mutate(water_debt_only = recode(water_debt_only,'NO'='no')) 

table(df$cycle)
df$cycle<- factor(df$cycle)
levels(df$cycle) <- list("10_daynotice"=c("10 Day Notice","10 Days Notice"),
                         "30_daynotice"=c("30 Day Notice","30 Days Notice"),
                         "60_daynotice"=c("60 Day Notice","60 Days Notice"),
                         "90_daynotice"=c("90 Day Notice","80 Days Notice"),
                         "final_sale"="Final Sale")
table(df$cycle)


# pivot data from wide to long format
df <- df %>%
  pivot_longer(cols = c('date','year'))
df <- df %>%
  pivot_longer(cols = c('cycle'), values_to = "sale_cycle", names_repair = "minimal")
df <- df %>%
  pivot_longer(cols = c('lot','community_board'), names_repair = "minimal")
df <- df %>%
  pivot_longer(cols = c('block'), names_repair = "minimal")
df <- df %>%
  pivot_longer(cols = c('tax_class_code','building_class'), names_repair = "minimal")

# write to disc
write.csv(df, file =  "data/_volunteer_created_datasets/_duttashi/nyc_tax_lien_sale_list_processed_acs_cleaned.csv")


