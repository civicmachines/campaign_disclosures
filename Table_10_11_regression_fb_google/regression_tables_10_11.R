library(sjPlot)
library(scales)
library(MASS)
require(nnet)
library(texreg)
#facebook ads
df_fb <- read.csv('facebook_regression.csv', sep =";")
df_fb$ad_delivery_start_time <- as.integer((as.Date(df_fb$ad_delivery_start_time))) - as.integer(as.Date(min(df_fb$ad_delivery_start_time )))
model_fb <- rlm(spending_ratio ~ AL + AK + AZ + AR + CA + CO + CT + DE + FL + GA + ID + IL + IN + IA + KS + KY +
                   LA + ME + MD + MA + MI + MN + MS + MO + MT + NE + NV + NH + NJ + NM + NY + NC + ND + OH + OK + OR + PA + RI + SC +
                   SD + TN + TX + UT + VT + VA + WA + WV + WI + WY + DC + `M.18.24` + `M.25.34` + `M.35.44` + `M.45.54` + 
                   `M.55.64` + `M.65.` + `F.18.24` + `F.25.34` + `F.35.44` + `F.45.54` + `F.55.64` + `F.65.` + ad_delivery_start_time + candidate - 1
                 , data = df_fb)
summary(model_fb)

# google ads
df_g <- read.csv("google_regression.csv", sep =';')
# value mappings to factors
#Spend_USD=="≤ 100" <- 1,#Spend_USD=="100-1k" <- 2,#Spend_USD=='1k-50k' <- 3,#Spend_USD=="50k-100k" <- 4,#Spend_USD=="> 100k" <- 5
df_g$Spend_USD <- as.factor(df_g$Spend_USD)
df_g$Impressions <- as.factor(df_g$Impressions)
df_g$Impressions <- factor(df_g$Impressions, levels =  c('≤ 10k', '10k-100k', '100k-1M','1M-10M','> 10M'))
df_g$Ad_Type <- relevel(as.factor(df_g$Ad_Type), ref = "Text")
model_google <- polr(Impressions ~ Spend_USD + Ad_Type  + Male + Female + age_18_24 + age_25_34 + age_45_54 + age_55_64 + zipcode  + county  + USA + region_not_targeted + candidate, data = df_g, method = "logistic")
summary(model_google)
# results to latex
#table 10
texreg(model_google, single.row = FALSE)
#table 11
texreg(coeftest(model_fb), sideways = TRUE)

