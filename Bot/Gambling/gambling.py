from Gambling.gamblingHelpers import activeSessions
class Gamble:

    def __init__(self):
        self.sessionId = 0
        self.gamblingSession = False
        self.minimum = 0
        self.maximum = 0
        self.people = []
        self.saveStatepeople = []
        self.rolls = []

    def get_sessionId(self):
        return self.sessionId

    def get_rolls(self):
        return self.rolls

    def get_gamblingSession(self):
        return self.gamblingSession

    def joinSession(self):
        for i in range(len(activeSessions) - 1, -1, -1):
            if activeSessions[i] != -1:
                self.sessionId = i + 1
                if i + 1 > len(activeSessions) - 1:
                    activeSessions.append(self)
                else:
                    activeSessions[i + 1] = self
                return
        self.sessionId = 0
        if len(activeSessions) == 0:
            activeSessions.append(self)
        else:
            activeSessions[0] = self
        return


    def gambleStart(self, args, user):
        #no args default to 1-100 elsewise complain about missing/too many args
        if len(args) == 0:
            self.minimum = 1
            self.maximum = 100
        elif len(args) == 2:
            self.minimum = args[0]
            self.maximum = args[1]
        else:
            return "<@{}> Please give either a self.maximum and self.minimum or default to 1-100. #gamble <self.minimum> <self.maximum>".format(user)
        #try to convert to int, if not a number yell at them
        try:
            self.minimum = int(self.minimum)
            self.maximum = int(self.maximum)
        except:
            return "<@{}> Must roll between two numbers. #gamble <self.minimum> <self.maximum>".format(user)
        #make sure the self.minimum is smaller
        if self.minimum >= self.maximum:
            return "<@{}> Self.minimum must be less than self.maximum. #gamble <self.minimum> <self.maximum>".format(user)
        #make sure it's whole numbers
        if self.maximum < 0 or self.minimum < 0:
            return "<@{}> Must roll between positive numbers. #gamble <self.minimum> <self.maximum>".format(user)
        #session has started
        self.gamblingSession = True
        self.people = [user]
        self.rolls = [-1]
        #adds itself to active sessions with id
        self.joinSession()
        return "<@{}> has started a gambling session with id {} with self.rolls between {} and {}, type #join {} to join this session".format(user, self.sessionId, self.minimum, self.maximum, self.sessionId)

    def join(self, user):
        if not self.gamblingSession:
            return "This is no longer an active session wait till self.rolls are done or start a new one!"
        newUser = True
        for person in self.people:
            if person == user:
                newUser = False
        if newUser:
            self.people.append(user)
            self.rolls.append(-1)
        else:
            return "<@{}> was already registered for gambling session {}".format(user, self.sessionId)
        return "<@{}> has joined gambling session {} and will roll between {} and {} when called".format(user, self.sessionId, self.minimum, self.maximum)


    def start_roll(self):
        self.gamblingSession = False
        self.saveStatepeople = []
        for person in self.people:
            self.saveStatepeople.append(person)
        return "Joining halted. Everyone who joined roll now!"


    def finish(self):
        activeSessions[self.sessionId] = -1
        users = self.saveStatepeople
        highUser = 0
        highest = self.minimum - 1
        lowUser = 0
        lowest = self.maximum + 1
        for i in range(0, len(self.rolls)):
            if self.rolls[i] > highest:
                highest = self.rolls[i]
                highUser = users[i]
            if self.rolls[i] < lowest:
                lowest = self.rolls[i]
                lowUser = users[i]
        return "<@{}> owes <@{}> {}".format(lowUser, highUser, highest - lowest)


    def check_roll(self, mostRecentRoll):
        if not self.gamblingSession:
            if mostRecentRoll[0] == self.minimum and mostRecentRoll[1] == self.maximum:
                for i in range(0, len(self.people)):
                    if self.people[i] == mostRecentRoll[2]:
                        self.rolls[i] = mostRecentRoll[3]
                        self.people[i] = -1
        done = True
        for roll in self.rolls:
            if roll == -1:
                done = False
        return done