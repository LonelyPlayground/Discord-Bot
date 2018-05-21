from random import *

#compilation of active gambling sessions
activeSessions = []

#users can roll between numbers
def rollFunc(args, user):
    global mostRecentRoll
    global activeSessions
    minimum = 0
    maximum = 0
    #no args default to 1-100 elsewise complain about missing/too many args
    if len(args) == 0:
        minimum = 1
        maximum = 100
    elif len(args) == 2:
        minimum = args[0]
        maximum = args[1]
    else:
        return "<@{}> Give me some input here geez or none, that's fine too. #roll <minimum> <maximum>".format(user)
    #try to convert to int, if not a number yell at them
    try:
        minimum = int(minimum)
        maximum = int(maximum)
    except:
        return "<@{}> Really, that's what you want me to roll between? No. #roll <minimum> <maximum>".format(user)
    #make sure the minimum is smaller
    if minimum >= maximum:
        return "<@{}> Minimum<Maximum go back to elementary school. #roll <minimum> <maximum>".format(user)
    #and roll!
    roll = randint(minimum, maximum)
    #contruct the string
    results = "Roll between {} and {}, <@{}> rolled: {}".format(minimum, maximum, user, roll)
    #checking for gambling finishes
    mostRecentRoll = [minimum, maximum, user, roll]
    for i in range(0, len(activeSessions)):
        if activeSessions[i] != -1:
            if activeSessions[i].check_roll(mostRecentRoll):
                results += "\n" + activeSessions[i].finish()
    return results