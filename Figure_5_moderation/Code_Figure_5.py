# Code for generating figure 5 from paper:
#How Online Platforms’ Algorithmic Tools Shape the Distribution of Political Advertising.
#Orestis Papakyriakopoulos, Christelle Tessono, Arvind Narayanan, Mihir Kshirsagar
#AAAI/ACM Conference on Aritificial Intelligence, Ethics, and Society 2022

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math

# transform data for visualization
def transform_data(list_of_values, dir = None):
    values = np.log10(list_of_values)
    values.loc[values == 0] = 0.1
    values.loc[values <0] = 0

    if dir=='negative':
        values = -values
    return(values)



# Load Google/YouTube Data

df_all = pd.read_csv("google_data_figure_5.csv")
df_all['impressions.lower_bound'] = None
df_all['impressions.upper_bound'] = None
df_all['impressions.lower_bound'][df_all.Impressions=="≤ 10k"] = 0
df_all['impressions.upper_bound'][df_all.Impressions=="≤ 10k"] = 10000
df_all.Impressions[df_all.Impressions=="≤ 10k"] = 5000
df_all['impressions.lower_bound'][df_all.Impressions=='10k-100k'] = 10000
df_all['impressions.upper_bound'][df_all.Impressions=='10k-100k'] = 100000
df_all.loc[df_all.Impressions=='10k-100k', 'Impressions'] = 55000
df_all['impressions.lower_bound'][df_all.Impressions=="100k-1M"] = 100000
df_all['impressions.upper_bound'][df_all.Impressions=="100k-1M"] = 1000000
df_all.loc[df_all.Impressions=='100k-1M', 'Impressions']  = 550000
df_all['impressions.lower_bound'][df_all.Impressions=="1M-10M"] = 1000000
df_all['impressions.upper_bound'][df_all.Impressions=="1M-10M"] = 10000000
df_all.Impressions[df_all.Impressions=="1M-10M"] = 5500000
df_all['impressions.lower_bound'][df_all.Impressions=="> 10M"] = 10000000
df_all['impressions.upper_bound'][df_all.Impressions=="> 10M"] = 100000000
# set maximum cap for uncapped ads
df_all.Impressions[df_all.Impressions=="> 10M"] = 55000000

# moderated image ads on Google (different instances of the same ad identified by id_diversity)
ads_impressions = df_all[['Impressions','id_diversity']].groupby(['id_diversity']).sum()
grouped_ads = df_all.groupby(['moderated','id_diversity']).count().loc[:,'Ad_ID'].unstack()
grouped_ads[grouped_ads.isna()] = 0
grouped_ads = grouped_ads.loc[:,(grouped_ads.iloc[1,:]!=0).tolist()]
grouped_ads = grouped_ads.iloc[:,:-1]
grouped_ads = grouped_ads.transpose()
grouped_ads = pd.merge(grouped_ads, ads_impressions, on='id_diversity')
grouped_ads = grouped_ads.sort_values(['Impressions'])
df_all_moderated = df_all[df_all.id_diversity.isin(grouped_ads.index)]

# Transform data - YouTube
# moderated image ads on YouTube (different instances of the same ad identified by Video_link)
ads_impressions = df_all[['Impressions','Video_link']].groupby(['Video_link']).sum()
grouped_yt = df_all.groupby(['moderated','Video_link']).count().loc[:,'Ad_ID'].unstack()

grouped_yt[grouped_yt.isna()] = 0
grouped_yt = grouped_yt.loc[:,(grouped_yt.iloc[1,:]!=0).tolist()]
grouped_yt = grouped_yt.transpose()
grouped_yt = pd.merge(grouped_yt, ads_impressions, on='Video_link')
grouped_yt = grouped_yt.sort_values(['Impressions'])

# load facebook data & transform
df_fb = pd.read_csv('fb_data_figure_5.csv')
# set maximum cap for uncapped ads
df_fb.loc[df_fb['impressions.lower_bound']==1000000,'impressions.upper_bound'] = 9999999
df_fb['Impressions'] = (df_fb['impressions.lower_bound'] + df_fb['impressions.upper_bound'])/2

# moderated image ads on Facebook (different instances of the same ad identified by image_id)
ads_impressions = df_fb[['Impressions','image_id']].groupby(['image_id']).sum()
grouped_ads_ = df_fb.groupby(['moderated','image_id']).count().loc[:,'id'].unstack()
grouped_ads_[grouped_ads_.isna()] = 0
grouped_ads_ = grouped_ads_.loc[:,(grouped_ads_.iloc[1,:]!=0).tolist()]
grouped_ads_ = grouped_ads_.transpose()
grouped_ads_ = pd.merge(grouped_ads_, ads_impressions, on='image_id')
grouped_ads_ = grouped_ads_.sort_values(['Impressions'])
df_fb_image_moderated = df_fb[df_fb.image_id.isin(grouped_ads_.index)]
df_fb_image_moderated[[ 'impressions.lower_bound' ,'impressions.upper_bound' ,'moderated']].groupby('moderated').sum()

# moderated video ads on facebook (different instances of the same ad identified by video_size)
grouped_video = df_fb.groupby(['moderated','video_size']).count().loc[:,'id'].unstack()
grouped_video[grouped_video.isna()] = 0
grouped_video = grouped_video.loc[:,(grouped_video.iloc[1,:]!=0).tolist()]
df_fb_video_moderated = df_fb[df_fb.video_size.isin(grouped_video.index)]
df_fb_video_moderated[[ 'impressions.lower_bound' ,'impressions.upper_bound' ,'moderated']].groupby('moderated').sum()
ads_impressions = df_fb[['Impressions','video_size']].groupby(['video_size']).sum()
grouped_video = grouped_video.transpose()
grouped_video = pd.merge(grouped_video, ads_impressions, on='video_size')
grouped_video = grouped_video.sort_values(['Impressions'])

# ad videos & images
grouped_total = grouped_video.append(grouped_ads_)
grouped_total = grouped_total.sort_values(['Impressions'])

#######generate figure###################################
fig, axes = plt.subplots(1, 3, figsize=(13, 3))
fig.suptitle('Number of moderated and unmoderated instances of unique ads')

# Google
x = np.log(grouped_ads['Impressions']) #+ np.log(list(map(lambda x: (x+120)/100, grouped_ads.reset_index().index.tolist())))

axes[0].bar(x, transform_data(grouped_ads[1]), width=0.2, color='#88CCEE')
axes[0].bar(x, transform_data(grouped_ads[0],'negative'), width=0.2, color='#CC6677')
axes[0].xaxis.set_ticks([np.log(5000), np.log(50000), np.log(500000), np.log(5000000), np.log(50000000),np.log(500000000)])
axes[0].set_xticklabels(['5k', '50k', '500k', '5M', '50M', '500M'])
axes[0].set_yticklabels(['100','100','10','0','10','100'])
axes[0].set_ylabel('no. of instances')
axes[0].set_title('Google' )
axes[0].set_xlabel('Impressions')


# YouTube

x1 = np.log(grouped_yt['Impressions'])
axes[1].bar(x1, transform_data(grouped_yt[1]), width=0.2, color='#88CCEE')
axes[1].bar(x1, transform_data(grouped_yt[0], "negative"), width=0.2, color='#CC6677')

axes[1].xaxis.set_ticks([np.log(5000), np.log(50000), np.log(500000), np.log(5000000), np.log(50000000),np.log(500000000)])
axes[1].set_xticklabels(['5k', '50k', '500k', '5M', '50M', '500M'])
axes[1].set_yticklabels(['100','100','10','0','10','100'])

axes[1].set_ylabel('no. of instances')
axes[1].set_title('YouTube' )
axes[1].set_xlabel('Impressions')


# Facebook

x2 = np.log(grouped_total['Impressions'])


axes[2].bar(x2, transform_data(grouped_total[1]), width=  0.2, color='#88CCEE')
axes[2].bar(x2, transform_data(grouped_total[0], 'negative'), width=0.2, color='#CC6677')
axes[2].xaxis.set_ticks([np.log(5000), np.log(50000), np.log(500000), np.log(5000000), np.log(50000000), np.log(500000000)])
axes[2].set_xticklabels(['5k', '50k', '500k', '5M', '50M', '500M'])
axes[2].set_yticklabels(['100','100','10','0','10','100'])

axes[2].set_ylabel('no. of instances')
axes[2].set_title('Facebook' )
axes[2].set_xlabel('Impressions')

red_patch = mpatches.Patch(color='#88CCEE', label='moderated')
blue_patch = mpatches.Patch(color='#CC6677', label='unmoderated')
#plt.legend(handles=[red_patch, blue_patch])
fig.legend(handles=[red_patch, blue_patch], labels = ['moderated', 'unmoderated'], loc='upper left')
plt.tight_layout()
plt.show()
