import praw
import re as regex
import time
from sympy import *


def RedditFriendlyString(string):
    return string.replace('*','\*')

def Authenticate():
    reddit = praw.Reddit('RedditMathBot',user_agent='Simple math bot v1.0')
    print("Authentication as {} successfull".format(reddit.user.me))
    return reddit

def Execute(reddit):
    for comment in reddit.subreddit('test').comments(limit = 25):
        if("!RedditMathBot|Solve:" in comment.body): #Solve an equation
            print("Found a math problem")
            com = comment.body.split("Solve: ",1)[1] #Seperate the arguements
      
            print("\nTrying to process...")
            exp = str.strip(regex.search( r'\[(.*?),' , com).group(1)) #The expression
            variable = str.strip(regex.search( r',(.*?)\]', com).group(1)) #The variable to solve for
            print("\nExpression to solve:",exp)
            print("\nVariable to solve for:",variable)

            
            x = Symbol(variable)
            result = solve(exp,x)
            print("Solution :",result)
            if(result != []):
                reply_message = ''.join((str(e)+' ') for e in result)
            else:
                reply_message = 'Could not find a solution.. :\'('
                comment.reply(reply_message)  
                print("Replied with : ",reply_message)

        elif("!RedditMathBot|Diff:" in comment.body): #Differentiate an expression
            print("Found a math problem")
            com = comment.body.split("Diff: ",1)[1] #Seperate the arguements
            
            print("\nTrying to process...")
            exp = str.strip(regex.search( r'\[(.*?),' , com).group(1)) #The expression
            variable = str.strip(regex.search( r',(.*?),', com).group(0))[1] #The variable to solve for
            times = str.strip(regex.search( r',[0-9]\]',com).group(0))[1] #How many times to diff
            print("\nDifferentiate exp :",exp)
            print("\nFor variable :",variable)
            print("\nTimes : ",times)

            x = Symbol(variable)
            result = RedditFriendlyString(simplify(diff(exp,x,times)))
            print("Solution :",result)
            
            comment.reply(result)


    print("Sleeping for 10s...")
    time.sleep(10)


def main():
    reddit = Authenticate()
    while(True):
        Execute(reddit)


if __name__ == "__main__":
    main()