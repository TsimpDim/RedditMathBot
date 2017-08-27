import praw
import re as regex
import time
import os
from sympy import *


def SplitArgs(rootlist):
    if(len(rootlist) == 0): return -1

    splitted  = []
    for i in range(len(rootlist)) : splitted.append(rootlist[i].split(',')) 
    return splitted

def StoreIDs(comments_replied_to):    
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

def RedditFriendlyString(text):
    return text.replace('*','\*')

def Authenticate():
    reddit = praw.Reddit('RedditMathBot',user_agent='Simple math bot v1.4')
    print("Authentication as {} successfull".format(reddit.user.me))
    return reddit

def Execute(reddit):
    
    
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        comments_replied_to = open("comments_replied_to.txt").read().splitlines()


    for comment in reddit.subreddit('test').comments(limit = 25):
        if comment.id not in comments_replied_to:

            sol_reqs = regex.findall(r'!RedditMathBot\|Solve:.\[(.*?)]',comment.body) #Requests for "Solve" function
            if(len(sol_reqs) > 0 ): sol_args = SplitArgs(sol_reqs) #Seperate the arguements for each call
            
            diff_reqs = regex.findall(r'!RedditMathBot\|Diff:.\[(.*?)]',comment.body) #Requests for "Diff" function
            if(len(diff_reqs) > 0 ): diff_args = SplitArgs(diff_reqs) 

            limit_reqs = regex.findall(r'!RedditMathBot\|Limit:.\[(.*?)]',comment.body) #Requests for "Limit" function
            if(len(limit_reqs) > 0 ): limit_args = SplitArgs(limit_reqs) 



            for i in range(len(sol_reqs)): #Process every "Solve" request
                print("\nFound a math problem")
                print("Trying to process comment",comment.body,"...")
  
                try:
                    exp = sol_args[i][0]  #The expression
                    variable = sol_args[i][1] #The variable to solve for
                    print("Expression to solve:",exp)
                    print("Variable to solve for:",variable)

                    x = Symbol(variable)
                    
                    result = RedditFriendlyString(str(simplify(solve(exp,x))))
                    print("Solution :",result)
                    comment.reply("Solution : "+result)
                except:
                    print("Something went wrong, check the syntax")
                    pass
                
                if(comment.id not in comments_replied_to): comments_replied_to.append(comment.id)


            for i in range(len(diff_reqs)): #Differentiate an expression
                print("\nFound a math problem")
                print("Trying to process comment",comment.body,"...")


                try:
                    exp = diff_args[i][0] #The expression
                    variable = diff_args[i][1] #The variable to solve for
                    times = diff_args[i][2] #How many times to diff
                    print("Differentiate exp :",exp)
                    print("For variable :",variable)
                    print("Times : ",times)

                    x = Symbol(variable)
                
                    result = RedditFriendlyString(str(simplify(diff(exp,x,times))))
                    print("Solution :",result)
                    comment.reply("The derivative is : "+result)
                except:
                    print("Something went wrong, check the syntax")
                    pass

                if(comment.id not in comments_replied_to): comments_replied_to.append(comment.id)

            for i in range(len(limit_reqs)): #Find the limit of an expression
                print("\nFound a math problem")
                print("Trying to process comment",comment.body,"...")


                try:
                    exp = limit_args[i][0] #The expression
                    variable = limit_args[i][1]
                    appr = limit_args[i][2]
                    print("Limit of :",exp)
                    print("For variable :",variable)
                    print("Approaching : ",appr)

                    x = Symbol(variable)
                    
                    result = RedditFriendlyString(str(limit(exp,variable,appr)))
                    print("Solution :",result)
                    comment.reply("The limit is : "+result)
                except:
                    print("Something went wrong, check the syntax")
                    pass

                if(comment.id not in comments_replied_to): comments_replied_to.append(comment.id)

            if("!RedditMathBot|Help" in comment.body):
                print("Found a help request...")
                help_msg = '''Hi! I\'m a simple MathBot for your run of the mill calculus problems.  \n
You can summon me easily by including \'!RedditMathBot|<function>: <arguments>\' in your comment.  \n
The available functions and their corresponding arguments are :  \n
Solve: [<expression>,<variable>]\n
Diff: [<expression>,<variable>,<times_to_diff>]\n
Limit: [<expression>,<variable>,<approaching_value>]'''
                comment.reply(help_msg)

                if(comment.id not in comments_replied_to): comments_replied_to.append(comment.id)

                
            StoreIDs(comments_replied_to)

            
    print("\n\nSleeping for 10s...")
    time.sleep(10)


def main():
    reddit = Authenticate()
    while(True):
        Execute(reddit)


if __name__ == "__main__":
    main()