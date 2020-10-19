import praw
from psaw import PushshiftAPI
from datetime import datetime
import csv
import time

#########################################################################

# Use pip to install the following two libraries :
#   $ pip install psaw
#   $ pip install praw

# In order for this script to run, you will have to obtain an ID and a SECRET key  from the following website
# <https://www.reddit.com/prefs/apps>

# Scroll to the bottom of this screen and click the button that says :
#   "are you a developer? create an app..."

# For the name, please enter "Comment Scraper"
# Please ensure that "script" is selected for the application category
# For the description, please enter "Search RedditSearch.io for comments that contain a specific string"
# For the redirect uri, please enter "http://localhost:8080"

# Click the "create app" button and look for the following two sections on the following screen
# At the top of the screen, you'll see a section with the following text :
#   personal use script
#   a346ovYDiTKG-h
# Take this random id and copy and paste into the "client_id" property on line 34 of this .py file

# You will also see a line that looks like the following :
#       secret	A-8351aJ2_P9e1Bk69lvgpLxpgk
# Take this random secret and copy and paste into the "client_secret" property on line 35 of this .py file

client_id = "a346ovYDiTKG-h"
client_secret = "A-8351aJ2_P9e1Bk69lvgpLxpgk"
user_agent = "Comment Scraper"

sub_reddit_string = "nyc"
string_to_search_for = "climate change"

#########################################################################

# Create Reddit client
reddit_client = praw.Reddit(client_id=client_id,
                            client_secret=client_secret,
                            user_agent=user_agent)

# Create Pushshift client and obtain comment id's
pushshift_client = PushshiftAPI(reddit_client)
gen_comments = pushshift_client.search_comments(subreddit=sub_reddit_string,
                                                q=string_to_search_for,
                                                limit=None)

# Start timer
start = time.time()
print("\nGathering comments from Pushshift API")

# Create dictionary of all comments retrieved from Pushshift
comments_dict = {}
for comment in gen_comments:
    if comment.id not in comments_dict:
        comments_dict[comment.id] = comment

# Display info via terminal
print("\n{} comments found in r/{} containing the text : {}".format(len(comments_dict), sub_reddit_string,
                                                                    string_to_search_for))

hours, rem = divmod(time.time()-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Time to gather comments: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

file_name = "{}-{}-{}.csv".format(sub_reddit_string,
                                  string_to_search_for,
                                  datetime.now().strftime("%d_%m_%Y-%H_%M_%S"))

# Initialize and open .csv file for data to be written to
with open(file_name, mode='w') as csv_file:
    print("\nGathering comment and post information from Reddit API")
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    search_index = 1
    csv_index = 0

    # Attempt to add comment's info to .csv file
    for comment in comments_dict.values():
        print("\t{} of {}".format(search_index, len(comments_dict)))
        search_index += 1

        try:
            csv_writer.writerow([
                str(datetime.fromtimestamp(comment.submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')),
                str(comment.submission.score),
                str(comment.submission.title),
                str(comment.submission.permalink),
                str(datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')),
                str(comment.score),
                str(comment.body),
                str(comment.permalink)
            ])

            csv_index += 1

        except:
            print("Error writing info to .csv")

    # Display info via terminal
    print("\nFile complete : {}".format(file_name))
    print("\t{} objects in .csv".format(str(csv_index)))

# Display info via terminal
hours, rem = divmod(time.time()-start, 3600)
minutes, seconds = divmod(rem, 60)
print("\nTotal Time : {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
