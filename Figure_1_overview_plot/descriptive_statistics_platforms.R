# Code for generating figure 1 from paper: 
#How Online Platforms’ Algorithmic Tools Shape the Distribution of Political Advertising.
#Orestis Papakyriakopoulos, Christelle Tessono, Arvind Narayanan, Mihir Kshirsagar
#AAAI/ACM Conference on Aritificial Intelligence, Ethics, and Society 2022


library(ggplot2)

df <- read.csv2('platform_impression_stats.csv', sep=',')
df$party <- factor(df$party,levels = c("Democratic", "Republican", "nonpartisan", "Trump", "Biden"))

safe_colorblind_palette <- c("#88CCEE", "#CC6677", "#DDCC77",
                             "#117733", "#332288", "#AA4499", 
                             "#44AA99", "#999933", "#882255", "#661100", "#6699CC", "#888888")
# Grouped
ylab <- c(0.1, 1, 10)
aggregate <- ggplot(df, aes(fill=platform, x=party, color = platform)) + 
  geom_errorbar( aes(ymin=min_impressions, ymax=max_impressions), width=.2,
                 position=position_dodge(.3), size=1.5) + 
  theme_bw() +
  scale_color_manual(values = safe_colorblind_palette, breaks = c('facebook','google','youtube'), labels = c("Facebook", "Google", "YouTube")) +
  labs(title = "Range of advertiser impressions by party/candidate", 
       y = "Nr. of impressions", x = 'party/candidate',
       color = "Platform") +
  scale_y_continuous(labels = paste0(ylab, "B"), trans='log10',
                     breaks = 10^9 * ylab)  +
  theme(legend.position = c(0.25,0.22)) + 
  theme(legend.key.size = unit(0.35, 'cm'))
aggregate
# tiktok
df_tiktok <- read.csv2('tiktok_view_stats.csv', sep=',') 
ggplot_build(aggregate)$layout$panel_params[[1]]$y.range

ylab <- c(0.1, 1, 10)
tiktok <- ggplot(df_tiktok, aes(x=party, y=views, color = safe_colorblind_palette[4])) +
  geom_point(shape=4, size=4, stroke = 2) + 
  theme_bw() + 
  labs(title = "Nr. of video views by influencers/hashtag on TikTok", 
       y = "Nr. of views", x = 'influencers/hashtag') +
  scale_y_continuous(labels = paste0(ylab, "B"), trans='log10',
                     breaks = 10^9 * ylab, limits = 10^ggplot_build(aggregate)$layout$panel_params[[1]]$y.range) + 
  theme(legend.position = "none")

library(ggpubr)

figure <- ggarrange(aggregate, tiktok,
                    labels = c("A", "B"), heights = c(4, 3),
                    ncol = 1, nrow = 2)
figure

