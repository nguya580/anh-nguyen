# %% importing

# import requests and json
import requests
import json
import pandas as pd
import numpy as np

# %% API key

#API key and setting for the community api
#https://developer.nytimes.com/docs/community-api-product/1/routes/user-content/url.json/get
api_key = "03Q77oAuM8UocuAmO9MwGeuV65h1KQeD"
article_url = "https://www.nytimes.com/2020/10/26/opinion/qanon-conspiracy-donald-trump.html?searchResultPosition=4"
sort = "newest"

# %% calling API

# show the API url with all the settings listed out
api_url = (f"https://api.nytimes.com/svc/community/v3/user-content/url.json?api-key={api_key}&url={article_url}&offset=0")

#test to see if api url is correct
print(api_url)

# %% data request

# calling the API with requests
response = requests.get(api_url)

# creating a variable called data to hold the json formatted result
data = response.json()

data

# %% parsing comment dict within data

comment_data =  data['results']['comments']

#put comment body in a list
comments_body = []
for comment in comment_data:
    comments_body.append(comment['commentBody'])

print (comments_body)

# %% calling Perspective API

perspective_apikey = "AIzaSyDWc4ktKubB1pDD2QnNDERmu17T-iKSGK4"

# url for perspective api
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +
    '?key=' + perspective_apikey)

# %% Testing comments with Perspective API

scores = []

for comment in comments_body:
    data_dict = {
    'comment': {'text': comment},
    'languages': ['en'],
    'requestedAttributes': {'TOXICITY': {}}
    }

    # append every score value into a list
    response = requests.post(url=url, data=json.dumps(data_dict))
    response_dict = json.loads(response.content)
    scores.append(response_dict)

print(scores) #a list of response from perspective api

# %% get the summary score values

#parse out the score value from scores list
score_values = []
for score in scores:
    score_values.append(score['attributeScores']['TOXICITY']['summaryScore']['value'])

print(score_values)

# %% Turn the dict into a data frame

#turn comments list and score_values list to a dict
#This function pairs the list element with other list element at corresponding index in form of key-value pairs.
comment_val_dict = dict(zip(comments_body, score_values)) #dict(zip(keys, values))

print(type(comment_val_dict))
comment_val_dict

# %% Turn the dict into a data frame

# make dataframe from a dict
df = pd.DataFrame(list(comment_val_dict.items()),columns = ['Comments','Score'])

pd.options.display.max_colwidth = 1000
# df

# %% Add a new column based on conditions

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

# sorting from high to low
df.sort_values(by='Score', ascending=False, inplace=True)
#reset index
df.reset_index(drop=True, inplace=True)

df

# %% Count number of each ranks

df['Priority'].value_counts()

# %% save df in a cvs file

df.to_csv('nytimes-comments-ranking.csv')
