import praw
import re as regex
import time
import os
from sympy import *

def StoreIDs(comments_replied_to):    
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

def RedditFriendlyString(text):
    return text.replace('**','^').replace('*','\*')

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
            if("!RedditMathBot|Solve:" in comment.body): #Solve an equation
                print("\nFound a math problem")
                com = comment.body.split("Solve: ",1)[1] #Seperate the arguements
        
                print("Trying to process comment",com,"...")

                    
                try:
                    exp = str.strip(regex.search( r'\[(.*?),' , com).group(1)) #The expression
                    variable = str.strip(regex.search( r',(.*?)\]', com).group(1)) #The variable to solve for
                    print("Expression to solve:",exp)
                    print("Variable to solve for:",variable)

                    x = Symbol(variable)
                    
                    result = solve(exp,x)
                    print("Solution :",result)
                    comment.reply("Solution : "+str(result))
                except:
                    print("Wrong syntax, aborting...")
                    pass
                
                if(comment.id not in comments_replied_to): comments_replied_to.append(comment.id)

            if("!RedditMathBot|Diff:" in comment.body): #Differentiate an expression
                print("\nFound a math problem")
                com = comment.body.split("Diff: ",1)[1] #Seperate the arguements
                
                print("Trying to process comment",com,"...")


                try:
                    exp = str.strip(regex.search( r'\[(.*?),' , com).group(1)) #The expression
                    variable = str.strip(regex.search( r',(.*?),', com).group(0))[1] #The variable to solve for
                    times = str.strip(regex.search( r',[0-9]\]',com).group(0))[1] #How many times to diff
                    print("Differentiate exp :",exp)
                    print("For variable :",variable)
                    print("Times : ",times)

                    x = Symbol(variable)
                
                    result = RedditFriendlyString(str(simplify(diff(exp,x,times))))
                    print("Solution :",result)
                    comment.reply("The derivative is : "+result)
                except:
                    print("Wrong syntax, aborting...")
                    pass

                if(comment.id not in comments_replied_to): comments_replied_to.append(comment.id)

            if("!RedditMathBot|Limit:" in comment.body): #Find the limit of an expression
                print("\nFound a math problem")
                com = comment.body.split("Limit: ",1)[1] #Seperate the arguements
                
                print("Trying to process comment",com,"...")


                try:
                    exp = str.strip(regex.search( r'(?<=\[)(.*?),' ,com).group(1)) #The expression
                    variable = str.strip(regex.search( r',(.*),', com).group(1))
                    appr = str.strip(regex.search( r',(.*?)\]',com).group(1))[2] #What our variable is approaching -- needs fixing
                    print("Limit of :",exp)
                    print("For variable :",variable)
                    print("Approaching : ",appr)

                    x = Symbol(variable)
                    
                    result = RedditFriendlyString(str(limit(exp,variable,appr)))
                    print("Solution :",result)
                    comment.reply("The limit is : "+result)
                except:
                    print("Wrong syntax, aborting...")
                    pass

                if(comment.id not in comments_replied_to): comments_replied_to.append(comment.id)

            if("!RedditMathBot|Help" in comment.body):
                help_msg = '''Hi! I\'m a simple MathBot for your run of the mill calculus problems.\n\n\nYou can summon me easily by including \'!RedditMathBot|<function>: <arguments>\' in your comment.\n\n\The available functions and their corresponding arguments are :\n\Solve: [<expression>,<variable>]\n\Diff: [<expression>,<variable>,<times_to_diff>] \n\Limit: [<expression>,<variable>,<approaching_value>]'''
                #^^This is not readable, i know. Howver the markdown does not like to cooperate -- i'll look into fixing this
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