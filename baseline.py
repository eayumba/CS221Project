import music21
import random

"""
clear goal for baseline:

1. make a list of notes along 2 consecutive octaves (the 2 middle octaves
or sum else, or within 1 key)
1b. add "rest" to our list of notes so the thing rests...

2. program something that picks randomly from this set of notes for however
many notes we want baseline song to go for

DONT NEED: actual midi files/songs yet
"""

NOTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_NOTES = 50
NUM_OCTAVES = 2
START_OCTAVE = 4

def generateBaselineNotes():
    baselineNotes = []
    for i in range(START_OCTAVE,START_OCTAVE + NUM_OCTAVES):
        for j in range(len(NOTES)):
            baselineNotes.append(NOTES[j] + str(i))
    # baselineNotes.append('R')
    return baselineNotes

def main():
    baseLineNotes = generateBaselineNotes()
    for i in range(NUM_NOTES):
        note = music21.note.Note(random.choice(baseLineNotes))
        note.show('midi')

if __name__ == '__main__':
    main()
