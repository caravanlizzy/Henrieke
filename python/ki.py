#%%
import sklearn
import keras
import game
import tensorflow as tf
import numpy as np



# create a ki for the game with a fixed set of 5 players
# each player starts with 11 cards and 0 crowns
# input per player = [1] * 11 + [0]
# complete input = [[1]* 11 + [0]] * 5
inputshape = (5, 12)

# the output is one of the 11 playable cards
outputshape = (11,)






# a first model

model = keras.models.Sequential()
model.add(keras.layers.Input(shape=inputshape))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(40, activation="relu"))
model.add(keras.layers.Dense(1, activation="linear"))
model.compile()
model.summary()

#%%
def gamestatetoinput(game): # function to extract
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
    return allinputs

def setupgame(playernum):
    newgame = game.Game()
    newgame.addplayer("ki")
    for i in range(playernum-1):
        newgame.addplayer("random"+str(i))
    return newgame

def playstep(game, model):
    with tf.GradientTape() as tape:
        modelinput = gamestatetoinput(game)
        movedistribution = model(modelinput[None])
        move = np.random.choice(range(11), 1, movedistribution)

    return game, grads


testgame = setupgame(5)
testgame.runround()


# define the rewardsystem
wrongmovereward = -100
lossreward = -3
crownreward = 2
winreward = 10

rewards = [wrongmovereward, lossreward, crownreward, winreward]
# %%
