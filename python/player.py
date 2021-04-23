#%%
import random 
import numpy as np

class Player:
    def __init__(self, name):
        self.name = name
        self.game = None 
        self.cards = [i for i in range(11)]
        self.crowns = 0
        self.strategy = "randombot"
        self.aimodel = None
        self.wrongpicks = 0

    def playcard(self):
        return getattr(self, self.strategy)() #execute the given strategy 
        
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
        try:
            index = self.cards.index(card)
        except:
            print(self.strategy)
        if(self.cards[index] != 0):
            self.cards.pop(index)
        

    def addcrown(self):
        self.crowns += 1
    
    def changename(self, newname):
        self.name = newname

    def reset(self):
        self.cards = [i for i in range(11)]
        self.crowns = 0

        
    #defining the different custom made strategies to train against
    def randombot(self):
        card = random.choice(self.cards)
        return card

    def human(self):
        card = self.getcardinput()
        return card

    def beabot(self):
        if self.game.round == 0:
            card = 0
        elif self.game.round == 1:
            card = random.choice([0, 4])
        else:
            card = np.max(self.cards)
        return card

    def niklasbot(self):
        if np.random.random() < 0.25:
            if 1 in self.cards:
                card = 1
            else:
                card = 0
        else:
            card = 0
        return card

    def henrieke(self):
        if self.game.round < 2:
            card = 0
        elif self.game.round == 2:
            card = 7
        else:
            card = np.max(self.cards)
        return card

    def ausweglos(self):
        if self.game.round < 4:
            card = 0
        elif self.game.round == 4:
            card = 4
        else:
            card = np.max(self.cards) 
        return card
    
    def ai(self):
        modelin = self.game.gamestatetoaiinput()
        modelout = self.aimodel(modelin)[0]
        card = np.argmax(modelout)
        if card not in self.cards:
            self.wrongpicks += 1
            card = random.choice(self.cards)
        return card  

    def loadmodel(self, model):
        self.aimodel = model
# %%
