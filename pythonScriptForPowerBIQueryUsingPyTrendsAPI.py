
import pytrends   # A psedo API for google trends data
import pandas as pd
import pytrends
from pytrends.request import TrendReq
pytrend = TrendReq()

"""
We need to be precise on the keywords to avoid ambiguity. 
Pytrends provides a function called pytrend.suggestions that could return several suggestions for a keyword.
Usually, the first suggestion is the most popular one. “mid” column contains those exact keywords we’d like to search.
"""

KEYWORDS=['Bitcoin','Gold','Recession','Ethereum'] # List of keywords to search for in Google Trends data, also don't put words with space here e.g stock USD
KEYWORDS_CODES=[pytrend.suggestions(keyword=i)[0] for i in KEYWORDS] # Fetching suggestions for the keywords to get exact search terms
df_CODES= pd.DataFrame(KEYWORDS_CODES)
df_CODES # Display DataFrame with the 'mid' column which contains the exact keywords

#Setting up the parameters for the pytrends API call

EXACT_KEYWORDS=df_CODES['mid'].to_list() # Extracting exact keywords from the 'mid' column
DATE_INTERVAL='all' # The time interval for which trends data will be fetched
COUNTRY=["US","IN"] #Use this link for iso country code https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes; Here we are choosing US and India as the regions for the search trends of words listed in KEYWORDS
CATEGORY=0 # Category ID for the trend data (0 is for 'all' categories); Use this link to select categories https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
SEARCH_TYPE='' #Type of search (default is 'web searches', others include 'images','news','youtube','froogle')


# Fetching Google Trends data for each keyword, country pair
Individual_EXACT_KEYWORD = list(zip(*[iter(EXACT_KEYWORDS)]*1))
Individual_EXACT_KEYWORD = [list(x) for x in Individual_EXACT_KEYWORD]
dicti = {}
i = 1
for Country in COUNTRY:
    for keyword in Individual_EXACT_KEYWORD:
         # Building the payload for API request
        pytrend.build_payload(kw_list=keyword, 
                              timeframe = DATE_INTERVAL, 
                              geo = Country, 
                              cat=CATEGORY,
                              gprop=SEARCH_TYPE) 
         # Fetching interest over time data
        dicti[i] = pytrend.interest_over_time()
        i+=1
df_trends = pd.concat(dicti, axis=1)

# Cleaning and formatting the fetched data

df_trends.columns = df_trends.columns.droplevel(0) # Dropping the outer header level in column names
df_trends = df_trends.drop('isPartial', axis = 1) # Dropping the "isPartial" column
df_trends.reset_index(level=0,inplace=True) # Resetting the index

# Renaming columns for readability
df_trends.columns=['date','Bitcoin-US','Gold-US','Recession-US','Ethereum-US','Bitcoin-IN','Gold-IN','Recession-IN','Ethereum-IN'] 

