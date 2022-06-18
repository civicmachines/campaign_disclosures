# Code for generating figure 6 from paper:
#How Online Platforms’ Algorithmic Tools Shape the Distribution of Political Advertising.
#Orestis Papakyriakopoulos, Christelle Tessono, Arvind Narayanan, Mihir Kshirsagar
#AAAI/ACM Conference on Aritificial Intelligence, Ethics, and Society 2022


import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
#load data
df_logreg = pd.read_csv("./tiktok_data.csv")

#run regression
df_logreg.author_id = df_logreg.author_id.astype(str)
df_logreg.author_nickname = df_logreg.author_nickname.astype(str)
df_logreg = df_logreg.join(df_users.set_index(['author_id', "author_nickname"]), on=['author_id', "author_nickname"], lsuffix="_video", rsuffix="_author")
df_logreg = df_logreg[df_logreg["diggCount_author"].notna()]

y = df_logreg.warnInfo.to_list()
x = df_logreg[["diggCount_video", "diggCount_author", "shareCount", 
               "commentCount","playCount", "followerCount","heartCount",
               "videoCount", "heart", "liked", "average_heart", 'biden', 'trump', 'vote', 'blm','abortion','gun',
               'desc']]
#,pd.get_dummies(x["desc"], drop_first=True, prefix = "hashtag_")
x = pd.concat((x["diggCount_video"]/100000,x["shareCount"]/100000,x["commentCount"]/100000,
               x["playCount"]/100000, x["diggCount_author"]/100000, x['trump'], x['biden'], x['vote'], x['blm'],x['abortion'],x['gun']), 
              axis=1).values
x = sm.add_constant(x, prepend = False)

mdl = sm.Logit(y, x)
mdl_fit = mdl.fit()
#mdl_margeff = mdl_fit.get_margeff()
# summary of regression
print(mdl_fit.summary())
# print(mdl_fit.summary().as_latex())

#calculate odds
params = mdl_fit.params
conf_int = mdl_fit.conf_int()
# convert log odds to ORs
odds = pd.DataFrame(np.exp(conf_int))
odds.columns = ['2.5%', '97.5%']
odds['odds_ratio'] = np.exp(params)
odds['i'] = ["video likes (by 100k)", "video shares (by 100k)", "video comments (by 100k)",
              "playCount (by 100k)", "author likes (by 100k)", '#biden','#trump','#vote','#blm','#abortion','#gun',"const"]
# check if pvalues are significant
odds['pvalues'] = mdl_fit.pvalues
odds['significant?'] = ['significant' if pval <= 0.05 else 'not significant' for pval in mdl_fit.pvalues]
odds = odds.set_index(['i'])
odds

# plot results
plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(6, 4), dpi=150)
ci = [odds.iloc[:-1][::-1]['odds_ratio'] - odds.iloc[:-1][::-1]['2.5%'].values, odds.iloc[:-1][::-1]['97.5%'].values - odds.iloc[:-1][::-1]['odds_ratio'] ]
plt.errorbar(x= odds.iloc[:-1][::-1]['odds_ratio'], y= odds.iloc[:-1][::-1].index.values, xerr=ci ,
            color='black', linestyle='None', linewidth=0.6,
            marker="o", markersize=3, mfc="white", mec="black")
plt.axvline(x=1, linewidth=0.8, linestyle='--', color='black')
plt.tick_params(axis='both', which='major', labelsize=8)
plt.xlabel('Odds Ratio change under the presence of a warning', fontsize=8)
plt.xscale('log')
plt.tight_layout()
plt.title("Relation of video parameters to warning placement")
#plt.xlim(-0.0001, 0.0001)
# plt.savefig('raw_forest_plot.png')
plt.show()

# calculate moderation frequency by user
author_counter = collections.Counter()
for index, row in df_logreg.iterrows():
  author_counter.update({row["author_id"]: row["warnInfo"]})

video_counter = collections.Counter()

for index, row in df_logreg.iterrows():
  video_counter.update({row["author_id"]: 1})

warning_ratio_per_author = list()
for author, freq in author_counter.items():
  num_warnings = author_counter[author]
  num_videos = video_counter[author]
  if num_warnings != num_videos and num_warnings > 0:
    #print(f"Auth: {author} tot. warnings: {num_warnings}, tot. videos: {num_videos}")
    warning_ratio_per_author.append(num_warnings/num_videos)
#plot
plt.bar(list(range(len(warning_ratio_per_author))), sorted(warning_ratio_per_author), color = '#CC6677')
plt.xlabel("Authors")
plt.ylabel("Ratio of # warning on total # political videos per author")
plt.show()

