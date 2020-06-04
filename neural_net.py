#import keras
from Data_Parser import getNotes

SEQUENCE_LEN = 20

def main():
    input, output, mapping = getNotes(SEQUENCE_LEN)
    # unique_notes = {note: num for num, note enumerate(input | output)}
    training_input = [[mapping[note] for note in sequence] for sequence in input]
    training_output = [mapping[note]for note in output]
    # training_map = dict(note: number for number, note in enumerate(unique_notes))


# A B C D E F G
# input[0] = [A,B,C] output[0] = D
# input[1] = [B, C, D] output[1] = E

if __name__ == '__main__':
    main()
