

# Feature selection to reduce data dimensionality

# required libraries
library(magrittr) # for the pipe operator
library(dplyr) # for data manipulation
library(caret) # for nearZeroVar()
library(FactoMineR) # for PCA
library(factoextra) # for fviz_screeplot()
library(gridExtra) # for grid.arrange()
library(grid) # for grid.rect()
library(ggpubr) # for annotate_figure()

# Read the raw nyc acs evict data file
df_raw_nycacsevict<- read.csv( "data//_volunteer_created_datasets//_duttashi//df_raw_nycacs_evict_joined.csv")
# make a copy
df<- df_raw_nycacsevict
# drop variables
df$X<-NULL
df$index<-NULL
# check data shape
dim(df) # [1] 3730 898

# separate numeric and character variables
vars_num <- df %>%
  select_if(is.numeric) # 995 out of 101

# DIMENSIONALITY REDUCTION: UNSUPERVISED FEATURE EXTRACTION
# Conduct PCA for continuous variables
df_pca<-PCA(df[,names(vars_num)], graph = FALSE)

#Scree plot to visualize the PCA's
screeplot<-fviz_screeplot(df_pca, addlabels = TRUE,
                          barfill = "gray", barcolor = "black",
                          ylim = c(0, 50), xlab = "Principal Component (PC) for continuous variables", ylab = "Percentage of explained variance",
                          main = "(A) Scree plot: Continuous factors affecting home eviction ",
                          ggtheme = theme_minimal())
screeplot
grid.rect(width = 1.00, height = 0.99, 
          gp = gpar(lwd = 2, col = "black", fill=NA))
# STEP 5.2: Determine Variable contributions to the principal axes
# Contributions of variables to PC1
pc1<-fviz_contrib(df_pca, choice = "var", 
                  axes = 1, top = 10, sort.val = c("desc"),
                  ggtheme= theme_minimal())+
  labs(title="(B) PC-1")

# Contributions of variables to PC2
pc2<-fviz_contrib(df_pca, choice = "var", axes = 2, top = 10,
                  sort.val = c("desc"),
                  ggtheme = theme_minimal())+
  labs(title="(C) PC-2")

fig1<- grid.arrange(arrangeGrob(screeplot), 
                    arrangeGrob(pc1,pc2, ncol=1), ncol=2, widths=c(2,1)) 
annotate_figure(fig1
                ,top = text_grob("Principal Component Analysis (PCA)", color = "black", face = "bold", size = 14)
                ,bottom = text_grob("Data source: \n NYC ACS Census\n", color = "brown",
                                    hjust = 1, x = 1, face = "italic", size = 10)
)
# Add a black border around the 2x2 grid plot
grid.rect(width = 1.00, height = 0.99, 
          gp = gpar(lwd = 2, col = "black", fill=NA))

# clear the graphic device
grid.newpage()

# find the top contributing variables to the overall variation in the dataset
# note you can specify which axes you want to look at with axes=, you can even do axes=c(1,2)

f<-factoextra::fviz_contrib(df_pca, choice = "var", 
                            axes = c(1,2), top = 10, sort.val = c("desc"))

#save data from contribution plot
dat<-f$data
max(dat$contrib)
min(dat$contrib)
#filter out ID's that are higher than, say, 20
r<-rownames(dat[dat$contrib>0.20,])

#extract these from your original data frame into a new data frame for further analysis
df_impvars<-df[r]
dim(df_impvars) # [1] 3730 rows with 158 numeric variables

# add a few categorical variables
df_impvars<- cbind(df_impvars, tract_code=df$tract_code)
df_impvars<- cbind(df_impvars, geoid=df$geoid)
df_impvars<- cbind(df_impvars, executed_day=df$executed_day)
df_impvars<- cbind(df_impvars, executed_month=df$executed_month)
df_impvars<- cbind(df_impvars, executed_year=df$executed_year)
df_impvars<- cbind(df_impvars, borough=df$borough)

dim(df_impvars) # [1] 3730  164

# Filter data based on Borough. There are 2 boroughs
df_brooklyn <- df_impvars %>%
  filter(borough=='BROOKLYN')
df_queens <- df_impvars %>%
  filter(borough == 'QUEENS')
dim(df_brooklyn) # [1] 2777  164
dim(df_queens) # [1] 953 164

# write to disc
write.csv(df_impvars, file =  "data//_volunteer_created_datasets//_duttashi/df_raw_nycacs_evict_impvars.csv")
write.csv(df_brooklyn, file =  "data//_volunteer_created_datasets//_duttashi//df_raw_nycacs_evict_impvars_brooklyn.csv")
write.csv(df_queens, file =  "data//_volunteer_created_datasets//_duttashi//df_raw_nycacs_evict_impvars_queens.csv")
