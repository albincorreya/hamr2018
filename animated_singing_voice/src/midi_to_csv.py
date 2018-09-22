import argparse

import numpy as np
import pandas as pd
import pretty_midi

from utils import pitch_to_freq


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MIDI (single part) to CSV '
                                     '(with time, frequency values in a given sampling rate)\n\n'
                                     'e.g.: python midi_to_csv.py data/aintMisbehavin.midi '
                                     'output/aintMisbehavin_freq_midi.csv')
    parser.add_argument('midi', help='Path to MIDI file')
    parser.add_argument('out', help='Path to CSV file to be written')
    parser.add_argument('--samplerate', help='args.samplerate of file to be written (default: 86.1328125)',
                        type=float, default=86.1328125)
    args = parser.parse_args()

    midi_data = pretty_midi.PrettyMIDI(args.midi)
    assert len(midi_data.instruments) == 1
    midi_instrument = midi_data.instruments[0]

    max_time = max(note.end for note in midi_instrument.notes)
    midi_freq = np.zeros(int(np.ceil(args.samplerate * max_time)))
    midi_times = np.arange(len(midi_freq)) / args.samplerate

    for note in midi_instrument.notes:
        start = note.start
        end = note.end
        freq = pitch_to_freq(note.pitch)

        start_idx = int(np.ceil(args.samplerate * start))
        end_idx = int(np.floor(args.samplerate * end))

        midi_freq[start_idx:end_idx] = freq

    df = pd.DataFrame({'time': midi_times, 'freq': midi_freq})
    df.to_csv(args.out, float_format='%.5f', index=False)
