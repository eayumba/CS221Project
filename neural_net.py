from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Activation, Dropout, Dense
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from Data_Parser import getNotes
import numpy

SEQUENCE_LEN = 20


def main():
    input, output, mapping = getNotes(SEQUENCE_LEN)
    training_input = [[mapping[note] for note in sequence] for sequence in input]
    training_output = [mapping[note]for note in output]
    # print("len(training_input[0] = ", len(training_input[0]))
    training_input = numpy.reshape(training_input, (len(training_input), len(training_input[0]), 1))
    #training_output = to_categorical(training_output)
    model = Sequential()
    model.add(LSTM(512,
                   input_shape=(training_input.shape[1], training_input.shape[2]),   # TODO: lern more and fixlen(training_input[0]),),
                   recurrent_dropout=0.3,
                   return_sequences=True))

    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Activation('relu'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='rmsprop')

    #TRAINING TIME
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    model.summary()

    model.fit(training_input, training_output, epochs=5, batch_size=10, callbacks=callbacks_list)



# A B C D E F G
# input[0] = [A,B,C] output[0] = D
# input[1] = [B, C, D] output[1] = E

if __name__ == '__main__':
    main()
