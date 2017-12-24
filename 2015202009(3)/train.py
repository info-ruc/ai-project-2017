import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from sklearn.model_selection import train_test_split

def load_data():
	X = []
	y = []
	with open('select.txt', 'r') as fp:
		for line in fp.readlines():
			name, value = line.split()
			value = int(value)
			if value >= 0:
				im = Image.open('JPEGImages/' + name + '.jpg').convert('L').resize((100, 100))
				im = np.array(im).reshape(1, 10000)
				X.extend(im)
				y.append(value)
	return np.array(X), np.array(y)

#目标数字做成0-5的One Hot编码
def tran_y(y):
	y_ohe = np.zeros(6)
	y_ohe[y] = 1
	return y_ohe

X, y = load_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 5)
X_train = X_train.reshape(X_train.shape[0], 100, 100, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 100, 100, 1).astype('float32')
X_train /= 255
X_test /= 255

y_train_ohe = np.array([tran_y(y_train[i]) for i in range(len(y_train))])
y_test_ohe = np.array([tran_y(y_test[i]) for i in range(len(y_test))])
#搭建卷积神经网络
model = Sequential()
model.add(Conv2D(filters = 128, kernel_size = (3, 3), strides = (1, 1), padding = 'same', input_shape = (100, 100, 1), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(64, activation = 'relu'))
model.add(Dense(32, activation = 'relu'))
model.add(Dense(6, activation = 'softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adadelta', metrics = ['accuracy'])
print(model.summary())
history = model.fit(X_train, y_train_ohe, validation_data = (X_test, y_test_ohe), epochs = 25, batch_size = 10)
model.save('model.h5')
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc = 'upper left')
plt.show()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss') 
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc = 'upper right')
plt.show()
scores = model.evaluate(X_train, y_train_ohe, verbose = 1)
print(scores)
scores = model.evaluate(X_test, y_test_ohe, verbose = 1)
print(scores)
