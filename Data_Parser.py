import music21
import os

dir = 'CS221_Training_Data'


def convertToString(elem):
    if isinstance(elem, music21.note.Note):
        return elem.name
    elif isinstance(elem, music21.chord.Chord):
        return '.'.join(n.name for n in elem.pitches)
    return 'R'

def getNotes(maxlen):
    inputs = []
    outputs = []
<<<<<<< HEAD
    unique_notes = []
=======
>>>>>>> 557f35282a14959f53e1227aab575e2d4c1017b5
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
                for j in range(i, i + maxlen + 1):
<<<<<<< HEAD
                    note = convertToString(raw_notes[j])
                    if note not in unique_notes:
                        unique_notes.append(note)
                    sequence.append(note)
                inputs.append(sequence)
                note = convertToString(raw_notes[i + maxlen + 1])
                if note not in unique_notes:
                    unique_notes.append(note)
                outputs.append(convertToString(note))
        except:
            continue
    mapping = {note: num for num, note in enumerate(unique_notes)}
    print(mapping)
    return inputs, outputs, mapping
=======
                    sequence.append(convertToString(raw_notes[j]))
                inputs.append(sequence)
                outputs.append(convertToString(raw_notes[i + maxlen + 1]))
        except:
            continue
    return inputs, outputs
>>>>>>> 557f35282a14959f53e1227aab575e2d4c1017b5
