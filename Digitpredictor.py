import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalize and reshape for CNN-compatible shape (needed for augmentation)
x_train = x_train / 255.0
x_test = x_test / 255.0

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# Data Augmentation - works only on 4D image data, not flattened
datagen = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)
datagen.fit(x_train)

# Build the model - FIXED LeakyReLU usage
model = models.Sequential([
    layers.Flatten(input_shape=(28, 28, 1)),
    layers.Dense(128),
    layers.LeakyReLU(alpha=0.1),
    layers.Dense(64),
    layers.LeakyReLU(alpha=0.1),
    layers.Dense(10, activation='softmax')
])

# Compile the model - adam is better than rmsprop for this
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model with augmented data
model.fit(datagen.flow(x_train, y_train, batch_size=32), epochs=10)

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_acc}")

# Make predictions
predictions = model.predict(x_test)

# Display the first image and prediction - FIXED reshape
plt.imshow(x_test[0].reshape(28, 28), cmap=plt.cm.binary)
plt.title(f"Predicted: {predictions[0].argmax()} - Actual: {y_test[0]}")
plt.show()