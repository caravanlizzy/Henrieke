#%%
import sklearn
import keras
import game as cardgame
import tensorflow as tf
import numpy as np
from collections import Counter
import tqdm
import time
import math


# define the rewardsystem
rewards = {
    "base" : 0,
    "fail" : -100,
    "loss" : -10,
    "crown" : 5,
    "win" : 60
}



# new ai settings
trainmodel = False
newmodelname = "zerobase_deep_model"

# previous ai settings
loadmodel = False
loadmodelname = "henrieke_model"


#training parameters
nplayers = 5
ngames = 10**6
maxrounds = 35
learningrate = 0.01
optimizer = keras.optimizers.Adam(lr=learningrate)


# define input shape
testinput = np.array([[i for i in range(60)]])
inputshape = testinput[0].shape


# a first mode1

model = keras.models.Sequential()
model.add(keras.layers.Input(shape=inputshape))
# model.add(keras.layers.Dense(75, activation="tanh"))
model.add(keras.layers.Dense(190, activation="relu"))
model.add(keras.layers.Dense(110, activation="tanh"))
model.add(keras.layers.Dense(40, activation="relu"))
model.add(keras.layers.Dense(11, activation="softmax"))
model.summary()


#######     functions to preprocess the game in order to make the model work    #######

def gamestatetoinput(game): # function to extract the model input info from the game
    allinputs = []
    for player in game.players:
        # playerinput = []
        for card in range(11):
            if card in player.cards:
                allinputs.append(1)
            else:
                allinputs.append(0)
        allinputs.append(player.crowns)
    normedinput = normalize(allinputs)
    return np.array([normedinput])


def normalize(inputlist):
    inputs = np.array(inputlist)
    mean = inputs.mean()
    std = inputs.std()
    normed = (inputs - mean)/std
    return normed


def transforminput(inputvector, kiposition): # function to adjust the input vector to guarantee the ai to be at position 0
    transinput = [inputvector[kiposition]] #put the ai-input to the start
    for index, inputlist in enumerate(inputvector):
        if index != kiposition:
            transinput.append(inputlist) # fill up the non-ai inputvectors
    return transinput
    

def getaiseat(game, newmodelname):
    for player in game.players:
        if player.name == newmodelname:
            return game.players.index(player)


def setupgame(playernum): # setup a game with training settings
    newgame = cardgame.Game()
    newgame.trainai = True
    newgame.addplayer(newmodelname)
    for i in range(playernum-1):
        newgame.addplayer("random"+str(i))
    return newgame



def getkireward(game, roundresult, rewards): #get the rewards for a given roundresult
    aiseat = getaiseat(game, newmodelname)
    reward = rewards["base"]
    if game.gamestate == "abort":
        reward = rewards["fail"]
    elif roundresult[0] == "win":
        reward = rewards["crown"]
        if game.players[aiseat].crowns == 2:
            reward = rewards["win"]
    else:
        for player in game.players:
            if player.crowns == 2:
                reward = rewards["loss"]
    return reward

def playround(game, model): # play a single round (each participants plays 1 card)
    with tf.GradientTape() as tape:
        modelinput = game.gamestatetoaiinput()
        modeloutput = model(modelinput)[0]
        card = np.random.choice(range(11), 1, np.array(modeloutput).tolist)
        move = np.zeros(11)
        move[card] = 1.0
        move = tf.cast(move, dtype=tf.float32)
        loss_fn = keras.losses.CategoricalCrossentropy()
        loss = loss_fn(move, modeloutput)
    grads = tape.gradient(loss, model.trainable_variables)
    roundresult = game.runround([card, 0, 0, 0, 0])
    reward = getkireward(game, roundresult, rewards)
    return game, grads, reward


def playonegame(model, maxrounds, nplayers): # play many rounds until either 1 player wins or #maxrounds rounds have been played
    game = setupgame(nplayers)
    game.startgame()
    allrewards = []
    allgrads = []
    for r in range(maxrounds):
        if game.gamestate == "running":
            game, grads, reward = playround(game, model)
            allrewards.append(reward)
            allgrads.append(grads)
            if(reward == -100):
                break #abort game since an invalid card has been played
        else:
            break
    return allrewards, allgrads

def normalizerewards(allrewards): 
    allrewards = np.array(allrewards)
    if np.sum(allrewards) == 0:
        return allrewards
    mean = allrewards.mean()
    std = allrewards.std()
    if std == 0:
        print(std)
    normalized = [(rewards - mean)/std for rewards in allrewards]
    return normalized

#######     functions to test the trained model     #######s

def createrandomgamestate(nplayers): # return an arbitrary gamestate (not won yet) - useful to quickly test tendencies
    gamestate = [np.random.choice([0,1]) for i in range(60)]
    return np.array([gamestate], dtype=float)

c = createrandomgamestate # for quick access

def playtestgame(model, playernames): # play a complete game - by default against random kis with the trained ai in seat 1
    game = cardgame.Game()
    for player in playernames:
        game.addplayer(player)
    game.players[0].strategy = "ai"
    game.players[0].aimodel = model
    winner = game.startgame()
    return winner

def runtest(model, ngames = 100): # play #ngames and print the win percentage of the trained ki
    ainame = "AI"
    playernames = [ainame, "Christian", "Uliana", "Florian", "Markus"]
    wins = {}
    for name in playernames:
        wins.update({name : 0})
    wins.update({"tie": 0})
    for k in tqdm.tqdm(range(ngames), desc="Progress"):
        winner = playtestgame(model, playernames)
        name = winner.name
        wins[name] += 1
    for p  in playernames:
        print("\n" + str(p) + " wins: " +str(wins[p]) + " times. -> " + str(wins[p]/ngames*100.0) + "%")
    print("\n" + str(wins["tie"]/ngames * 100) + "% of the games ended tie.")
    
trainmodel = True
# loop to actually train the model
if trainmodel:
    if loadmodel:
        model = keras.models.load_model(loadmodelname)
    for i in tqdm.tqdm(range(ngames), desc="Progress"):
        # print("\nGame # " + str(i))
        allrewards, allgrads = playonegame(model, maxrounds, nplayers)
        finalrewards = normalizerewards(allrewards)
        allmeangrads = []
        for varindex in range(len(model.trainable_variables)):
            meangrads = tf.reduce_mean(
                [finalreward * allgrads[step][varindex]
                for step, finalreward in enumerate(finalrewards)], axis=0)
            allmeangrads.append(meangrads)
        optimizer.apply_gradients(zip(allmeangrads, model.trainable_variables))
    model.save(newmodelname)


testmodel = loadmodel
test_model = keras.models.load_model(newmodelname)

runtest(test_model, 10**4)


# todo:
#   - plot the error/learning curve

# %%
