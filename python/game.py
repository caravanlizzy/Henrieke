#%%
import random 
import numpy as np
from collections import Counter

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = [i for i in range(11)]
        self.crowns = 0
        self.strategy = "random"
        self.aimodel = None

    def playcard(self, game = None, card = 0):
        if self.strategy == "random":
            card = random.choice(self.cards)
        elif self.strategy == "human":
            card = self.getcardinput()
            print(card)
        elif self.strategy == "trainai":
            pass
        elif self.strategy == "bea":
            if game.round == 0:
                card = 0
            elif game.round == 1:
                card = random.choice([0, 4])
            else:
                card = np.max(self.cards)
        elif self.smodelnametrategy == "niklas":
            if np.random.random() < 0.25:
                card = 1
            else:
                card = 0
        elif self.strategy == "henrieke":
            if game.round < 2:
                card = 0
            elif game.round == 2:
                card = 7
            else:
                card = np.max(self.cards)
        elif self.strategy == "auswegslos":
            if game.round < 4:
                card = 0
            elif game.round == 4:
                card = 0
            else:
                card = np.max(self.cards)
        elif self.strategy == "ai":
            modelin = game.gamestatetoaiinput()
            modelout = self.aimodel(modelin)[0]
            card = np.argmax(modelout)
            if card not in self.cards:
                card = random.choice(self.cards)
        return card 

    

    def getcardinput(self):
        card = -1
        while card not in self.cards:
            print("Choose a card! Your cards are: " + str(self.cards))
            card = int(input())
        else:
            return card
            
    def removehighestcards(self, amount = 1):
        for i in range(amount):
            if(self.cards[-1] != 0):
                self.cards.pop()

    def removecard(self, card):
        index = self.cards.index(card)
        if(self.cards[index] != 0):
            self.cards.pop(index)
        

    def addcrown(self):
        self.crowns += 1
    
    def changename(self, newname):
        self.name = newname

    def reset(self):
        self.cards = [i for i in range(11)]
        self.crowns = 0

class Game:
    def __init__(self):
        self.players = []
        self.crownstowin = 2
        self.round = 0
        self.verbose = False
        self.trainai = False
        self.gamestate = "idle"

    def addplayer(self, name, human = False):
        player = Player(name)
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


    def runround(self, cards = [0]*9):
        self.round += 1 
        playedcards = cards[:len(self.players)]
        for i, player in enumerate(self.players): 
            if(player.strategy != "trainai"):
                playedcards[i] = player.playcard(game = self) # play card according to strategy
            else:
                if cards[i] not in player.cards: # ai uses the card that is passed in cards
                    self.gamestate = "abort"
        roundresults = self.getroundresults(playedcards) # evaluate round
        self.updateplayers(roundresults, playedcards) # update player cards and crowns
        self.checkwin()
        return roundresults

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
            else:
                newplayer = Player("tie") # workaround to have a pseudo winner in case of a tie
                return newplayer




# %%
