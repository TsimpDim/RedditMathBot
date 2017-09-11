import re
import time
import os
import praw
from sympy import Symbol, simplify, solve, diff, limit


def split_args(rootlist):
    '''Split rootlist elemenets on every comma'''

    if not rootlist:
        return -1

    splitted = []
    for i in range(len(rootlist)):
        splitted.append(rootlist[i].split(','))

    return splitted


def store_ids(comments_replied_to):
    '''Store IDs of posts replied to in comments_replied_to.txt'''

    with open("comments_replied_to.txt", "w") as txt_file:
        for comment_id in comments_replied_to:
            txt_file.write(comment_id + "\n")

def reddit_string(text):
    '''Remove markdown formatting from string'''

    return text.replace('*', '\*')

def authenticate():
    '''Authenticate as user using praw.ini'''

    reddit = praw.Reddit('RedditMathBot', user_agent='Simple math bot v1.4')
    print("Authentication as {} successfull".format(reddit.user.me))
    return reddit

def execute(reddit):
    '''Scan comments for problems and solve them'''

    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        comments_replied_to = open("comments_replied_to.txt").read().splitlines()


    for comment in reddit.subreddit('test').comments(limit=25):
        if comment.id not in comments_replied_to:

            #Requests for "Solve" function
            sol_reqs = re.findall(r'!RedditMathBot\|Solve:.\[(.*?)]', comment.body)
            if sol_reqs:
                sol_args = split_args(sol_reqs)#Seperate the args for each call

            #Requests for "Diff" function
            diff_reqs = re.findall(r'!RedditMathBot\|Diff:.\[(.*?)]', comment.body)
            if diff_reqs:
                diff_args = split_args(diff_reqs)

            #Requests for "Limit" function
            limit_reqs = re.findall(r'!RedditMathBot\|Limit:.\[(.*?)]', comment.body)
            if limit_reqs:
                limit_args = split_args(limit_reqs)



            for i in range(len(sol_reqs)):#Process every "Solve" request
                print("\nFound a math problem")
                print("Trying to process comment", comment.body, "...")

                try:
                    exp = sol_args[i][0]#The expression
                    variable = sol_args[i][1]#The variable to solve for
                    print("Expression to solve:", exp)
                    print("Variable to solve for:", variable)

                    x = Symbol(variable)

                    result = reddit_string(str(simplify(solve(exp, x))))
                    print("Solution :", result)
                    comment.reply("Solution to '"+reddit_string(str(exp))+ "': "+ result)
                except:
                    print("Something went wrong, check the syntax")


                if comment.id not in comments_replied_to:
                    comments_replied_to.append(comment.id)


            for i in range(len(diff_reqs)): #Differentiate an expression
                print("\nFound a math problem")
                print("Trying to process comment", comment.body, "...")


                try:
                    exp = diff_args[i][0] #The expression
                    variable = diff_args[i][1] #The variable to solve for
                    times = diff_args[i][2] #How many times to diff
                    print("Differentiate exp :", exp)
                    print("For variable :", variable)
                    print("Times : ", times)

                    x = Symbol(variable)

                    result = reddit_string(str(simplify(diff(exp, x, times))))
                    print("Solution :", result)
                    comment.reply("The derivative of '"+reddit_string(str(exp))+"' ,"+str(times)+" time(s) is : "+result)
                except:
                    print("Something went wrong, check the syntax")


                if comment.id not in comments_replied_to:
                    comments_replied_to.append(comment.id)

            for i in range(len(limit_reqs)): #Find the limit of an expression
                print("\nFound a math problem")
                print("Trying to process comment", comment.body, "...")


                try:
                    exp = limit_args[i][0] #The expression
                    variable = limit_args[i][1]
                    appr = limit_args[i][2]
                    print("Limit of :", exp)
                    print("For variable :", variable)
                    print("Approaching : ", appr)

                    x = Symbol(variable)

                    result = reddit_string(str(limit(exp, variable, appr)))
                    print("Solution :", result)
                    comment.reply("The limit of '"+reddit_string(str(exp))+" ("+str(variable)+"->"+str(appr)+")' is : "+result)
                except:
                    print("Something went wrong, check the syntax")


                if comment.id not in comments_replied_to:
                    comments_replied_to.append(comment.id)

            if "!RedditMathBot|Help" in comment.body:
                print("Found a help request...")
                help_msg = '''Hi! I\'m a simple MathBot for your run of the mill calculus problems.  \n
You can summon me easily by including \'!RedditMathBot|<function>: <arguments>\' in your comment.  \n
The available functions and their corresponding arguments are :  \n
Solve: [<expression>,<variable>]\n
Diff: [<expression>,<variable>,<times_to_diff>]\n
Limit: [<expression>,<variable>,<approaching_value>]'''
                comment.reply(help_msg)

                if comment.id not in comments_replied_to:
                    comments_replied_to.append(comment.id)


            store_ids(comments_replied_to)


    print("\n\nSleeping for 10s...")
    time.sleep(10)


def main():
    ''' Main function '''

    reddit = authenticate()
    while True:
        execute(reddit)


if __name__ == "__main__":
    main()
