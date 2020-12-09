# Comments ranking between gated and un-gated method.

This repo is an experiment to test if AI does play a role in filtering comments with toxicity on journalism news website.

I tested between two sets of comment on the same video. The video is published on the New York Times website which has gated comments, and their Youtube channel which has un-gated comments.

To read more about my experiment and project about the comment section in journalism, [click here.](https://www.notion.so/MS-1-Idea-in-Form-Part-3-359fedfc6a25465dbbc89240325560b6)

Please feel free to test out the code on your own. You will need to generate **your own API keys** from Google and The New York Times.

## The libraries I used:

- Pandas
- Numpy
- Request
- Json
- [Perspective API](https://www.perspectiveapi.com/#/start)
- [Youtube API](https://developers.google.com/youtube/v3)
- [The New York Times API](https://developer.nytimes.com/) (community beta)

## Pseudocode

Import libraries.

Insert API keys.

Set parameters for an API request.

Request for an API response.

Print the response to see the structure of the data.

Access to the wanted piece of data.
	Loop:
		Get all the comments in the data.
		Append to a list of comments.

Print the list of comments.

Use Perspective API to score all comments.

Loop:
	For every score in the comments:
		Get summary score value for each comment.
		Append summary score value into a list.

Match comments and summary scores in a dict.

Create a data frame using Pandas based on the above dict of {comment: score}.

Create a condition and value lists to rank comments based on the summary score within the data frame.

Create a new column of priority base on the condition and value lists.

Sort the data frame from high to low order.

.value_count() data frame to see totals of each comment rank.

Export as CSV file for record and presentation in Major Studio 1 class.
