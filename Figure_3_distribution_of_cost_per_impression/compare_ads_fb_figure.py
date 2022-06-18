import pandas as pd
import matplotlib.pyplot as plt
from piecewise import piecewise

# load ads with targeting information
df_ads = pd.read_csv('fb_ads_audience_characteristics.csv')

# load data collected from the facebook business manager
df_manager = pd.read_csv("fb_cost_reach.csv",sep="\t")

# clean data
df_manager.Reach[df_manager.Reach.isna()]=" - "
df_manager["min_reach"] = df_manager.Reach.apply(lambda x: x.split("-")[0])
df_manager["max_reach"] = df_manager.Reach.apply(lambda x: x.split("-")[1])
df_us_all = df_manager[(df_manager.Gender=='All') & (df_manager.State=='USA')]
df_us_all = df_us_all.reset_index()
df_us_all.loc[:,'min_reach'] = pd.to_numeric(df_us_all.min_reach)
df_us_all.loc[:,'max_reach'] = pd.to_numeric(df_us_all.max_reach)
df_us_all['Cost ($)'] = pd.to_numeric(df_us_all['Cost ($)'])


# find ads that were placed in the total US
df_ads = df_ads.sort_values('spend.upper_bound')
USA = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',  'SC', 'SD', 'TN', 'TX', 'UT',  'VA', 'WA', 'WV', 'WI', 'WY', 'DC',
'M-18-24', 'M-25-34','M-35-44', 'M-45-54', 'M-55-64', 'M-65+', 'F-18-24', 'F-25-34', 'F-35-44', 'F-45-54','F-55-64', 'F-65+']

df_ads[USA] = df_ads[USA].apply(pd.to_numeric, errors='coerce')
df_USA = df_ads[pd.DataFrame.all(df_ads[USA]>0,1)]
df_USA[df_USA["spend.upper_bound"]==0] = 10000000
df_USA[df_USA["impressions.upper_bound"]==0] = 10000000
df_USA['mean_cost'] = (df_USA['spend.lower_bound'] +  df_USA['spend.upper_bound'])/2
df_USA['mean_impressions'] = (df_USA['impressions.lower_bound'] +  df_USA['impressions.upper_bound'])/2



# interpolate lines based on the values of the facebook business manager
model = piecewise(df_us_all['Cost ($)'][:-1], df_us_all['min_reach'][:-1])
df_USA['predicted_lower_impressions'] = model.predict(df_USA['spend.lower_bound'])
model = piecewise(df_us_all['Cost ($)'][:-1], df_us_all['max_reach'][:-1])
df_USA['predicted_upper_impressions'] = model.predict(df_USA['spend.upper_bound'])
df_USA['error'] =  (df_USA['impressions.upper_bound'] -df_USA['impressions.lower_bound'])/2

# find which values fall within the predicted intervals and which not
df_USA_reduced = df_USA[(df_USA['predicted_upper_impressions'] < df_USA['impressions.lower_bound']) | (df_USA['predicted_lower_impressions'] > df_USA['impressions.upper_bound'])]
df_USA_within = df_USA[~((df_USA['predicted_upper_impressions'] < df_USA['impressions.lower_bound']) | (df_USA['predicted_lower_impressions'] > df_USA['impressions.upper_bound']))]


# plot predicted & actual values
fig, ax = plt.subplots(figsize=(3,3.5))
lines = ['--' , ':']
labels = ['min predicted reach', 'max predicted reach']
for idx, name in enumerate(['min_reach','max_reach']):
    ax.plot(df_us_all['Cost ($)'],df_us_all[name],lines[idx], color = 'black', label=labels[idx] )
ax.errorbar(df_USA_reduced['mean_cost'], df_USA_reduced['mean_impressions'] , df_USA_reduced['error'], color='#CC6677', label = 'unexplained targeting', fmt="o")
ax.errorbar(df_USA_within['mean_cost'], df_USA_within['mean_impressions'] , df_USA_within['error'], color='#88CCEE', label = 'plausible targeting', fmt="o")
ax.set_xlim(1,1000000)
ax.set_xlabel("Cost ($)")
ax.set_ylabel("Nr of Impressions")
ax.loglog()
ax.legend(loc='best')
ax.get_legend().remove()
#ax.set_title("Explainability of political ads on Facebook \n Ad parameters: Total US - All Genders/Ages")
fig.tight_layout()
fig.savefig('fb_all.png')

#####################################################################################################
##find ads that were placed in California, and seen by Women
df_cal_f = df_manager[(df_manager.Gender=='Women') & (df_manager.State=='California')]
df_cal_f = df_cal_f.reset_index()
df_cal_f.loc[:,'min_reach'] = pd.to_numeric(df_cal_f.min_reach)
df_cal_f.loc[:,'max_reach'] = pd.to_numeric(df_cal_f.max_reach)
df_cal_f['Cost ($)'] = pd.to_numeric(df_cal_f['Cost ($)'])


not_cal_female = ['AL', 'AK', 'AZ', 'AR','CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',  'SC', 'SD', 'TN', 'TX', 'UT',  'VA', 'WA', 'WV', 'WI', 'WY', 'DC',
'M-18-24', 'M-25-34','M-35-44', 'M-45-54', 'M-55-64', 'M-65+']

# extrapolate lines from values
df_cal_f_ads = df_ads[pd.DataFrame.all(df_ads[not_cal_female]==0,1)]
df_cal_f_ads = df_cal_f_ads[pd.DataFrame.all(df_cal_f_ads[['CA','F-18-24', 'F-25-34', 'F-35-44', 'F-45-54','F-55-64', 'F-65+']]>0,1)]
model = piecewise(df_cal_f['Cost ($)'], df_cal_f['min_reach'])
df_cal_f_ads['predicted_lower_impressions'] = model.predict(df_cal_f_ads['spend.lower_bound'])
model = piecewise(df_cal_f['Cost ($)'], df_cal_f['max_reach'])
df_cal_f_ads['predicted_upper_impressions'] = model.predict(df_cal_f_ads['spend.upper_bound'])
df_cal_f_ads[df_cal_f_ads["spend.upper_bound"]==0] = 10000000
df_cal_f_ads[df_cal_f_ads["impressions.upper_bound"]==0] = 10000000
df_cal_f_ads['error'] =  (df_cal_f_ads['impressions.upper_bound'] -df_cal_f_ads['impressions.lower_bound'])/2
df_cal_f_ads['mean_cost'] = (df_cal_f_ads['spend.lower_bound'] +  df_cal_f_ads['spend.upper_bound'])/2
df_cal_f_ads['mean_impressions'] = (df_cal_f_ads['impressions.lower_bound'] +  df_cal_f_ads['impressions.upper_bound'])/2

# find which values fall within the predicted intervals and which not
df_cal_f_ads_reduced = df_cal_f_ads[(df_cal_f_ads['predicted_upper_impressions'] < df_cal_f_ads['impressions.lower_bound']) | (df_cal_f_ads['predicted_lower_impressions'] > df_cal_f_ads['impressions.upper_bound'])]
df_cal_f_ads_within = df_cal_f_ads[~((df_cal_f_ads['predicted_upper_impressions'] < df_cal_f_ads['impressions.lower_bound']) | (df_cal_f_ads['predicted_lower_impressions'] > df_cal_f_ads['impressions.upper_bound']))]


# plot predicted & actual values

fig, ax = plt.subplots(figsize=(3,3.5))
lines = ['--' , ':']
labels = ['min predicted reach', 'max predicted reach']
for idx, name in enumerate(['min_reach','max_reach']):
    ax.plot(df_cal_f['Cost ($)'],df_cal_f[name],lines[idx], color = 'black', label=labels[idx] )
ax.errorbar(df_cal_f_ads_reduced['mean_cost'], df_cal_f_ads_reduced['mean_impressions'] , df_cal_f_ads_reduced['error'],color='#CC6677', label = 'unexplainable targeting', fmt="o")
ax.errorbar(df_cal_f_ads_within['mean_cost'], df_cal_f_ads_within['mean_impressions'] , df_cal_f_ads_within['error'], color='#88CCEE', label = 'plausible targeting', fmt="o")
ax.set_xlim(1,1000000)
ax.set_xlabel("Cost ($)")
ax.set_ylabel("Nr of Impressions")
ax.loglog()
fig.tight_layout()
ax.legend(loc='best')
ax.get_legend().remove()
#ax.set_title("Explainability of political ads on Facebook \n Ad parameters: California - Female, All Ages")
fig.savefig('fb_cali.png')
