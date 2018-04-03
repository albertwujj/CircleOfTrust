import praw
import time
import pickle

r = praw.Reddit(client_id='YourFace',
                     client_secret='Like enter your stuff here',
                     password='Try this site: https://www.reddit.com/prefs/apps',
                     user_agent='lol',
                     username='AIIDreamNoDrive')


def getAll(comments, verbose=True):
  commentsList = []
  for comment in comments:
    getSubComments(comment, commentsList, verbose=verbose)
  return commentsList

def getSubComments(comment, allComments, verbose=True):
  allComments.append(comment)
  if not hasattr(comment, "replies"):
    replies = comment.comments()
    if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
  else:
    replies = comment.replies
  for child in replies:
    getSubComments(child, allComments, verbose=verbose)


def analyzeFlair(flair):

    print(flair)
    flair = flair.replace(",", "")
    flair = flair.strip()
    flair_arr = flair.split(' ')
    return int(flair_arr[0]), int(flair_arr[1]), len(flair_arr) > 2

def scan_and_send(user):
    flair = r.flair('CircleofTrust', user.name)
    members, joined, betrayer = analyzeFlair(flair)

    if not betrayer and members > 8 and joined > 12 \
            and (time.time() - user.created_utc) / (60 * 60 * 24) > 130 \
            and user.link_karma > 25 and user.comment_karma > 29:
        livingcircle = False
        print("Test living")
        for i in user.submissions.hot(limit=25):
            if str(i.subreddit) == 'CircleofTrust':
                if not submission.link_flair_text is None:

                    break
                else:
                    livingcircle = True
                    break
        if livingcircle:
            send(user)
def send(user):
    if user.name in sent_users:
        print("already sent")
        print(user.name)
    if not user.name in sent_users:
        print("sent")
        print(user.name)
        sent_users.add(user.name)
        #user.message("Key for key?", "mine is [timer](https://www.reddit.com/r/CircleofTrust/comments/891l6w/uaiidreamnodrives_circle/)")
        with open("save.txt", "wb") as fp:
            pickle.dump(sent_users, fp)
        time.sleep(2)

with open("save.txt", "rb") as fp:
    sent_users = pickle.load(fp)

print(sent_users)
sent = 0
sr = r.subreddit('CircleofTrust')
for itr in range(0, 100000):
    total = 0
    betrayed = 0
    awesome = 0
    thread = None
    if itr % 2 == 0:
        thread = sr.hot(limit = 120)
    else:
        thread = sr.rising(limit = 140)
    for submission in thread:
        if submission.author_flair_text:
            flair = submission.author_flair_text
            members, joined, betrayer = analyzeFlair(flair)

            # if not betrayer
            print("a sub")
            if not betrayer:
                user = submission.author
                if members > 8 and joined > 12 \
                and (time.time() - user.created_utc) / (60 * 60 * 24) > 130 \
                and user.link_karma > 25 and user.comment_karma > 29 \
                and submission.link_flair_text is None:
                    send(user)
            j = 0
            for i in getAll(submission.comments):
                #uncomment below line to scan all COMMENTS too
                #scan_and_send(i.author)
                print("")
                j+=1
                if j == 100:
                    break
        total += 1
        if total % 10 == 0 and not betrayed == 0:
            #print("ratio: " + str(awesome/betrayed))
            print(str(sent))
    print("all")
    time.sleep(100)