# Code for generating figure 4 from paper: 
#How Online Platforms’ Algorithmic Tools Shape the Distribution of Political Advertising.
#Orestis Papakyriakopoulos, Christelle Tessono, Arvind Narayanan, Mihir Kshirsagar
#AAAI/ACM Conference on Aritificial Intelligence, Ethics, and Society 2022

library(ggplot2)
library(gridExtra)
library(grid)
library(ggpubr)

long_fb_ads_biden_gender_all <- read.csv('Biden_ads_no_gender_specific_audience.csv')
long_fb_ads_trump_age_all <- read.csv('Trump_ads_no_age_specific_audience.csv')

p_biden <- ggplot(long_fb_ads_biden_gender_all,aes(x=value)) + 
  geom_histogram(data=subset(long_fb_ads_biden_gender_all,variable == 'male'),aes(fill=variable), alpha = 0.5) +
  geom_histogram(data=subset(long_fb_ads_biden_gender_all,variable == 'female'),aes(fill=variable), alpha = 0.5) +
  theme_minimal() + theme(legend.position = 'right') +
  scale_fill_manual(name="gender", values=c("#CC6677","#88CCEE")) + 
  labs(y="Nr. of ads", x = "Gender breakdown of individuals shown ads", title = "Biden ads - no gender-specific audience")  +
  theme(legend.text=element_text(size=rel(1)))

p_trump  <-ggplot(long_fb_ads_trump_age_all,aes(x=value)) + 
  geom_histogram(data=subset(long_fb_ads_trump_age_all,variable == 'A1824'),aes(fill=variable), alpha = 0.5) +
  geom_histogram(data=subset(long_fb_ads_trump_age_all,variable == 'A2534'),aes(fill=variable), alpha = 0.5) +
  geom_histogram(data=subset(long_fb_ads_trump_age_all,variable == 'A4554'),aes(fill=variable), alpha = 0.5) +
  theme_minimal()  + theme(legend.position = 'right') +
  scale_fill_manual(name="age group", values=c("#CC6677","#88CCEE","#117733"), labels = c("18-24","25-34","45-54")) + 
  labs(y="Nr. of ads", x = "Age breakdown of individuals shown ads", title = "Trump ads - no age-specific audience") +
  theme(legend.text=element_text(size=rel(1)))

figure <-   annotate_figure(ggarrange(p_biden,p_trump, ncol =1, nrow = 2),top = text_grob("Distribution of ads on Facebook", size = 15))
figure