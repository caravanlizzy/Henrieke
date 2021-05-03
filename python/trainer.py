#%%
import random
import sklearn
import keras
import game
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
            "fail" : -150,
            "loss" : -10,
            "crown" : 5,
            "win" : 70
        }
        #training parameters
        self.nPlayers = 5
        self.nGames = 10**5
        self.maxRounds = 25
        self.learningRate =  0.05

        self.optimizer = keras.optimizers.Adam(lr=self.learningRate) #optimizier is being loaded 
        self.modelList = {} #list to store models to prevent loading them more than once
        self.model = None #trained model is stored here automatically
        self.wrongPicks = 0 #counter to detect ai wrong picks

        #available strats to train against:
        self.strategies = ["randomBot", "beaBot", "niklasBot", "henriekeBot", "ausweglosBot", "ai"]

    def getReward(self, event):
        return self.rewards[event]

    def setReward(self, event, value):
        self.rewards[event] = value

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
        print("New model successfully created.")
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

    def getStrategy(self, includeAi = False):
        strats = self.strategies.copy()
        if not includeAi:
            strats.pop(strats.index("ai"))
        return random.choice(strats)

    def setupGame(self, trainModelName): # setup a game with training settings
        newGame = game.Game()
        newGame.trainAi = True
        newGame.addPlayer(trainModelName, "trainAi")
        for i in range(self.nPlayers-1):
            playerStrategy = self.getStrategy()
        #     # print(playerStrategy)
            if playerStrategy == "ai":
                loadModelName = "zerobase_deep_model"
                model = self.loadModel(loadModelName)
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
            print("fail passierte: " + str(reward))
        elif roundresult[0] == "win":
            reward = self.rewards["crown"]
            # print("crown passierte: " + str(reward))
            if game.players[aiSeat].crowns == 2:
                reward = self.rewards["win"]
                # print("win passierte: " + str(reward))
        else:
            for player in game.players:
                if player.crowns == 2:
                    reward = self.rewards["loss"]
        return reward

    def coinToss(self):
        # return random.choice([True, False])
        return True

    def playRound(self, game, model, modelName): # play a single round (each participants plays 1 card)
        with tf.GradientTape() as tape:
            modelInput = game.gameStateToAiInput()
            modelOutput = model(modelInput)[0]
            # print("modeloutput: " + str(modelOutput))
            if self.coinToss():
                card = np.random.choice(range(11), 1, np.array(modelOutput).tolist)[0]
            else:
                card = tf.math.argmax(modelOutput)
                # print("model played card: " + str(card))
            # print(card)
            move = np.zeros(11)
            move[card] = 1.0
            move = tf.cast(move, dtype=tf.float32)
            lossFunction = keras.losses.CategoricalCrossentropy()
            # loss_fn = keras.losses.Adam()
            # print("move is: " + str(move))
            # print("modeloutput is: " + str(modelOutput))
            lossValue = lossFunction(move, modelOutput)
            print("loss is: " + str(lossValue))
        grads = tape.gradient(lossValue, model.trainable_variables)
        print("current gradienst: "+str(grads))
        roundresult = game.runRound([card, 0, 0, 0, 0])
        reward = self.getAiReward(game, roundresult, modelName)
        return game, grads, reward


    def playOneGame(self, model, modelName): # play rounds until either 1 player wins or #maxrounds rounds have been played
        game = self.setupGame(modelName)
        game.start()
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
        # print("all rewards for this game are: " + str(allRewards))
        return allRewards, allGrads

    def normalizeRewards(self, allRewards): 
        allRewards = np.array(allRewards)
        if np.sum(allRewards) == 0:
            return allRewards
        mean = allRewards.mean()
        # print("mean: " + str(mean))
        std = allRewards.std()
        # print("std: " + str(std))
        if std == 0:
            print(std)
        normalized = [(rewards - mean)/std for rewards in allRewards]
        return normalized

    #######     functions to test the trained model     #######s

    def createRandomGameState(self, nPlayers): # return an arbitrary gameState (not won yet) - useful to quickly test ai behaviour
        gameState = [np.random.choice([0,1]) for i in range(60)]
        return np.array([gameState], dtype=float)


    def setupTest(self, modelName, playerNames): # play a complete game - by default against random bots with the trained ai in seat 1
        newGame = game.Game()
        for player in playerNames:
            strategy = self.getStrategy(False)
            newGame.addPlayer(player, strategy=strategy)
        newGame.players[0].strategy = "ai"
        newGame.players[0].name = "ai"
        # model = self.loadModel(modelName)
        model = self.model
        newGame.players[0].setModel(model)
        newGame.start()
        return newGame

    def test(self, modelName, nGames = 100): # play #ngames and print the win percentage of the trained ki
        playerNames = ["ai", "Christian", "Uliana", "Florian", "Markus"]
        wins = {}
        wrongPickPercentage = []
        for name in playerNames:
            wins.update({name : 0})
        wins.update({"tie": 0})
        for k in tqdm.tqdm(range(nGames), desc="Progress"):
            testGame = self.setupTest(modelName, playerNames)
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
        print("\n" + "AI picked an invalid card in " + str(averagewrongPicks) + "%. ")
        


    def loadModel(self, modelName, compile=False):
        if modelName in self.modelList:
            model = self.modelList[modelName]
        else:
            model = keras.models.load_model(modelName, compile = compile)
        return model

    def addToModelList(self, modelNames):
        for modelName in modelNames:
            if modelName not in self.modelList:
                model = self.loadModel(modelName)
                print(str(modelName) + " has been added to <trainerInstance>.modelList.")
                self.modelList[modelName] = model

    def getModel(self, modelName):
        if modelName not in self.modelList:
            self.addToModelList(modelName)
        return self.modelList[modelName]

    def trainModel(self, newModelName, loadModelName = ""):
        if loadModelName in self.modelList:
            model = self.loadModel(loadModelName, compile=True)
        else:
            model = self.createModel()
        print("\nStart training.")
        for i in tqdm.tqdm(range(self.nGames), desc="Progress"):
            allRewards, allGrads = self.playOneGame(model, newModelName)
            finalRewards = self.normalizeRewards(allRewards)
            # print("normalized rewards are: " + str(finalRewards))
            allMeanGrads = []
            for varIndex in range(len(model.trainable_variables)):
                meanGrads = tf.reduce_mean(
                    # [finalreward * allgrads[step][varindex]
                    [self.getFinalReward(finalReward, allGrads, step, varIndex)
                    for step, finalReward in enumerate(finalRewards)], axis=0)
                allMeanGrads.append(meanGrads)
                # print(meanGrads)
            # print(model.trainable_variables)
            # print(allmeangrads)
            self.optimizer.apply_gradients(zip(allMeanGrads, model.trainable_variables))
            print(model.trainable_weights)
        self.model = model
        self.addToModelList(newModelName)
        print("\nModel Saved.")
        return model

    def getFinalReward(self, finalReward, allGrads, step, varIndex):
        # print(finalReward)
        result = finalReward * allGrads[step][varIndex]
        # print(result)
        return result



modelToTrain = "secondmay_new"
trainer = Trainer()
trainer.addToModelList(["zerobase_deep_model"])
newModel = trainer.trainModel("secondmay_new")
trainer.test(modelToTrain, nGames = 10**4)

# todo:
#   - plot the error/learning curve

# %%

# %%
