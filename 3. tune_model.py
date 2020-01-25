import constants as cst
import pandas as pd
import os as os

from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import numpy as np
import random
import time

import imp
imp.reload(cst)

# Directory Dictionary
DIR = cst.get_dirs()

# Load file
file_name = os.path.join(DIR['parent'], 'clean_data.csv')
data = pd.read_csv (file_name)
# quicker development, turn off when ready for proper tuning
#data = data.iloc[1:50000,]


# Partition Data
data_train = data[data['partition'] == 'train']
data_dev = data[data['partition'] == 'dev']
data_test = data[data['partition'] == 'test']

del(data, file_name)

# Drop columns
data_train.drop(['partition'], axis = 1, inplace = True)
data_test.drop(['partition'], axis = 1, inplace = True)
data_dev.drop(['partition'], axis = 1, inplace = True)


# Convert to numpy matrix
data_train = data_train.as_matrix()
data_dev = data_dev.as_matrix()
data_test = data_test.as_matrix()

np.random.seed(1)

# Split into X and Y
Y_train = data_train[:, 0]
Y_dev = data_dev[:, 0]
Y_test = data_test[:, 0]

X_train = data_train[:, 1:35]
X_dev = data_dev[:, 1:35]
X_test = data_test[:, 1:35]

del(data_dev, data_test, data_train)

# Check proportion of positives
np.mean(Y_train)
np.mean(Y_dev)
np.mean(Y_test)



# Hyper Parameters
input_dim = X_train.shape[1]
learning_rate = 0.001
cell_per_layer = 128
batch_size = 2^11
epochs = 1



def build_model(learning_rate, cell_per_layer, batch_size, epochs):
    print(learning_rate, cell_per_layer, batch_size, epochs)
    # create model
    # two layers
    model = Sequential()
    model.add(Dense(cell_per_layer, input_dim=input_dim, activation='relu'))
    model.add(Dense(cell_per_layer, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Adam optimizer
    adam = optimizers.Adam(lr=learning_rate)

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])

    # Fit the model
    start = time.clock()
    model.fit(X_train, Y_train, epochs=epochs , batch_size=batch_size)
    time_taken = time.clock() - start

    # evaluate the model
    dev_acc = model.evaluate(X_dev, Y_dev)
    test_acc = model.evaluate(X_test, Y_test)
    print('dev & test acc:' , dev_acc[1], test_acc[1])

    tuning_csv = os.path.join(DIR['parent'], 'tuning.csv')

    df = pd.DataFrame([[learning_rate, cell_per_layer, batch_size, epochs, dev_acc[1], test_acc[1], time_taken]]
    , columns = ['learning_rate', 'cell_per_layer', 'batch_size', 'epochs', 'dev_acc', 'test_acc', 'time_taken']
    )

    with open(tuning_csv, 'a') as f:
        df.to_csv(f, header=False, index=False)

while(True):
    # Tuning process
    learning_rate = 10 ** (random.randint(-3, -2))
    cell_per_layer = 2 ** (random.randint(6, 9))
    batch_size = 2 ** (random.randint(8, 11))
    epochs = 2 ** (random.randint(6,8))

    try: build_model(learning_rate, cell_per_layer, batch_size, epochs)
    finally: print()
