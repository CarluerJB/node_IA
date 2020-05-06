import tensorflow as tf
import tensorflow.keras as keras

def Model():
	layer0 = keras.layers.Input((0,0))
	layer1 = keras.layers.Input((0,0))
	layer2 = keras.layers.Add()([layer0, layer1])
	layer5 = keras.layers.Concatenate()([layer1, layer0])
	layer3 = keras.layers.Activation("sigmoid")(layer2)
	layer4 = keras.layers.Activation("elu")(layer5)
	return keras.models.Model(inputs = [layer0, layer1], outputs = [layer3, layer4])

if __name__=="__main__":
	model = Model()
	model.summary()
