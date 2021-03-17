# Change this to something between 0.2 and 0.5
dropout = 0.5

# For RMSprop, Adam, Nadam optimizer the learning rate should be around 0.0001
# For Adadelta the learning rate has to be set to 0.1
learning_rate = 0.01

# Increase or dcrease this number according to your system
batch_size = 16

# The directory in which we stored the training and validation data for the two different classes.
# !!! Make sure to adjust this !!!
train_dir = 'data3_update/train/'
val_dir = 'data3_update/validation/'

# Image resolution in pixels for the image slices
x = 100 #height
y = 119 #width
img_size = (x, y, 3)

# Number of training and validation images
nr_train_img = 5838 # don't forget
nr_val_img = 1894  # don't forget

# Number of training epochs; for testing 5 for final training 15 - 30
nr_epoch = 30



model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(img_size), kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(dropout))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer=SGD(lr=learning_rate,momentum=0.9, nesterov=True),
              metrics=['accuracy'])
