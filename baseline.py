import music21
import random
FILE_NAME = 'shape_of_you.mid'
"""
clear goal for baseline:

1. make a list of notes along 2 consecutive octaves (the 2 middle octaves
or sum else, or within 1 key)
1b. add "rest" to our list of notes so the thing rests...

2. program something that picks randomly from this set of notes for however
many notes we want baseline song to go for
2b. create stream object and append notes to the stream

DONT NEED: actual midi files/songs yet
"""

NOTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_NOTES = 50
NUM_OCTAVES = 2
START_OCTAVE = 4

def generateBaselineNotes():
    midi = music21.converter.parse(FILE_NAME)
    baseLineNotes = []
    notes_to_parse = None
    output_midi = music21.stream.Stream()

    instruments = music21.instrument.partitionByInstrument(midi)
    print("Instruments has %s elements" %(len(instruments)))
    print(instruments.parts)
    for part in instruments:
        if isinstance(part.getInstrument(), music21.instrument.Flute):
            print(part)
        print(part.getInstrument())
    notes_to_parse = instruments.parts[0].recurse()
    #except: # file has notes in a flat structure
        # notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, music21.note.Note):
            baseLineNotes.append(str(element.pitch))
            output_midi.append(element)
            # output_midi.append(music21.note.Note(str(element.pitch)))
        elif isinstance(element, music21.chord.Chord):
            print(str(element))
            baseLineNotes.append('.'.join(str(n) for n in element.normalOrder))
            # output_midi.append(music21.chord.Chord(str(element.pitch)))
            output_midi.append(element)

    # TODO: try making a distribution and sampling from there?

    print(baseLineNotes)  # this is just for us to test what notes have been added
    return output_midi
    # for i in range(START_OCTAVE,START_OCTAVE + NUM_OCTAVES):
    #     for j in range(len(NOTES)):
    #         baselineNotes.append(NOTES[j] + str(i))
    # # baselineNotes.append('R')
    # return baselineNotes

def main():
    stream = generateBaselineNotes()
    # s = music21.stream.Stream()
    # for i in range(NUM_NOTES):
    #     note = music21.note.Note(random.choice(baseLineNotes))
    #     s.append(note)
    #     # note.show('midi')
    stream.write('midi', fp='ed_sheeran_output.mid')
    # s.show('midi')

if __name__ == '__main__':
    main()
