#%%
import random 
import numpy as np

class Player:
    def __init__(self, name):
        self.name = name
        self.game = None 
        self.cards = [i for i in range(11)]
        self.crowns = 0
        self.strategy = "randomBot"
        self.aiModel = None
        self.wrongPicks = 0

    def playCard(self):
        return getattr(self, self.strategy)() #execute the given strategy 
        
    def getCardInput(self):
        card = -1
        while card not in self.cards:
            print("Choose a card! Your cards are: " + str(self.cards))
            card = int(input())
        else:
            return card
            
    def removeHighestCards(self, amount = 1):
        for i in range(amount):
            if(self.cards[-1] != 0):
                self.cards.pop()

    def removeCard(self, card):
        try:
            index = self.cards.index(card)
        except:
            print(self.strategy)
        if(self.cards[index] != 0):
            self.cards.pop(index)
        

    def addCrown(self):
        self.crowns += 1
    
    def changeName(self, newName):
        self.name = newName

    def reset(self):
        self.cards = [i for i in range(11)]
        self.crowns = 0

        
    #defining the different custom made strategies to train against
    def randomBot(self):
        card = random.choice(self.cards)
        return card

    def human(self):
        card = self.getCardInput()
        return card

    def beaBot(self):
        if self.game.round == 0:
            card = 0
        elif self.game.round == 1:
            card = random.choice([0, 4])
        else:
            card = np.max(self.cards)
        return card

    def niklasBot(self):
        if np.random.random() < 0.25:
            if 1 in self.cards:
                card = 1
            else:
                card = 0
        else:
            card = 0
        return card

    def henriekeBot(self):
        if self.game.round < 2:
            card = 0
        elif self.game.round == 2:
            card = 7
        else:
            card = np.max(self.cards)
        return card

    def ausweglosBot(self):
        if self.game.round < 4:
            card = 0
        elif self.game.round == 4:
            card = 4
        else:
            card = np.max(self.cards) 
        return card
    
    def ai(self): #access the ai 
        modelIn = self.game.gameStateToAiInput()
        modelOut = self.aiModel(modelIn)[0]
        card = np.argmax(modelOut)
        if card not in self.cards:
            self.wrongPicks += 1
            card = random.choice(self.cards)
        return card  

    def setModel(self, model): #load the ai
        self.aiModel = model
# %%
