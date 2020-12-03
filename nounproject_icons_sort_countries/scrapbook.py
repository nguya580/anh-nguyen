# %%

import pandas as pd
import numpy as np

import json

import requests
from requests_oauthlib import OAuth1

# %%

auth = OAuth1("**********", "**********")
endpoint = "http://api.thenounproject.com/icons/food?&limit=50"

response = requests.get(endpoint, auth=auth)

data = response.content

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
df['country code'] = df.location.str[-2:]
df.sort_values(by='country code', ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)

df['country code'].value_counts()

# %%
# create a list of our conditions
conditions = [
    (df['country code'] == 'GB'),
    (df['country code'] == 'US'),
    (df['country code'] == 'FR'),
    (df['country code'] == 'IN'),
    (df['country code'] == 'PK'),
    (df['country code'] == 'MX'),
    (df['country code'] == 'RU'),
    (df['country code'] == 'CH'),
    (df['country code'] == 'EG'),
    (df['country code'] == 'TH'),
    (df['country code'] == 'IR'),
    (df['country code'] == 'CA'),
    (df['country code'] == 'TR'),
    (df['country code'] == 'BR'),
    (df['country code'] == 'ES'),
    (df['country code'] == 'DE'),
    (df['country code'] == 'AU'),
    (df['country code'] == 'IT'),
    (df['country code'] == 'BG'),
    ]

# create a list of the values we want to assign for each condition
values = ['🇬🇧', '🇺🇸', '🇫🇷', '🇮🇳', '🇵🇰', '🇲🇽', '🇷🇺', '🇨🇭', '🇪🇬', '🇹🇭', '🇮🇷', '🇨🇦', '🇹🇷', '🇧🇷', '🇪🇸', '🇩🇪', '🇦🇺', '🇮🇹', '🇧🇬']

df['country emoji'] = np.select(conditions, values)

df

# %% write json

df.to_json('nounproject_countries.json', orient='records', lines=True)
