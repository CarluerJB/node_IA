import tensorflow as tf
import tensorflow.keras as keras

def Model():
	layer0 = keras.layers.Input((0,0))
	layer1 = keras.layers.Input((0,0))
	layer2 = keras.layers.Add()([layer0, layer1])
	layer3 = keras.layers.Activation("sigmoid")(layer2)
	return keras.models.Model(inputs = [layer0, layer1], outputs = layer3)

if __name__=="__main__":
	model = Model()
	model.summary()
