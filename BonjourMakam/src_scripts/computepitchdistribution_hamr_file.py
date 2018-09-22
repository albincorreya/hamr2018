import numpy as np
from pitchdistamr_utils_hamr import write_to_csv_hamr
from pitchdistamr_utils_hamr import convert_to_cent
from pitchdistamr_utils_hamr import get_args_compute_pitch_distribution_hamr
from external_utilities.pitchfilter import PitchFilter
from external_utilities.toniclastnote import TonicLastNote
from external_utilities.predominantmelodymakam import PredominantMelodyMakam


def main(number_of_bins,
         pct,
         file_path,
         features_save_name):
    """

        This method computes pitch distributions of target recordings
        and aligns the obtained distributions with respect to the tonic
        frequency. The obtained distributions are saved as a csv file.
        To use the mode information specified in annotations file, 'annot'
        should be 1. To use the already extracted pitch values from the
        directory, 'pitch_files' should be 1. To use the already estimated
        tonic frequencies included in annotations
        file, 'annot_tonic' should be 1. For the required folder structure,
        README file can be referred.

        Parameters
        ----------
        number_of_bins : int
            Number of comma values to divide between 0 and 1200 cent
        pct : float
            Percentage value for the first and the last sections
        file_path : str
            Directory of the recordings
        features_save_name : str
            File name for storing feature values

    """

    # creating an array for the column names
    pitch_column_names = np.ndarray(shape=(1, number_of_bins * 3),
                                    dtype='|U16')

    # if the analysis includes the first and the last sections,
    # column names are arranged accordingly
    for k in range(0, number_of_bins):
        pitch_column_names[0][k] = 'FreqBin_' + str(k + 1)
        pitch_column_names[0][k + number_of_bins] \
            = 'FreqBin_FS_' + str(k + 1)
        pitch_column_names[0][k + number_of_bins * 2] \
            = 'FreqBin_LS_' + str(k + 1)

    # initializing array for storing the pitch distribution
    pitch_val = np.zeros(number_of_bins*3)

    # extract the pitch values
    extractor = PredominantMelodyMakam(filter_pitch=False)
    pitch_hz = extractor.run(file_path)['pitch']
    pitch_filter = PitchFilter()
    pitch_hz = pitch_filter.run(pitch_hz)

    # compute the tonic value
    tonic_identifier = TonicLastNote()
    tonic, _, _, _ = tonic_identifier.identify(pitch_hz)
    tonic = tonic['value']

    # discarding the 0 values
    pitch_hz = pitch_hz[pitch_hz != 0]

    # converting the pitch values from frequency to cent
    cent_val = convert_to_cent(pitch_hz, tonic)['cent_val']

    # creating the histogram based on the number of bins
    hist_val, _ = np.histogram(cent_val,
                               bins=number_of_bins)

    # storing the values of the histograms
    pitch_val[: number_of_bins] = hist_val

    # taking values of the first and the last quarters
    pitch_hz_fs \
        = pitch_hz[: np.int(pitch_hz.size * (pct / 100))]
    pitch_hz_ls \
        = pitch_hz[np.int(pitch_hz.size * ((100 - pct) / 100)):]

    # converting the pitch values from frequency to cent
    cent_val_fs = convert_to_cent(pitch_hz_fs, tonic)['cent_val']
    cent_val_ls = convert_to_cent(pitch_hz_ls, tonic)['cent_val']

    # creating the histograms based on the number of bins
    hist_val_fs, _ = np.histogram(cent_val_fs,
                                  bins=number_of_bins)
    hist_val_ls, _ = np.histogram(cent_val_ls,
                                  bins=number_of_bins)

    # storing the values of the histograms
    pitch_val[number_of_bins: (number_of_bins * 2)] \
        = hist_val_fs
    pitch_val[(number_of_bins * 2):(number_of_bins * 3)] \
        = hist_val_ls

    # writing the values to the csv file
    write_to_csv_hamr(features_save_name, pitch_column_names, pitch_val)

    return pitch_val


if __name__ == "__main__":
    args = get_args_compute_pitch_distribution_hamr()
    main(number_of_bins=args['number_of_bins'],
         pct=args['pct'],
         file_path=args['file_path'],
         features_save_name=args['features_save_name']
         )
