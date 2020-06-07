import music21
import os

training_dir = 'CS221_Training_Data'
testing_dir = 'CS221_Testing_Data'


def convertToString(elem):
    if isinstance(elem, music21.note.Note):
        return elem.name
    elif isinstance(elem, music21.chord.Chord):
        return '.'.join(n.name for n in elem.pitches)
    return 'R'


def extractSequences(dir, unique_notes, maxlen):
    inputs = []
    outputs = []
    for song in os.listdir(dir):
        try:
            midi = music21.converter.parse(dir + '/' + song)
            raw_notes = None
            try:
                s2 = music21.instrument.partitionByInstrument(midi)
                raw_notes = s2.parts[0].recurse()
            except:
                raw_notes = midi.flat.notes
            for i in range(len(raw_notes) - maxlen - 1):
                sequence = []
                for j in range(i, i + maxlen):
                    note = convertToString(raw_notes[j])
                    if note not in unique_notes:
                        unique_notes.append(note)
                    sequence.append(note)
                inputs.append(sequence)
                output = convertToString(raw_notes[i + maxlen + 1])
                if output not in unique_notes:
                    unique_notes.append(output)
                outputs.append(output)
        except:
            continue
    return inputs, outputs

def getNotes(maxlen, train):
    unique_notes =[]
    training_input, training_output = extractSequences(training_dir, unique_notes, maxlen)
    testing_input, testing_output = extractSequences(testing_dir, unique_notes, maxlen)
    mapping = {note: num for num, note in enumerate(unique_notes)}
    if train:
        return training_input, training_output, mapping
    return testing_input, testing_output, mapping
