import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from scipy import interpolate

# Function to plot error boxes
def makeErrorBoxes(xdata,ydata,xerror,yerror,fc='r',ec='None',alpha=0.5):

    # Create list for all the error patches
    errorboxes = []

    # Loop over data points; create box from errors at each point
    for xc,yc,xe,ye in zip(xdata,ydata,xerror.T,yerror.T):
        rect = Rectangle((xc-xe,yc-ye),xe*2,ye*2)
        errorboxes.append(rect)

    # Create patch collection with specified colour/alpha
    pc = PatchCollection(errorboxes,facecolor=fc,alpha=alpha,edgecolor=ec)

    # Add collection to axes
    ax.add_collection(pc)


# load targeting data
df = pd.read_csv('google_ads_targeting.csv')
# create different dataframes for types of ads. Video = YouTube
df_image = df[df.Ad_Type=="Image"]
df_text = df[df.Ad_Type=="Text"]
df_video = df[df.Ad_Type=="Video"]
###


# load data collected from the google ads manager for image ads placed in the total US
df_manager = pd.read_csv("google_image_cost_reach.csv",sep="\t")
# format data
df_manager["min_reach"] = df_manager.Reach.apply(lambda x: x.split("-")[0])
df_manager["max_reach"] = df_manager.Reach.apply(lambda x: x.split("-")[1])
df_us_all = df_manager[(df_manager.Gender=='All') & (df_manager.State=='USA')]
df_us_all = df_us_all.reset_index()
df_us_all.loc[:,'min_reach'] = pd.to_numeric(df_us_all.min_reach)
df_us_all.loc[:,'max_reach'] = pd.to_numeric(df_us_all.max_reach)
df_us_all['Cost ($)'] = pd.to_numeric(df_us_all['Cost ($)'])
df_image = df_image.sort_values('Spend_Range_Max_USD')
df_USA = df_image[(df_image.Geo_Targeting_Included=="United States") & (df_image.Age_Targeting=='Not targeted') & (df_image.Gender_Targeting=='Not targeted')]
df_USA[df_USA["Spend_Range_Max_USD"].isna()] = 10000000
df_USA['mean_cost'] = (df_USA['Spend_Range_Min_USD'] +  df_USA['Spend_Range_Max_USD'])/2

# interpolate lines based on the values of the google ads manager
model =  interpolate.interp1d(df_us_all['Cost ($)'],  df_us_all['min_reach'], fill_value='extrapolate')
df_USA['predicted_lower_impressions'] = model(df_USA['Spend_Range_Min_USD'])
model =  interpolate.interp1d(df_us_all['Cost ($)'],  df_us_all['max_reach'], fill_value='extrapolate')
df_USA['predicted_upper_impressions'] = model(df_USA['Spend_Range_Max_USD'])
df_USA['error'] =  (df_USA['impressions.upper_bound'] -df_USA['impressions.lower_bound'])/2
df_USA['error_cost'] =  (df_USA['Spend_Range_Max_USD'] -df_USA['Spend_Range_Min_USD'])/2
df_USA['mean_impressions'] = (df_USA['impressions.lower_bound'] +  df_USA['impressions.upper_bound'])/2

# find which values fall within the predicted intervals and which not
df_USA_reduced = df_USA[(df_USA['predicted_upper_impressions'] < df_USA['impressions.lower_bound']) | (df_USA['predicted_lower_impressions'] > df_USA['impressions.upper_bound'])]
df_USA_within = df_USA[~((df_USA['predicted_upper_impressions'] < df_USA['impressions.lower_bound']) | (df_USA['predicted_lower_impressions'] > df_USA['impressions.upper_bound']))]

# plot predicted & actual values
fig, ax = plt.subplots(figsize=(3,3.5))
lines = ['--' , ':']
labels = ['min predicted reach', 'max predicted reach']
for idx, name in enumerate(['min_reach','max_reach']):
    ax.plot(df_us_all['Cost ($)'],df_us_all[name],lines[idx], color = 'black', label=labels[idx] )
ax.errorbar(df_USA_reduced['mean_cost'], df_USA_reduced['mean_impressions'] , df_USA_reduced['error'], df_USA_reduced['error_cost'], color='#CC6677', label = 'unexplainable targeting', fmt="o")
ax.errorbar(df_USA_within['mean_cost'], df_USA_within['mean_impressions'] , df_USA_within['error'], df_USA_within['error_cost'], color='#88CCEE', label = 'plausible targeting', fmt="o")
# make error-boxes
df_r = df_USA_reduced[['mean_cost','mean_impressions','error','error_cost']].drop_duplicates()
df_w = df_USA_within[['mean_cost','mean_impressions','error','error_cost']].drop_duplicates()
makeErrorBoxes(df_r['mean_cost'].to_numpy(),df_r['mean_impressions'].to_numpy(), df_r['error_cost'].to_numpy(),df_r['error'].to_numpy(),fc='#CC6677',alpha=0.5)
makeErrorBoxes(df_w['mean_cost'].to_numpy(),df_w['mean_impressions'].to_numpy(), df_w['error_cost'].to_numpy(),df_w['error'].to_numpy(),fc='#88CCEE',alpha=0.5)
# add extra information
ax.set_xlim(1,1000000)
4/len(df_USA)
2/len(df_USA)
ax.text(25500,55000, " 0.07%")
46/len(df_USA)
ax.text(50,550000, " 1.7%")
14/len(df_USA)
ax.text(550,5000, " 0.5%")
5/len(df_USA)
ax.text(550,5500000, " 0.2%")
ax.set_xlabel("Cost ($)")
ax.set_ylabel("Nr of Impressions")
ax.loglog()
ax.legend(loc='best')
fig.tight_layout()
ax.get_legend().remove()
#ax.set_title("Explainability of political image ads on google \n Ad parameters: Total US - All Genders/Ages")
fig.savefig('g_all.png')


#####################################################################################################
# load data collected from the google ads manager for YouTube ads placed in PA, age 25-34
df_manager = pd.read_csv("google_video_cost_reach.csv",sep="\t")
#format data
df_manager["min_reach"] = df_manager.Reach.apply(lambda x: x.split("-")[0])
df_manager["max_reach"] = df_manager.Reach.apply(lambda x: x.split("-")[1])
df_pa_25_34 = df_manager[df_manager.Age=="25-34"]
df_pa_25_34['Cost ($)'] = pd.to_numeric(df_pa_25_34['Cost ($)'])
df_pa_25_34['max_reach'] = pd.to_numeric(df_pa_25_34['max_reach'])
df_pa_25_34['min_reach'] = pd.to_numeric(df_pa_25_34['min_reach'])
df_pa_25_34_ads = df_video[(df_video.Geo_Targeting_Included=='Pennsylvania') & (df_video.Gender_Targeting=='Female') & (df_video.Age_Targeting=="25-34")]
df_pa_25_34_ads['error'] =  (df_pa_25_34_ads['impressions.upper_bound'] -df_pa_25_34_ads['impressions.lower_bound'])/2
df_pa_25_34_ads['error_cost'] =  (df_pa_25_34_ads['Spend_Range_Max_USD'] -df_pa_25_34_ads['Spend_Range_Min_USD'])/2

# interpolate lines based on the values of the google ads manager
model =  interpolate.interp1d(df_pa_25_34['Cost ($)'],  df_pa_25_34['min_reach'], fill_value='extrapolate')
df_pa_25_34_ads['predicted_lower_impressions'] = model(df_pa_25_34_ads['Spend_Range_Min_USD'])
model =  interpolate.interp1d(df_pa_25_34['Cost ($)'],  df_pa_25_34['max_reach'], fill_value='extrapolate')
df_pa_25_34_ads['predicted_upper_impressions'] = model(df_pa_25_34_ads['Spend_Range_Max_USD'])
df_pa_25_34_ads['mean_cost'] = (df_pa_25_34_ads['Spend_Range_Min_USD'] +  df_pa_25_34_ads['Spend_Range_Max_USD'])/2
df_pa_25_34_ads['mean_impressions'] = (df_pa_25_34_ads['impressions.lower_bound'] +  df_pa_25_34_ads['impressions.upper_bound'])/2

# find which values fall within the predicted intervals and which not
df_pa_25_34_ads_reduced = df_pa_25_34_ads[(df_pa_25_34_ads['predicted_upper_impressions'] < df_pa_25_34_ads['impressions.lower_bound']) | (df_pa_25_34_ads['predicted_lower_impressions'] > df_pa_25_34_ads['impressions.upper_bound'])]
df_pa_25_34_ads_within = df_pa_25_34_ads[~((df_pa_25_34_ads['predicted_upper_impressions'] < df_pa_25_34_ads['impressions.lower_bound']) | (df_pa_25_34_ads['predicted_lower_impressions'] > df_pa_25_34_ads['impressions.upper_bound']))]



# plot predicted & actual values
fig, ax = plt.subplots(figsize=(7,5))
lines = ['--' , ':']
labels = ['min predicted reach', 'max predicted reach']
for idx, name in enumerate(['min_reach','max_reach']):
    ax.plot(df_pa_25_34['Cost ($)'],df_pa_25_34[name],lines[idx], color = 'black', label=labels[idx] )

ax.errorbar(df_pa_25_34_ads_reduced['mean_cost'], df_pa_25_34_ads_reduced['mean_impressions'] , df_pa_25_34_ads_reduced['error'], df_pa_25_34_ads_reduced['error_cost'], color='#CC6677', label = 'unexplainable targeting', fmt="o")
ax.errorbar(df_pa_25_34_ads_within['mean_cost'], df_pa_25_34_ads_within['mean_impressions'] , df_pa_25_34_ads_within['error'], df_pa_25_34_ads_within['error_cost'], color='#88CCEE', label = 'plausible targeting', fmt="o")
ax.set_xlim(1,1000000)
ax.text(500,5000, "  13%")
# make error-boxes
df_r = df_pa_25_34_ads_reduced[['mean_cost','mean_impressions','error','error_cost']].drop_duplicates()
df_w = df_pa_25_34_ads_within[['mean_cost','mean_impressions','error','error_cost']].drop_duplicates()
makeErrorBoxes(df_r['mean_cost'].to_numpy(),df_r['mean_impressions'].to_numpy(), df_r['error_cost'].to_numpy(),df_r['error'].to_numpy(),fc='#CC6677',alpha=0.5)
makeErrorBoxes(df_w['mean_cost'].to_numpy(),df_w['mean_impressions'].to_numpy(), df_w['error_cost'].to_numpy(),df_w['error'].to_numpy(),fc='#88CCEE',alpha=0.5)
# add extra information
ax.set_xlabel("Cost ($)")
ax.set_ylabel("Nr of Impressions")
ax.loglog()
ax.legend(loc='best')
fig.tight_layout()
ax.get_legend().remove()
# Put a legend below current axis
#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#          fancybox=True, shadow=True, ncol=5)
ax.set_title("Youtube - Ad parameters: PA - Female, 25-34")
fig.savefig('g_legend1.png')


