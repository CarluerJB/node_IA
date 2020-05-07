import tensorflow as tf
import tensorflow.keras as keras

def Model():
	layer0 = keras.layers.Input((None, None, 3))
	layer2 = keras.layers.Conv2D(filters=200, kernel_size=(3, 3), strides=(1, 1), padding="same", activation="linear")(layer0)
	layer3 = keras.layers.Conv2D(filters=100, kernel_size=(5, 5), strides=(1, 1), padding="same", activation="linear")(layer2)
	layer4 = keras.layers.Conv2D(filters=3, kernel_size=(1, 1), strides=(1, 1), padding="same", activation="linear")(layer3)
	layer1 = keras.layers.Activation("sigmoid")(layer4)
	return keras.models.Model(inputs = layer0, outputs = layer1)

if __name__=="__main__":
	model = Model()
	model.summary()
