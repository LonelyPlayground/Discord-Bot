from random import *
class Gamble:

    #users can roll between numbers
    def roll(self, args):
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
            return "Usage: #roll <minimum whole number> <maximum whole number>"
        #try to convert to int, if not a number yell at them
        try:
            minimum = int(minimum)
            maximum = int(maximum)
        except:
            return "Usage: #roll <minimum whole number> <maximum whole number>"
        #make sure the minimum is smaller
        if minimum >= maximum:
            return "Usage: #roll <minimum whole number> <maximum whole number>"
        #and roll!
        return "Roll between {} and {}, you rolled: {}".format(minimum, maximum, randint(minimum, maximum))