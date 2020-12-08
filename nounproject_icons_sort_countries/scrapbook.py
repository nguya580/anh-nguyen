# %%

import pandas as pd
import numpy as np

import json

import requests
from requests_oauthlib import OAuth1

# %%

auth = OAuth1("Insert-Key", "Insert-Secret")
endpoint = "http://api.thenounproject.com/icons/food?&limit=50"

response = requests.get(endpoint, auth=auth)

data = response.content

print(data)

# %%

# Load the JSON to a Python list & dump it back out as formatted JSON
data = json.loads(data)
data

uploaders = []

for icon in data['icons']:
    uploaders.append(icon['uploader'])

uploaders

# %%

df = pd.DataFrame(uploaders)

pd.set_option('display.max_rows', 60)

df

# %% clean data from empty country vals

# replace any empty strings in the 'location' column with np.nan objects
df['location'].replace('', np.nan, inplace=True)

# drop the null values:
df.dropna(subset=['location'], inplace=True)

df

# %% sort countries column

#if need extract first 2 chars from each user
df['country_code'] = df.location.str[-2:]
df.sort_values(by='country_code', ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)

df['country_code'].value_counts()

# %%
# create a list of our conditions
conditions = [
    (df['country_code'] == 'GB'),
    (df['country_code'] == 'US'),
    (df['country_code'] == 'FR'),
    (df['country_code'] == 'IN'),
    (df['country_code'] == 'PK'),
    (df['country_code'] == 'MX'),
    (df['country_code'] == 'RU'),
    (df['country_code'] == 'CH'),
    (df['country_code'] == 'EG'),
    (df['country_code'] == 'TH'),
    (df['country_code'] == 'IR'),
    (df['country_code'] == 'CA'),
    (df['country_code'] == 'TR'),
    (df['country_code'] == 'BR'),
    (df['country_code'] == 'ES'),
    (df['country_code'] == 'DE'),
    (df['country_code'] == 'AU'),
    (df['country_code'] == 'IT'),
    (df['country_code'] == 'BG'),
    ]

# create a list of the values we want to assign for each condition
values = ['🇬🇧', '🇺🇸', '🇫🇷', '🇮🇳', '🇵🇰', '🇲🇽', '🇷🇺', '🇨🇭', '🇪🇬', '🇹🇭', '🇮🇷', '🇨🇦', '🇹🇷', '🇧🇷', '🇪🇸', '🇩🇪', '🇦🇺', '🇮🇹', '🇧🇬']

df['country_emoji'] = np.select(conditions, values)

df

# %% write json

df.to_csv('nounproject_countries.csv')
