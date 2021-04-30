import random 
import numpy as np
from collections import Counter
import player

class Game:
    def __init__(self):
        self.players = []
        self.crownsToWin = 2
        self.round = 0
        self.verbose = False
        self.trainAi = False
        self.gameState = "idle"
        self.showGames = False
        # self.wrongpickpercentage = 0 #for now only working with 1 ai being trained

    def addPlayer(self, name, strategy = "randomBot", aiModel = False):
        newPlayer = player.Player(name)
        newPlayer.game = self  
        newPlayer.strategy = strategy
        self.players.append(newPlayer)

    def addAi(self, name, model):
        ai = player.Player("ai")
        ai.game = self
        ai.strategy = "ai"
        ai.loadModel(model)
        self.players.append(ai)

    def reset(self):
        self.round = 0
        self.gameState = "idle"

    def printroundResults(self, roundResults, playedCards):
        print("Roundresults:\n")
        for i, p in enumerate(self.players):
            print(str(p.name) + " played: " + str(playedCards[i]) + " - crowns: " + str(self.players[i].crowns))
        print("\n")

    def updatePlayers(self, roundResults, playedCards):
        for index, roundResult in enumerate(roundResults):
            if roundResult == "win":
                cards = playedCards[index] - 1 #remove cards - 1 for win
                self.players[index].crowns += 1 #add crown
                self.players[index].removeHighestCards(cards)
            elif roundResult == "loss":
                cards = playedCards[index] # remove all cards for loss
                self.players[index].removeHighestCards(cards)
            elif roundResult == "tie":
                playedCard = playedCards[index] # remove 1 card for tie
                self.players[index].removeCard(playedCard)

        if self.verbose: #print console output
            self.printroundResults(roundResults, playedCards)

    def checkWin(self):
        if self.round > 25:
            self.gameState = "over"
        for player in self.players:
            if player.crowns >= self.crownsToWin:
                self.gameState = "over"
                return True
        return False 

    def initGame(self):
        self.reset()
        self.gameState = "running"
        nPlayers = len(self.players)
        if nPlayers < 2:
            print("Not enough players.")
        elif nPlayers == 2:
            self.crownsToWin = 3
        else:
            self.crownsToWin = 2
        if self.verbose:
            print("Welcome to Henriekow! Good luck.")

    def startGame(self): #return value is a bad choice for now
        self.initGame()
        if self.trainAi:
            return
        while self.gameState == "running":
            self.runRound()
        else:
            if self.verbose:
                print(str(self.findWinner().name) + " wins the game!")
            return self.findWinner()

    def runRound(self, cards = [0]*9): # play a complete round, (each player plays 1 card), the optional parameter "cards" allow to input specific inputs (i.e. to process ai output )
        self.round += 1 
        playedCards = cards[:len(self.players)]
        for i, player in enumerate(self.players): 
            if(player.strategy != "trainAi"):
                playedCards[i] = player.playCard() # play card according to strategy
            else:
                if cards[i] not in player.cards: # ai uses the card that is passed in cards
                    self.gameState = "abort" #abort for playing an invalid card
        roundResults = self.getroundResults(playedCards) # evaluate round
        self.updatePlayers(roundResults, playedCards) # update player cards and crowns
        self.checkWin()
        return roundResults

    def gameStateToAiInput(self): # function to extract the model input info from the game
        allInputs = []
        for player in self.players:
            # playerinput = []
            for card in range(11):
                if card in player.cards:
                    allInputs.append(1)
                else:
                    allInputs.append(0)
            allInputs.append(player.crowns)
        normedinput = self.normalize(allInputs)
        return np.array([normedinput])

    def normalize(self, inputList):
        inputs = np.array(inputList)
        mean = inputs.mean()
        std = inputs.std()
        normed = (inputs - mean)/std
        return normed

    def getroundResults(self, playedCards):
        roundResults = ["loss"] * len(playedCards)
        if self.showGames:
            print(playedCards)
        highestCard = max(playedCards)
        occurence = Counter(playedCards)[highestCard]
        if occurence == 1:
            index = playedCards.index(highestCard)
            roundResults[index] = "win"
        else:
            for i in range(len(roundResults)):
                if(playedCards[i] == highestCard):
                    roundResults[i] = "tie"
        return roundResults

    def findWinner(self):
        for p in self.players:
            if p.crowns >= self.crownsToWin:
                return p
        pseudoPlayer = player.Player("tie") # newPlayer stands for a pseudo winner in case of a tie
        return pseudoPlayer
