import praw
import re as regex
import time
from sympy import *

def Authenticate():
    reddit = praw.Reddit('RedditMathBot',user_agent='Simple math bot v1.0')
    print("Authentication as {} successfull".format(reddit.user.me))
    return reddit

def Execute(reddit):
    for comment in reddit.subreddit('test').comments(limit = 25):
        if("!RedditMathBot|Solve:" in comment.body):
            print("Found a math problem")
            com = comment.body.split("Solve: ",1)[1]
      
            print("\nTrying to process...")
            exp = str.strip(regex.search( r'\[(.*?),' , com).group(1))
            variable = str.strip(regex.search( r',(.*?)\]', com).group(1))
            print("\nExpression to solve:",exp)
            print("\nVariable to solve for:",variable)

            
            x = Symbol(variable)
            result = solve(exp,x)
            print("Solution :",result)
            if(result != []):
                reply_message = ''.join((str(e)+' ') for e in result)
                comment.reply(reply_message)  
                print("Replied with : ",reply_message)
                

    print("Sleeping for 10s...")
    time.sleep(10)


def main():
    reddit = Authenticate()
    while(True):
        Execute(reddit)


if __name__ == "__main__":
    main()