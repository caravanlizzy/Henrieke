#%%
import random 
from collections import Counter

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = [i for i in range(11)]
        self.crowns = 0
        self.strategy = "random"

    def playcard(self, card = 0):
        if self.strategy == "random":
            card = random.choice(self.cards)
        elif self.strategy == "human":
            card = self.getcardinput()
        elif self.strategy == "ki":
            pass
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
        # self.trainki = False
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
        gameover = self.checkwin()
        while gameover == False:
            self.runround()
            gameover = self.checkwin()
        else:
            if self.verbose:
                print(str(self.findwinner().name) + " wins the game!")
            


    def runround(self, cards):
        self.round += 1 
        playedcards = cards
        for i, player in enumerate(self.players): 
            if(player.strategy != "ki"):
                playedcards[i] = (player.playcard()) # play card according to strategy
            else:
                if cards[i] not in player.cards: # ki uses the card that is passed in cards
                    self.gamestate = "abort"
        roundresults = self.getroundresults(playedcards) # evaluate round
        self.updateplayers(roundresults, playedcards) # update player cards and crowns
        return roundresults
        


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



