import tensorflow as tf
import tensorflow.keras as keras

def Model():
	layer0 = keras.layers.Input((32, 32, 3))
	layer1 = keras.layers.Input((32, 32, 3))
	layer2 = keras.layers.Add()([layer1, layer0])
	layer4 = keras.layers.Dense(units=3, use_bias=True, activation="linear")(layer1)
	layer5 = keras.layers.Concatenate()([layer2, layer4])
	layer6 = keras.layers.Dense(units=11, use_bias=True, activation="linear")(layer5)
	layer3 = keras.layers.Activation("softmax")(layer6)
	return keras.models.Model(inputs = [layer0, layer1], outputs = layer3)

if __name__=="__main__":
	model = Model()
	model.summary()
