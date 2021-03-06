import praw
from credentials import *
import time
import nltk
import re
import csv

# If I can process one post in 3.7 seconds, how often do we get a new post?
# There are 37 posts per hour, which means it takes 98 seconds to make a post.
# Holy shit, we make a post every 98 seconds!

# I have to trun 

#I'm just being safe and keeping my credentials in a separate file.
reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret,
                     user_agent = user_agent,
                     username = username,
                     password = password)

OurSubreddit = 'relationships'
                     
#This is how you can check the connection. It should say 'False'.
#print(reddit.read_only)

# This function describes how to create each variable.
def ProcessPost(submission): # Creates the flags for a single post.
    # When we first find a post, we assume it's not a troll.
    Troll = 0
    # I should know the submission's ID.
    LinkID = submission.id
    # The first thing I care about is the spread between the author's age and karma.
    AuthorAge = time.time() - submission.author.created_utc
    AuthorKarma = submission.author.link_karma + submission.author.comment_karma
    AuthorKarmaAgeSpread = AuthorAge - AuthorKarma
    # The next thing I care about is the post's lexical diversity, which is unique words / total words.
    words = []
    for i in submission.selftext.split():
        if i.isalpha() == True:
            words.append(i)
    if len(words)>0:
        LexicalDiversity = len(set(words))/len(words)
    else:
        LexicalDiversity = 0
    # The formatting variable is looking for lists, headers, bolding, italicizing, and horizontal lines.
    HeadersBoldingListsSeparators = re.findall(r'[*#]+\S*',submission.selftext)
    NumberedLists = re.findall(r'\d\.\s+',submission.selftext)
    HyphenListsAndSeparators = re.findall(r'\-+\s+',submission.selftext)
    PlusLists = re.findall(r'\+\s+',submission.selftext)
    formatting = HeadersBoldingListsSeparators + NumberedLists + HyphenListsAndSeparators + PlusLists
    FormattingCount = len(formatting)

    # These criteria were developed by other moderators.
    # This is a measure of how much link karma a redditor has compared to his number of posts. (u/ofthrees)
    posts = []
    for i in submission.author.submissions.new(limit=100):
        posts.append(i)
    KarmaPerPost = submission.author.link_karma/len(posts)

    # This is a measure of how often OP comments in his own thread relative to everyone else. (u/justsomebadadvice)
    OPCommentCounter = 0
    CommentCounter = 0
    OPSelfCommentRate = 0
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        CommentCounter += 1
        if submission.author == comment.author:
            OPCommentCounter += 1
    if CommentCounter != 0:
        OPSelfCommentRate = OPCommentCounter/CommentCounter
    
    # All of this processing gives us a list of traits for the post.
    TheList = [LinkID,Troll,AuthorKarmaAgeSpread,LexicalDiversity,FormattingCount,KarmaPerPost,OPSelfCommentRate]
    return TheList

#This is where I initialize the dictionary that will hold all of the information, and pull older data from the csv file on my computer.
Rows = {}
with open('posts.csv') as posts:
    reader = csv.DictReader(posts)
    for i in reader:
        Rows[i['LinkID']] = [i['Troll'],i['AuthorKarmaAgeSpread'],i['LexicalDiversity'],i['FormattingCount'],i['KarmaPerPost'],i['OPSelfCommentRate']]

# This is where the variables are created.
for i, submission in enumerate(reddit.subreddit(OurSubreddit).hot(limit=30)):
    Rows[ProcessPost(submission)[0]] = ProcessPost(submission)[1:7]

# Moderators flag trolls by selecting the 'Trolling' reason in the modqueue. The bot will remove it and then note the post as a troll.
for item in reddit.subreddit(OurSubreddit).mod.reports(limit=100):
    if len(item.mod_reports) == 1:
        if item.mod_reports[0][0] == 'Trolling':
            if type(item) == praw.models.reddit.comment.Comment:
                item.mod.remove() # Do not uncomment this line until we go live!
##                print("This is a comment.")
            elif type(item) == praw.models.reddit.submission.Submission:
##                print("This is a submission.", item.id)
                Rows[item.id][0] = 1
                item.mod.remove() # Do not uncomment this line until we go live!

# This is the machine learning portion of the program. It's commented out because I want to collect data before making a model.
##from sklearn import tree # Visit http://scikit-learn.org/stable/install.html to learn how to install this package.
##features = []
##labels = []
##for id,item in enumerate(Rows):
##    features.append(Rows[item][1:5])
##    labels.append(Rows[item][0])
##clf = tree.DecisionTreeClassifier()
##clf = clf.fit(features,labels)
##print(clf.predict([[654535, .681535, 4, 2352]])) # This line is just a test of the prediction function.

# I write all of my post data to my csv file.
with open('posts.csv','w') as posts:
    fieldnames = ['LinkID','Troll','AuthorKarmaAgeSpread','LexicalDiversity','FormattingCount','KarmaPerPost','OPSelfCommentRate']
    writer = csv.DictWriter(posts, fieldnames = fieldnames, lineterminator = '\n')
    writer.writeheader()
    for row in Rows:
        writer.writerow({'LinkID':row,'Troll':Rows[row][0],'AuthorKarmaAgeSpread':Rows[row][1],'LexicalDiversity':Rows[row][2],'FormattingCount':Rows[row][3],'KarmaPerPost':Rows[row][4],'OPSelfCommentRate':Rows[row][5]})
