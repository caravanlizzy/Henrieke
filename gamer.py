import random 
import numpy as np
from collections import Counter
import player 

class Game:
    def __init__(self):
        self.players = []
        self.crownstowin = 2
        self.round = 0
        self.verbose = False
        self.trainai = False
        self.gamestate = "idle"

    def addplayer(self, name, human = False):
        player = player.Player(name)
        player.game = self
        if human:
            player.strategy = "human"
        self.players.append(player)

    def reset(self):
        self.round = 0
        self.gamestate = "idle"

    def printroundresults(self, roundresults, playedcards):
        print("roundresults:\n")
        for i, p in enumerate(self.players):
            print(str(p.name) + " played: " + str(playedcards[i]) + " - crowns: " + str(self.players[i].crowns))
        print("\n")


    def updateplayers(self, roundresults, playedcards):
        for index, roundresult in enumerate(roundresults):
            if roundresult == "win":
                cards = playedcards[index] - 1 #remove cards - 1 for win
                self.players[index].crowns += 1 #add crown
                self.players[index].removehighestcards(cards)
            elif roundresult == "loss":
                cards = playedcards[index] # remove all cards for loss
                self.players[index].removehighestcards(cards)
            elif roundresult == "tie":
                playedcard = playedcards[index] # remove 1 card for tie
                self.players[index].removecard(playedcard)

        if self.verbose: #print console output
            self.printroundresults(roundresults, playedcards)


    def checkwin(self):
        if self.round > 25:
            self.gamestate = "over"
        for player in self.players:
            if player.crowns >= self.crownstowin:
                self.gamestate = "over"
                return True
        return False 

    def initgame(self):
        self.reset()
        self.gamestate = "running"
        nplayers = len(self.players)
        if nplayers < 2:
            print("Not enough players.")
        elif nplayers == 2:
            self.crownstowin = 3
        else:
            self.crownstowin = 2
        if self.verbose:
            print("Welcome to Henriekow! Good luck.")

    def startgame(self):
        self.initgame()
        if self.trainai:
            return
        while self.gamestate == "running":
            self.runround()
        else:
            if self.verbose:
                print(str(self.findwinner().name) + " wins the game!")
            return self.findwinner()


    def runround(self, cards = [0]*9): #the optional parameter "cards" allow to input specific inputs (i.e. to process ai output )
        self.round += 1 
        playedcards = cards[:len(self.players)]
        for i, player in enumerate(self.players): 
            if(player.strategy != "trainai"):
                playedcards[i] = player.playcard() # play card according to strategy
            else:
                if cards[i] not in player.cards: # ai uses the card that is passed in cards
                    self.gamestate = "abort" #abort for playing an invalid card
        roundresults = self.getroundresults(playedcards) # evaluate round
        self.updateplayers(roundresults, playedcards) # update player cards and crowns
        self.checkwin()
        return roundresults
    
    def getwrongpickcount(self):
        wrongpicks = []
        for player in self.players:
            wrongpicks.append(player.wrongpicks)
        return wrongpicks

    

    def gamestatetoaiinput(self): # function to extract the model input info from the game
        allinputs = []
        for player in self.players:
            # playerinput = []
            for card in range(11):
                if card in player.cards:
                    allinputs.append(1)
                else:
                    allinputs.append(0)
            allinputs.append(player.crowns)
        normedinput = self.normalize(allinputs)
        return np.array([normedinput])


    def normalize(self, inputlist):
        inputs = np.array(inputlist)
        mean = inputs.mean()
        std = inputs.std()
        normed = (inputs - mean)/std
        return normed
        


    def getroundresults(self, playedcards):
        rr = ["loss"] * len(playedcards)
        highestcard = max(playedcards)
        occurence = Counter(playedcards)[highestcard]
        if occurence == 1:
            index = playedcards.index(highestcard)
            rr[index] = "win"
        else:
            for i in range(len(rr)):
                if(playedcards[i] == highestcard):
                    rr[i] = "tie"
        return rr

    def findwinner(self):
        for player in self.players:
            if player.crowns >= self.crownstowin:
                return player
        newplayer = Player("tie") # newplayer stands for a pseudo winner in case of a tie
        return newplayer
