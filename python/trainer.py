#%%
import random
import sklearn
import keras
import game as game
import tensorflow as tf
import numpy as np
from collections import Counter
import tqdm
import time
import math


class Trainer:
    def __init__(self):
        # define the rewardsystem
        self.rewards = { 
            "base" : 0,
            "fail" : -200,
            "loss" : -10,
            "crown" : 5,
            "win" : 60
        }

        #training parameters
        self.nPlayers = 5
        self.nGames = 10**6
        self.maxRounds = 25
        self.learningRate =  0.11 
        self.optimizer = keras.optimizers.Adam(lr=self.learningRate)
        self.preload = True
        self.modelList = {}

        #counter to detect ai wrong picks
        self.wrongPicks = 0

        #available strats to train against:
        self.strategies = ["randomBot", "beaBot", "niklasBot", "henriekeBot", "ausweglosBot", "ai"]

        #load availabe ai models to train against 
        self.availableModelNames = { 
            #models for 5 players
            5 : ["henrieke_model", "zerobase_model", "zerobase_deep_model", "anyopponentai"]
        }



    def setPlayers(self, n):
        self.nPlayers = n
    
    def setMaxRounds(self, m):
        self.maxRounds = m

    
    def setLearningRate(self, lr):
        self.learningRate = lr


    def createModel(self):
        # define input shape
        testinput = np.array([[i for i in range(60)]])
        inputshape = testinput[0].shape
        model = keras.models.Sequential()
        model.add(keras.layers.Input(shape=inputshape))
        model.add(keras.layers.Dense(190, activation="relu"))
        model.add(keras.layers.Dense(110, activation="tanh"))
        model.add(keras.layers.Dense(40, activation="relu"))
        model.add(keras.layers.Dense(11, activation="softmax"))
        model.summary()
        return model

    ### preprocess the game in order to make the model work    

    def transformGameState(self, game): # extract the model input info from the game
        allinputs = []
        for player in game.players:
            # playerinput = []
            for card in range(11):
                if card in player.cards:
                    allinputs.append(1)
                else:
                    allinputs.append(0)
            allinputs.append(player.crowns)
        normedinput = self.normalize(allinputs)
        return np.array([normedinput])


    def normalize(self, inputList):
        inputs = np.array(inputList)
        mean = inputs.mean()
        std = inputs.std()
        normed = (inputs - mean)/std
        return normed


    def transformInput(self, inputVector, aiPosition): # adjust the input vector to guarantee the ai to be at position 0
        transInput = [inputVector[aiPosition]] #put the ai-input to the start
        for index, inputList in enumerate(inputVector):
            if index != aiPosition:
                transInput.append(inputList) # fill up the non-ai inputvectors
        return transInput
        

    def getaiSeat(self, game, newModelName):
        for player in game.players:
            if player.name == newModelName:
                return game.players.index(player)

    def getStrategy(self, includeAi = True):
        strats = self.strategies.copy()
        if not includeAi:
            strats.pop(strats.index("ai"))
        return random.choice(strats)

    def setupGame(self, modelName): # setup a game with training settings
        newGame = game.Game()
        newGame.trainAi = True
        newGame.addPlayer(modelName)
        for i in range(self.nPlayers-1):
            playerStrategy = self.getStrategy()
        #     # print(playerStrategy)
            if playerStrategy == "ai":
                model = self.loadModel("zerobase_deep_model")
                newGame.addAi(playerStrategy + str(i), model)
            else:
                newGame.addPlayer(playerStrategy+str(i), playerStrategy)   
            # newGame.addPlayer("randombot" + str(random.choice([1,2,3,4,5,6,7,8,9])))   
        return newGame

    def getAiReward(self, game, roundresult, modelName): #get the rewards for a given roundresult
        aiSeat = self.getaiSeat(game, modelName)
        reward = self.rewards["base"]
        if game.gameState == "abort":
            reward = self.rewards["fail"]
        elif roundresult[0] == "win":
            reward = self.rewards["crown"]
            if game.players[aiSeat].crowns == 2:
                reward = self.rewards["win"]
        else:
            for player in game.players:
                if player.crowns == 2:
                    reward = self.rewards["loss"]
        return reward

    def playRound(self, game, model, modelName): # play a single round (each participants plays 1 card)
        with tf.GradientTape() as tape:
            modelInput = game.gameStateToAiInput()
            modelOutput = model(modelInput)[0]
            card = np.random.choice(range(11), 1, np.array(modelOutput).tolist)
            move = np.zeros(11)
            move[card] = 1.0
            move = tf.cast(move, dtype=tf.float32)
            loss_fn = keras.losses.CategoricalCrossentropy()
            loss = loss_fn(move, modelOutput)
        grads = tape.gradient(loss, model.trainable_variables)
        roundresult = game.runRound([card, 0, 0, 0, 0])
        reward = self.getAiReward(game, roundresult, modelName)
        return game, grads, reward


    def playOneGame(self, model, modelName): # play rounds until either 1 player wins or #maxrounds rounds have been played
        game = self.setupGame(modelName)
        game.startGame()
        allRewards = []
        allGrads = []
        for r in range(self.maxRounds):
            if game.gameState == "running":
                game, grads, reward = self.playRound(game, model, modelName)
                allRewards.append(reward)
                allGrads.append(grads)
                if(reward == self.rewards["fail"]):
                    break #abort game since an invalid card has been played by ai
            else:
                break
        return allRewards, allGrads

    def normalizeRewards(self, allRewards): 
        allRewards = np.array(allRewards)
        if np.sum(allRewards) == 0:
            return allRewards
        mean = allRewards.mean()
        std = allRewards.std()
        if std == 0:
            print(std)
        normalized = [(rewards - mean)/std for rewards in allRewards]
        return normalized

    #######     functions to test the trained model     #######s

    def createRandomGameState(self, nPlayers): # return an arbitrary gameState (not won yet) - useful to quickly test ai behaviour
        gameState = [np.random.choice([0,1]) for i in range(60)]
        return np.array([gameState], dtype=float)


    def testGame(self, model, playerNames): # play a complete game - by default against random kis with the trained ai in seat 1
        newGame = game.Game()
        for player in playerNames:
            strategy = self.getStrategy(False)
            # print(strategy)
            newGame.addPlayer(player, strategy=strategy)
        newGame.players[0].strategy = "ai"
        newGame.players[0].name = "ai"
        newGame.players[0].loadModel(model)
        newGame.startGame()
        return newGame

    def runTest(self, model, nGames = 100): # play #ngames and print the win percentage of the trained ki
        playerNames = ["ai", "Christian", "Uliana", "Florian", "Markus"]
        wins = {}
        wrongPickPercentage = []
        for name in playerNames:
            wins.update({name : 0})
        wins.update({"tie": 0})
        for k in tqdm.tqdm(range(nGames), desc="Progress"):
            testGame = self.testGame(model, playerNames)
            winner = testGame.findWinner()
            wins[winner.name] += 1
            wrongPickPercentage.append(testGame.players[0].wrongPicks*100/testGame.round)
        self.showTestStats(wins, wrongPickPercentage, nGames)


    def showTestStats(self, wins, wrongPickPercentage, nGames):
        for p in wins:
            player = wins[p]
            if not player == "tie":
                print("\n" + str(p) + " wins: " +str(wins[p]) + " times. -> " + str(wins[p]/nGames*100.0) + "%")
        print("\n" + str(wins["tie"]/nGames * 100) + "% of the games ended tie.")
        averagewrongPicks = np.sum(wrongPickPercentage)/len(wrongPickPercentage)
        print("\n" + "AI picked a wrong card in " + str(averagewrongPicks) + "%. ")
        

    def preloadModels(self, selection = []):
        if self.preload:
            print("loading again")
            loadModels = self.availableModelNames[self.nPlayers]
            if len(selection) > 0:
                loadModels = selection
        for modelName in loadModels:
            self.modelList.update({modelName : keras.models.load_model(modelName, compile = False)})


    def loadModel(self, modelName):
        if not modelName in self.modelList:
            self.preloadModels()
        if modelName in self.modelList:
            model = self.modelList[modelName]
        else:
            model = self.createModel()
        return model


    def trainModel(self, newModelName, loadModelName = ""):
        model = self.loadModel(loadModelName)
        for i in tqdm.tqdm(range(self.nGames), desc="Progress"):
            allRewards, allgrads = self.playOneGame(model, newModelName)
            finalrewards = self.normalizeRewards(allRewards)
            allmeangrads = []
            for varindex in range(len(model.trainable_variables)):
                meangrads = tf.reduce_mean(
                    [finalreward * allgrads[step][varindex]
                    for step, finalreward in enumerate(finalrewards)], axis=0)
                allmeangrads.append(meangrads)
            self.optimizer.apply_gradients(zip(allmeangrads, model.trainable_variables))
        model.save(newModelName)
        return model

trainer = Trainer()
trainingModel = "anyopponentai"
newModel = trainer.trainModel(trainingModel, trainingModel)
trainer.runTest(newModel)

# todo:
#   - plot the error/learning curve

# %%
