# %% import

import json
import requests
import pandas as pd
import numpy as np

# %% api key

from googleapiclient.discovery import build

api_key = "AIzaSyDWc4ktKubB1pDD2QnNDERmu17T-iKSGK4"

# create a service with specific request for youtube api from google
youtube = build('youtube', 'v3', developerKey = api_key)

# url for perspective api
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +
    '?key=' + api_key)

# make a request from youtube service
request = youtube.commentThreads().list(
            part = "snippet",
            videoId = "4lg6cZmfpeM",
            maxResults = 25,
            order = "time")

response = request.execute()

# %% code cell

items = response['items']
items

# %% code cell

#parse out the comment text content from api response
comments = []
for i in items:
    comments.append(i['snippet']['topLevelComment']['snippet']['textOriginal'])

print(comments)

# %% codecell

scores = []
for comment in comments:
    data_dict = {
    'comment': {'text': comment},
    'languages': ['en'],
    'requestedAttributes': {'TOXICITY': {}}
    }

    # append every score value into a list
    response = requests.post(url=url, data=json.dumps(data_dict))
    response_dict = json.loads(response.content)
    # response_all = json.dumps(response_dict, indent=2)
    # print(response_all)
    scores.append(response_dict)

# %% codecell
print(scores)

#parse out the score value from scores list
score_values = []
for score in scores:
    score_values.append(score['attributeScores']['TOXICITY']['summaryScore']['value'])

print(score_values)

# %% codecell
#turn comments list and score_values list to a dict
comment_val_dict = dict(zip(comments, score_values))

print(type(comment_val_dict))

# %% codecell

# make dataframe from a dict
df = pd.DataFrame(list(comment_val_dict.items()),columns = ['Comments','Score'])

pd.options.display.max_colwidth = 1000
df

# %% codecell

# create a list of our conditions
conditions = [
    (df['Score'] < 0.1),
    (df['Score'] >= 0.1) & (df['Score'] <= 0.5),
    (df['Score'] > 0.5)
    ]

# create a list of the values we want to assign for each condition
values = ['low', 'medium', 'high']

# create a new column and use np.select to assign values to it using our lists as arguments
df['Priority'] = np.select(conditions, values)

df.sort_values(by='Score', ascending=False, inplace=True)
df

# %% codecell



df['Priority'].value_counts()
