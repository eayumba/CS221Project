from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Activation, Dropout, Dense
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from Data_Parser import getNotes
import numpy
import music21
from Data_Parser import getNotes

SEQUENCE_LEN = 20


def main():
    input, output, mapping = getNotes(SEQUENCE_LEN, False)
    test_input = [[mapping[note] for note in sequence] for sequence in input]

    model = rebuild_model(test_input, mapping)
    test_output = [mapping[note]for note in output]
    test_input = numpy.reshape(test_input, (len(test_input), len(test_input[0]), 1))
    test_output = to_categorical(test_output, num_classes = len(mapping))
    #test_output = to_categorical_mod(test_output, mapping)
    results = model.evaluate(test_input, test_output, batch_size=64)
    print(results)
    output = makeNotes(model, test_input, mapping)



def rebuild_model(test_input, mapping):
    # print("len(test_input[0] = ", len(test_input[0]))
    test_input = numpy.reshape(test_input, (len(test_input), len(test_input[0]), 1))
    #training_output = to_categorical(training_output)
    model = Sequential()
    model.add(LSTM(512,
                   input_shape=(test_input.shape[1], test_input.shape[2]),   # TODO: lern more and fixlen(test_input[0]),),
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

    #load weights
    model.load_weights('TrainingWeights.hdf5')

    return model


def makeNotes(model, test_input, mapping):
    start = numpy.random.randint(0, len(test_input)-1)

    int_to_note = dict((mapping[note], note) for note in mapping.keys())
    initial_sequence = test_input[start]
    output = []

    s = music21.stream.Stream()

    for i in range(500):
        prediction_input = numpy.reshape(initial_sequence, (1, len(initial_sequence), 1))
        #prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)
        index = numpy.argmax(prediction)
        # print(index)
        #print(type(prediction))
        #index = weightedRandomChoice(prediction)
        # temp = 0.8
        # prediction = numpy.log(prediction) / 0.8
        # prediction = numpy.exp(prediction) / numpy.sum(numpy.exp(prediction))
        # index = numpy.argmax(numpy.random.multinomial(1, prediction, 1))

        result = int_to_note[index]
        #add the note to output stream
        if len(result) > 1:
            note = music21.chord.Chord(result.split("."))
        elif (result == 'R'):
            note = music21.note.Rest()
        else:
            note = music21.note.Note(result)
        s.append(note)
        output.append(result)

        initial_sequence.append(index)
        initial_sequence = initial_sequence[1:len(initial_sequence)]
    s.write('midi', fp="Sample_Output.mid")

    return output

if __name__ == '__main__':
    main()
