import matplotlib.pyplot as plt
import praw
from settings import USERNAME, PASSWORD, CLIENT_ID, SECRET

print(USERNAME, PASSWORD, CLIENT_ID, SECRET)

SUBREDDIT = 'politics'
NUM_SOURCES = 20
COLOR = 'magenta'

plt.style.use('ggplot')

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET, username=USERNAME, password=PASSWORD, user_agent="echo-chambers-project by u/phirseudchala")
sub = reddit.subreddit(SUBREDDIT)

num_posts = 0
list_of_websites = {}
common_websites = ['www.archive.is', 'www.youtube.com', 'www.youtu.be', 'www.i.redd.it', 'www.imgur.com', 'www.reddit.com', 'www.i.imgur.com', 'www.twitter.com', 'www.v.redd.it']

for submission in sub.top("month", limit=1000):
    num_posts += 1
    url = submission.url # get the url for that submission if it exists
    #get the top level domain
    tld = url.split('/')[2]

    if 'www' not in tld:
        tld = 'www.' + tld


    if tld not in common_websites:
        if tld not in list_of_websites:
            list_of_websites[tld] = 1
        else:
            list_of_websites[tld] += 1

list_of_websites = ({k: v for k, v in sorted(list_of_websites.items(), key=lambda item: item[1])})
top_websites = list(list_of_websites.keys())[-NUM_SOURCES:]
top_frequency = list(list_of_websites.values())[-NUM_SOURCES:]

x_pos = [i for i, _ in enumerate(top_websites)]

plt.bar(x_pos, top_frequency, color=COLOR)
plt.xlabel('Source')
plt.ylabel('Frequency')

plt.title("Top " + str(NUM_SOURCES) + " Sources for r/" + SUBREDDIT)

plt.xticks(x_pos, top_websites)

plt.xticks(
    rotation=45,
    horizontalalignment='right',
    fontweight='light',
    fontsize='x-small'
)

plt.tight_layout()
print('total number of posts - ' + str(num_posts) + '\n')

for i, website in enumerate(top_websites):
    print(website, top_frequency[i])

plt.show()
