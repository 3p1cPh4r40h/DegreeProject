import pickle
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, ThresholdedReLU
from keras.models import Sequential
import matplotlib.pyplot as plt

# Load the preprocessed data from the pickle files
with open('network_files/x_train.pkl', 'rb') as f:
    x_train = pickle.load(f)
with open('network_files/y_train.pkl', 'rb') as f:
    y_train = pickle.load(f)
with open('network_files/x_val.pkl', 'rb') as f:
    x_val = pickle.load(f)
with open('network_files/y_val.pkl', 'rb') as f:
    y_val = pickle.load(f)
with open('network_files/x_test.pkl', 'rb') as f:
    x_test = pickle.load(f)
with open('network_files/y_test.pkl', 'rb') as f:
    y_test = pickle.load(f)
with open('network_files/label_set.pkl', 'rb') as f:
    label_set = pickle.load(f)

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
x_val = x_val.reshape(x_val.shape[0], x_val.shape[1], x_val.shape[2], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

# Create a convolutional neural network model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=x_train.shape[1:]))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(len(label_set), activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, epochs=100, batch_size=16, validation_data=(x_val, y_val))


# Plot the training and validation accuracy over the training epochs
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.savefig('model_results/accuracy_plot69proof.png')
plt.show()

# Plot the training and validation loss over the training epochs
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.savefig('model_results/loss_plot69proof.png')
plt.show()



# Save the model
model.save('network_files/modelxproof.h5')

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test loss:', test_loss)
print('Test accuracy:', test_acc)