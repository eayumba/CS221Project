from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Activation, Dropout, Dense
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from Data_Parser import getNotes
import numpy

SEQUENCE_LEN = 20

def main():
    input, output, mapping = getNotes(SEQUENCE_LEN, True)
    training_input = [[mapping[note] for note in sequence] for sequence in input]
    training_output = [mapping[note]for note in output]
    training_input = numpy.reshape(training_input, (len(training_input), len(training_input[0]), 1))
    training_output = to_categorical(training_output, num_classes = len(mapping))
    print(training_input.shape)
    print(training_output.shape)
    model = Sequential()
    model.add(LSTM(512,
                   input_shape=(training_input.shape[1], training_input.shape[2]),   # TODO: lern more and fixlen(training_input[0]),),
                   recurrent_dropout=0.2,
                   return_sequences=True))

    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.2,))

    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Activation('relu'))
    model.add(Dense(len(mapping)))
    model.add(Dropout(0.2))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    #TRAINING TIME
    filepath = "TrainingWeights.hdf5"
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
