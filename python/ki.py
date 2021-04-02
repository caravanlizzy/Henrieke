#%%
import sklearn
import keras
import game



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
model.add(keras.layers.Dense(1, activation="softmax"))
model.compile()
model.summary()


# %%
