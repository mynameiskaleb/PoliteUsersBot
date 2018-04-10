import praw
import time

#Configuration options.

#OAuth config. See https://praw.readthedocs.io/en/stable/pages/oauth.html for more info.
#Get a client id and client secret by creating an app on Reddit
clientid = ""
clientsecret = ""
#Leave this empty at first, then run the script. Do the thing on Reddit, then enter the 'code' hex
#key from the 127.0.0.1 url here.
authcode = ""

r = praw.Reddit(user_agent = "A bot to thank users for being nice on reddit created by /u/kooldawgstar")
print("Logging in...")
r.set_oauth_app_info(client_id=clientid,client_secret=clientsecret,redirect_uri='http://127.0.0.1:65010/authorize_callback')
if authcode == "":
    url = r.get_authorize_url('uniqueKey', 'identity read submit', True)
    print("URL: "+url)
    exit(0)
access_information = r.get_access_information(authcode)
r.set_access_credentials(**access_information)

words_to_match = ['Please', 'thank you', 'You are welcome', 'May I', 'Excuse me', 'Pardon me', 'sorry', 'thanks ', ' thanks']
cache = []

nice = len(cache)

def run_bot():
    print("Grabbing subreddits...")
    subreddit = r.get_subreddit("all")
    comments = subreddit.get_comments(limit=25)
    print("Grabbing comments...")
    for comment in comments:
        comment_text = comment.body.lower()
        isMatch = any(string in comment_text for string in words_to_match)
        if comment.id not in cache and isMatch:
            print("Match found! Comment ID: " + comment.id)
            comment.reply("Thank you for being a polite user on reddit! \n\n*This bot was created by [kooldawgstar](http://reddit.com/u/kooldawgstar), if this bot is an annoyance to your subreddit feel free to ban it. [Fork me on Github](http://www.github.com/kooldawgstar/PoliteUsersBot) For more information check out /r/Polite_Users_Bot!*")
            print("Reply Sucessful")
            cache.append(comment.id)
    print("Comment loop finished, bot sleeping")
    
#Blacklist
def look_at_replies():
    print("Looking at replies")
    for comment in r.get_unread(limit=None):
        command = comment.body.strip().lower()
        if command == "stop":
            blacklist.append(comment.author.name)
            comment.reply("You have been blacklisted!")
            print("User Blacklisted")
            r.message.mark_as_read()
        except:
            pass
        
#Delete Downvoted Comments
def delete_downvoted_comments():
    if comment.score < 1:
        try:
            comment.delete()
            print("Comment Deleted")
        except:
            pass
while True:
    try:
        run_bot()
        look_at_replies()
        delete_downvoted_comments()
        time.sleep(60)
    except:
        pass
