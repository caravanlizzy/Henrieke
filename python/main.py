#%%
import game
import trainer

modelToTrain = "thirdmaysimple"
t = trainer.Trainer()
t.setNGames(10)
t.addToModelList("zerobase_deep_model")
newModel = t.trainModel(modelToTrain)
t.testModel(modelToTrain, nGames = 10**3)
# %%
