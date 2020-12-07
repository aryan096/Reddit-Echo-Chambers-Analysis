import matplotlib.pyplot as plt
import praw
from settings import USERNAME, PASSWORD, CLIENT_ID, SECRET
import pickle
import random
import numpy as np

# ----------------------------------------------------------------------------

SUBREDDIT = 'neutralnews'
NUMBER_OF_USERS_TO_LOOK_AT = 1000
SHUFFLE = True

# ----------------------------------------------------------------------------

usernames = []

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET, username=USERNAME, password=PASSWORD, user_agent="echo-chambers-project by u/phirseudchala")

political_subreddits = ['politics', 'Conservative', 'worldnews',
                        'news', 'worldpolitics', 'Worldevents', 'business', 'Economics',
                        'environment', 'energy', 'law', 'education', 'government', 'history',
                        'PoliticalPDFs', 'WikiLeaks', 'SOPA', 'worldnews2', 'AnarchistNews',
                        'LGBTnews', 'politics2', 'economics2', 'uspolitics', 'AmericanPolitics',
                        'Libertarian', 'Anarchism', 'socialism', 'progressive', 'americapirateparty',
                        'democrats', 'Liberal', 'new_right', 'Republican', 'egalitarian', 'demsocialist',
                        'LibertarianLeft', 'Liberty', 'Anarcho_Capitalism', 'alltheleft', 'neoprogs',
                        'tea_party', 'voluntarism', 'labor', ' blackflag', 'GreenParty',
                        'democracy', 'IWW', 'Marxism', 'Objectivism', 'LibertarianSocialism',
                        'peoplesparty', 'Capitalism', 'Anarchist', 'feminisms', 'republicans',
                        'Communist', 'socialdemocracy', 'Postleftanarchism', 'RadicalFeminism',
                        'AnarchoPacifism', 'conservatives', 'republicanism', 'Conspiracy',
                        '911truth', 'climatesceptics', 'infograffiti', 'conspiracyhub', 'Liberal',
                        'The_Donald', 'Uncensorednews', 'Neoliberal', 'PoliticalDiscussion', 'WayOfTheBern',
                        'OurPresident', 'SandersForPresident', 'collapse', 'geopolitics', 'ukpolitics',
                        'PoliticalCompassMemes', 'stupidpol', 'Coronavirus']

with open(SUBREDDIT + '_usernames.data', 'rb') as filehandle:
    # read the data as binary data stream
    usernames = pickle.load(filehandle)

num_subreddits = []
count = 0

if SHUFFLE:
    random.shuffle(usernames)

print('starting')

for username in usernames:
    # for each username, we want to get the number of subreddits they have
    # participated in, that means commented in or posted in
    redditor = praw.models.Redditor(reddit,name=username)
    comment_history = redditor.comments.top("month", limit=1000)
    comment_subreddits = {}

    try:
        for comment in comment_history:
            if comment.subreddit in political_subreddits:
                if comment.subreddit in comment_subreddits:
                    comment_subreddits[comment.subreddit] += 1
                else:
                    comment_subreddits[comment.subreddit] = 1
    except:
        continue

    num_subreddits.append(len(comment_subreddits))
    count += 1

    if count > NUMBER_OF_USERS_TO_LOOK_AT:
        break

    print('looking at user ' + str(count) + ' ...')

print('-------------------------------------')
print('   REPORT FOR r/' + SUBREDDIT + '   ')
print('-------------------------------------')
print('average ', np.average(num_subreddits))
print('median ', np.median(num_subreddits))
print('std ', np.std(num_subreddits))
print('---------------------------------')
