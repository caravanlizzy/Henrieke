#%%
import sklearn
import keras
import game as cardgame
import tensorflow as tf
import numpy as np
from collections import Counter


# define the rewardsystem
rewards = {
    "fail" : -100,
    "loss" : -5,
    "crown" : 3,
    "win" : 15
}


kiname = "ki"
testinput = np.array([[[i for i in range(12)] for j in range(5)]])
inputshape = testinput[0].shape
# print(testinput)


# a first model

model = keras.models.Sequential()
model.add(keras.layers.Input(shape=inputshape))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(40, activation="relu"))
model.add(keras.layers.Dense(11, activation="softmax"))

model.summary()

#%%
def gamestatetoinput(game): # function to extract the model input info from the game
    allinputs = []
    for player in game.players:
        playerinput = []
        for card in range(11):
            if card in player.cards:
                playerinput.append(1)
            else:
                playerinput.append(0)
        playerinput.append(player.crowns)
        allinputs.append(playerinput)
    return np.array([allinputs])

def transforminput(inputvector, kiposition): # function to adjust the input vector to guarantee the ki to be at position 0
    transinput = [inputvector[kiposition]] #put the kiinput to the start
    for index, inputlist in enumerate(inputvector):
        if index != kiposition:
            transinput.append(inputlist) # fill up the non-ki inputvectors
    return transinput
    

def getkiseat(game, kiname):
    for player in game.players:
        if player.name == kiname:
            return game.players.index(player)


def setupgame(playernum):
    newgame = cardgame.Game()
    newgame.addplayer(kiname)
    for i in range(playernum-1):
        newgame.addplayer("random"+str(i))
    return newgame

def getkireward(game, roundresult, rewards):
    kiseat = getkiseat(game, kiname)
    reward = 0
    if game.gamestate == "abort":
        reward = rewards["fail"]
    elif roundresult[0] == "win":
        reward = rewards["crown"]
        if game.players[kiseat].crowns == 2:
            reward = rewards["win"]
    else:
        for player in game.players:
            if player.crowns == 2:
                reward = rewards["loss"]
    return reward

def playround(game, model):
    with tf.GradientTape() as tape:
        modelinput = gamestatetoinput(game)
        modeloutput = model.predict(modelinput)[0]
        card = np.random.choice(range(11))
        move = np.zeros(11)
        move[card] = 1.0
        loss_fn = keras.losses.CategoricalCrossentropy()
        loss = loss_fn(move, modeloutput)
        print(loss)
    grads = tape.gradient(loss, model.trainable_variables)
    print(grads)
    roundresult = game.runround([card, 0, 0, 0, 0])
    reward = getkireward(game, roundresult, rewards)
    return game, grads, reward


def playonegame(model, maxrounds):
    game = setupgame(5)
    allrewards = []
    allgrads = []
    for r in range(maxrounds):
        if not (game.gamestate == "over" or game.gamestate == "abort"):
            game, grads, reward = playround(game, model)
            allrewards.append(reward)
            allgrads.append(grads)
        else:
            break
    return allrewards, allgrads

def normalizerewards(allrewards):
    allrewards = np.array(allrewards)
    mean = allrewards.mean()
    std = allrewards.std()
    normalized = [(rewards - mean)/std for rewards in allrewards]
    return normalized

ngames = 500
maxrounds = 25
optimizer = keras.optimizers.Adam(lr=0.01)

for i in range(ngames):
    allrewards, allgrads = playonegame(model, maxrounds)
    finalrewards = normalizerewards(allrewards)
    print(finalrewards)
    allmeangrads = []
    for varindex in range(len(model.trainable_variables)):
        meangrads = tf.reduce_mean(
            [finalreward * allgrads[step][varindex]
            for step, finalreward in enumerate(finalrewards)], axis=0)
        allmeangrads.append(meangrads)
    optimizer.apply_gradients(zip(allmeangrads, model.trainable_variables))

