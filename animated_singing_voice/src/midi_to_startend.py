import argparse

import numpy as np
import pandas as pd
import pretty_midi


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MIDI (single part) to CSV '
                                     '(with start, end, pitch values per note)\n\n'
                                     'e.g.: python midi_to_startend.py data/aintMisbehavin.midi '
                                     'output/aintMisbehavin_startend_midi.csv\n')
    parser.add_argument('midi', help='Path to MIDI file')
    parser.add_argument('out', help='Path to CSV file to be written')
    args = parser.parse_args()

    midi_data = pretty_midi.PrettyMIDI(args.midi)
    assert len(midi_data.instruments) == 1
    midi_instrument = midi_data.instruments[0]

    midi_start = np.zeros(len(midi_instrument.notes))
    midi_end = np.zeros(len(midi_instrument.notes))
    midi_pitch = np.zeros(len(midi_instrument.notes), dtype='int')

    for i, note in enumerate(midi_instrument.notes):
        midi_start[i] = note.start
        midi_end[i] = note.end
        midi_pitch[i] = note.pitch

    df = pd.DataFrame({'start': midi_start, 'end': midi_end, 'pitch': midi_pitch})
    df.to_csv(args.out, float_format='%.5f', index=False)
