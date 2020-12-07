import matplotlib.pyplot as plt
import praw
from settings import USERNAME, PASSWORD, CLIENT_ID, SECRET
import pickle

print(USERNAME, PASSWORD, CLIENT_ID, SECRET)

SUBREDDIT = 'neutralnews'

plt.style.use('ggplot')

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET, username=USERNAME, password=PASSWORD, user_agent="echo-chambers-project by u/phirseudchala")
sub = reddit.subreddit(SUBREDDIT)

num_posts = 0
usernames = []

for submission in sub.hot(limit=1000):
    num_posts += 1
    comments = submission.comments

    for comment in comments:

        if isinstance(comment, praw.models.Comment) and comment.author and comment.author.name not in usernames:
            usernames.append(comment.author.name)

        if isinstance(comment, praw.models.Comment):
            for reply in comment.replies:
                if isinstance(reply, praw.models.Comment) and reply.author and reply.author.name not in usernames:
                    usernames.append(reply.author.name)

for submission in sub.top("month", limit=1000):
    num_posts += 1
    comments = submission.comments

    for comment in comments:

        if isinstance(comment, praw.models.Comment) and comment.author and comment.author.name not in usernames:
            usernames.append(comment.author.name)

        if isinstance(comment, praw.models.Comment):
            for reply in comment.replies:
                if isinstance(reply, praw.models.Comment) and reply.author and reply.author.name not in usernames:
                    usernames.append(reply.author.name)

    if len(usernames) > 20000:
        break

with open(SUBREDDIT + '_usernames.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(usernames, filehandle)

print(len(usernames))
