from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Activation, Dropout, Dense
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from Data_Parser import getNotes
import numpy

SEQUENCE_LEN = 20
LOADED = False # must change if songs are added to training/testing data

def main():
    input, output, mapping = getNotes(SEQUENCE_LEN, True, LOADED)  # getNotes(int, bool train, bool loaded)
    training_input = [[mapping[note] for note in sequence] for sequence in input]
    training_output = [mapping[note]for note in output]
    training_input = numpy.reshape(training_input, (len(training_input), len(training_input[0]), 1))
    training_output = to_categorical(training_output, num_classes = len(mapping))
    # print(training_input.shape)
    # print(training_output.shape)
    model = Sequential()
    model.add(LSTM(512,  # num nodes
                   input_shape=(training_input.shape[1], training_input.shape[2]),   # Since this is the first layer, we know dimentions of input
                   return_sequences=True))  # creates recurrence
    print('training_input.shape[1] = %d, training_input.shape[2] = %d'
            %(training_input.shape[1], training_input.shape[2]))
    model.add(LSTM(512,
                   return_sequences=True,  # creates recurrence
                   recurrent_dropout=0.2,))  # fraction to leave out from recurrence

    model.add(LSTM(512))            # multiple LSTM layers create Deep Neural Network for greater accuracy
    model.add(BatchNorm())          # normalizes inputs to neural network layers to make training faster
    #model.add(Activation('relu'))  # is this appropriate for LSTM layer?Rectified Linear activation - overcomes vanishing gradient problem
    model.add(Dropout(0.2))         # prevents overfitting
    model.add(Dense(len(mapping)))  # classification layer - output must be same dimentions as mapping
    model.add(Activation('softmax'))# transforms output into a probability distribution

    model.compile(loss='categorical_crossentropy', optimizer='adam')  # try changing optimizer to adam - adpative moment estimation

    model.summary()
    #TRAINING TIME
    filepath = "takao_reformed_adam.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    model_callbacks = [checkpoint]

    # 100 epochs led to minimal returns to training loss
    model.fit(training_input, training_output, epochs=50, batch_size=64, callbacks=model_callbacks)


if __name__ == '__main__':
    main()
