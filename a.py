import tensorflow as tf
import tensorflow.keras as keras

def Model():
	layer0 = keras.layers.Input((0, 2))
	layer1 = keras.layers.Input((0, 2))
	layer4 = keras.layers.Dense(units=2, use_bias=True)(layer1)
	layer2 = keras.layers.Add()([layer0, layer1, layer4])
	layer3 = keras.layers.Activation("elu")(layer2)
	return keras.models.Model(inputs = [layer0, layer1], outputs = layer3)

if __name__=="__main__":
	model = Model()
	model.summary()
