# Code for generating figure 7 from paper: 
#How Online Platforms’ Algorithmic Tools Shape the Distribution of Political Advertising.
#Orestis Papakyriakopoulos, Christelle Tessono, Arvind Narayanan, Mihir Kshirsagar
#AAAI/ACM Conference on Aritificial Intelligence, Ethics, and Society 2022


library(dplyr)
library(ggplot2)
library(ggpubr)
library(grid)
library(gtable)

df_t <- read.csv('TikTok_influencers_figure_7.csv', sep=';')
df_g <- read.csv('Google_advertisers_figure_7.csv', sep=';')
df_fb <- read.csv("Facebook_advertisers_figure_7.csv", sep=';')

# FEC registered amount
df_fb %>% group_by(FEC_registered) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count))
df_g %>% group_by(FEC_registered) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count))

# advertisers by ad category
df_fb %>% group_by(Broad_Sector) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count))
df_g %>% group_by(Broad_Sector) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count))

# advertisers by entity type
df_fb %>% group_by(Support_Type) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) 
df_g %>% group_by(Support_Type) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) 

# advertisers by partisanship
df_fb %>% group_by(Specific_Party) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) 
df_g %>% group_by(Specific_Party) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) 

# top 10 advertisers non FEC registered
df_g[df_g$FEC_registered=="NO",c('Advertiser_Name',"Spend_USD")][1:10,]
df_fb[df_fb$FEC_registered=="NO",c('Page.Name',"spend")][1:10,]

#tiktok links
df_t$Support_Type[df_t$Support_Type==""] <-"no link"
df_t %>% group_by(Support_Type)  %>%  summarise(count = n())

#########################################################################
#make plots

# colorblind palette
safe_colorblind_palette <- c("#88CCEE", "#CC6677", "#DDCC77", "#117733", "#332288", "#AA4499", 
                             "#44AA99", "#999933", "#882255", "#661100", "#6699CC", "#888888")
scales::show_col(safe_colorblind_palette)
#
legend_object <- scale_fill_manual(values = c("Facebook" = "#88CCEE", "Google/YT" = "#CC6677", "TikTok" = "#888888"))


# FEC registered amount
df_fb %>% group_by(FEC_registered) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) -> df_fb_fec
df_fb_fec$platform <- 'Facebook'
df_g %>% group_by(FEC_registered) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count))  -> df_g_fec
df_g_fec$platform <- "Google/YT"
df_fec <- rbind(df_fb_fec,df_g_fec)
df_fec$platform <- as.factor(df_fec$platform)
levels(df_fec$platform) <- c(levels(df_fec$platform), 'TikTok')
p_fec <- ggplot(df_fec,
       aes(x = FEC_registered, y = ratio*100 , fill = platform))  + 
       geom_bar(position="dodge", stat="identity") + theme_minimal() + 
       labs(x = "",
       y = "Percent (%)",
       title = "Registered at FEC") +
        legend_object

# advertisers by ad category
df_fb %>% group_by(Broad_Sector) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) -> df_fb_cat
df_fb_cat$platform <- 'Facebook'

df_g %>% group_by(Broad_Sector) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) -> df_g_cat
df_g_cat$platform <- "Google/YT"
df_cat <- rbind(df_fb_cat,df_g_cat)

p_cat <- ggplot(df_cat,
       aes(x = ratio*100, y = reorder(Broad_Sector, ratio), fill = platform))  + 
  geom_bar(position="dodge", stat="identity") + theme_minimal() + 
  labs(x = "Percent (%)",
       y = "Ad category",
       title = "Ad category") +
      legend_object


# advertisers by type
df_fb %>% group_by(Support_Type) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) -> df_fb_type
df_fb_type$platform <- 'Facebook'

df_g %>% group_by(Support_Type) %>% summarise(count = n()) %>% mutate(ratio = count/sum(count)) -> df_g_type
df_g_type$platform <- "Google/YT"
df_type <- rbind(df_fb_type,df_g_type)

p_type <- ggplot(df_type,
       aes(x = ratio*100, y = reorder(Support_Type, ratio), fill = platform))  + 
  geom_bar(position="dodge", stat="identity") + theme_minimal() + 
  labs(x = "Percent (%)",
       y = "",
       title = "Advertiser type") +
        legend_object

# tiktok links
df_t %>% group_by(Support_Type)  %>%  summarise(count = n()) -> df_t_link

p_link <- ggplot(df_t_link,
                 aes(x = count, y = reorder(Support_Type, count)))  + 
  geom_bar(position="dodge", stat="identity", fill = "#888888") + theme_minimal() + 
  labs(x = "N",
       y = "",
       title = "Links to entities")

p_link

figure <- ggarrange(p_fec,p_cat,p_type,p_link,
                    ncol =4, nrow = 1, common.legend = T,
                    widths = c(2,4,4,4)) 
figure

legend = gtable_filter(ggplot_gtable(ggplot_build(p_fec + theme(legend.position="left"))), "guide-box")
gt <- grid.arrange(legend, p_fec  + theme(legend.position="none"),                               # bar plot spaning two columns
                  p_cat + theme(legend.position="none"), p_type +theme(legend.position="none"),p_link,                               # box plot and scatter plot
                  ncol = 5, nrow = 4, widths = c(2,2,2,4,2),
                  layout_matrix = rbind(c(1,2,3,3,3), c(4,4,4,5,5)))
annotate_figure(as_ggplot(gt), top=textGrob("Advertisers in the libraries", gp = gpar(cex = 1.3)))

