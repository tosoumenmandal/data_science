import matplotlib.pyplot as plt
import pandas as pd

#%matplotlib inline
%config InlineBackend.figure_format = 'svg' 
plt.style.use('fivethirtyeight')

# Reading in current data from coinmarketcap_06012018.csv
current = pd.read_csv("coinmarketcap_06012018.csv")
print(current.head)

# Reading coinmarketcap_06122017.csv into pandas
dec6 = pd.read_csv("coinmarketcap_06122017.csv")
#print(dec6.columns)

# Selecting the 'id' and the 'market_cap_usd' columns
market_cap_raw = dec6.loc[:,['id','market_cap_usd']]
print("Count: "+ str(market_cap_raw.count))

# Filtering out rows without a market capitalization
#cap = market_cap_raw.query('market_cap_usd > 0')
cap = market_cap_raw[market_cap_raw['market_cap_usd'] > 0]

print(cap.count)

#Declaring these now for later use in the plots
TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

# Selecting the first 10 rows and setting the index
cap10 = cap.loc[0:9,].set_index('id')
#print(cap['market_cap_usd'].sum())

# Calculating market_cap_perc
cap10 = cap10.assign(market_cap_perc= lambda x: (x/cap['market_cap_usd'].sum())*100)

# Plotting the barplot with the title defined above 
ax= cap10.plot.bar('market_cap_perc', title=TOP_CAP_TITLE)

# Annotating the y axis with the label defined above
ax.set_ylabel(TOP_CAP_YLABEL)

# Colors for the bar plot
COLORS = ['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver', 'orange', 'red', 'green']

# Plotting market_cap_usd as before but adding the colors and scaling the y-axis  
ax = cap10.plot.bar('market_cap_usd', title=TOP_CAP_TITLE, color=COLORS, log=True)

# Annotating the y axis with 'USD'
# ... YOUR CODE FOR TASK 5 ...
ax.set_ylabel('USD')

# Removing the xlabel as it is not very informative
ax.set_xlabel('')
ax.axes.get_xaxis().set_visible(False)

#print(dec6.columns)
# Selecting the id, percent_change_24h and percent_change_7d columns
volatility = dec6.loc[:, ['id', 'percent_change_24h','percent_change_7d']]

# Setting the index to 'id' and dropping all NaN rows
volatility = volatility.dropna().set_index('id')

# Sorting the DataFrame by percent_change_24h in ascending order
volatility = volatility.sort_values(['percent_change_24h'], ascending= [True])
#volatility = volatility.sort_values(['percent_change_24h', 'percent_change_7d'], ascending=[True, False])

print(volatility.head)

#Defining a function with 2 parameters, the series to plot and the title
def top10_subplot(volatility_series, title):
    # Making the subplot and the figure for two side by side plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    
    # Plotting with pandas the barchart for the top 10 losers
    ax= volatility_series[:10].plot.bar(ax=axes[0], color='darkred')
    
    # Setting the figure's main title to the text passed as parameter
    # ... YOUR CODE FOR TASK 7 ...
    fig.suptitle(title)
    # Setting the ylabel to '% change'
    # ... YOUR CODE FOR TASK 7 ...
    ax.set_ylabel('% change')
    # Same as above, but for the top 10 winners
    ax = volatility_series[-10:].plot.bar(ax=axes[1], color='darkblue')
    
    # Returning this for good practice, might use later
    return fig, ax

DTITLE = "24 hours top losers and winners"

# Calling the function above with the 24 hours period series and title DTITLE  
fig, ax = top10_subplot(volatility['percent_change_24h'], title=DTITLE)

# Sorting in ascending order
volatility7d = volatility.sort_values(['percent_change_7d'], ascending=[True])

WTITLE = "Weekly top losers and winners"

# Calling the top10_subplot function
fig, ax = top10_subplot(volatility7d['percent_change_7d'], title=WTITLE)

# Selecting everything bigger than 10 billion 
#largecaps = cap[cap['market_cap_usd'] > 10**10]
largecaps = cap.query('market_cap_usd > 10**10')

print(largecaps)

# Making a nice function for counting different marketcaps from the
# "cap" DataFrame. Returns an int.
# INSTRUCTORS NOTE: Since you made it to the end, consider it a gift :D
def capcount(query_string):
    return cap.query(query_string).count().id

# Labels for the plot
LABELS = ["biggish", "micro", "nano"]

# Using capcount count the biggish cryptos
biggish = capcount('market_cap_usd> 300*10**6')

# Same as above for micro ...
micro = capcount('market_cap_usd>= 50*10**6 and market_cap_usd< 300*10**6')

# ... and for nano
nano =  capcount('market_cap_usd < 50*10**6')

# Making a list with the 3 counts
values = [biggish, micro, nano]