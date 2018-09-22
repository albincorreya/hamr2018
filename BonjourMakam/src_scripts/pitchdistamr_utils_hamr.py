import os
import csv
import argparse
from sklearn.preprocessing import Normalizer
import matplotlib.pyplot as plt
import itertools
import numpy as np
import pandas as pd

def get_args_compute_pitch_distribution_hamr():
    """ Argument parser for computepitchdistribution.py

        Returns
        -------
        dictionary : dict
            number_of_bins : int
                Number of comma values to divide between 0 and 1200 cent
            pct : float
                Percentage value for the first and the last sections
            file_path : str
                Directory of the recordings
            features_save_name : str
                File name for storing feature values
    """
    parser = argparse.ArgumentParser(description='This method computes pitch '
                                                 'distributions of target '
                                                 'recordings and aligns the '
                                                 'obtained distributions with'
                                                 ' respect to the tonic '
                                                 'frequency. The obtained '
                                                 'distributions are saved as '
                                                 'a csv file. ')
    parser.add_argument('-n',
                        '--number_of_bins',
                        type=int,
                        help='Number of comma values to divide between '
                             '0 and 1200 cent. Type is integer. '
                             'Default is 53.',
                        default=53)
    parser.add_argument('-p',
                        '--pct',
                        type=int,
                        default=10,
                        help='Percentage value for the first and '
                             'the last sections. Type is integer.'
                             'Default is 10.')
    parser.add_argument('-d',
                        '--file_path',
                        type=str,
                        default='test_file.wav',
                        help='Directory of the files. '
                             'Type is string. Default is '
                             'test_file.wav')
    parser.add_argument('-fs',
                        '--features_save_name',
                        type=str,
                        default='feature_values_hamr.csv',
                        help='File name for storing feature values. '
                             'Type is string. Default is feature_values.csv')

    args = parser.parse_args()

    return {'number_of_bins': args.number_of_bins,
            'pct': args.pct,
            'file_path': args.file_path,
            'features_save_name': args.features_save_name,
            }

def get_args_compare_two_modes():
    """ Argument parser for comparetwomodes.py

        Returns
        -------
        dictionary : dict
            first_mode : str
                Name of the first mode to plot pitch histogram
            second_mode : str
                Name of the second mode to plot pitch histogram
            number_of_bins : int
                Number of comma values to divide between 0 and 1200 cent
            first_last_pct : int
                Whether to include the first and the last sections
            features_csv : str
                Name of the csv file containing feature values of instances
            classes_csv : str
                Name of the csv file containing class values of instances

    """
    parser = argparse.ArgumentParser(description='This method plots the '
                                                 'average pitch histograms '
                                                 'of given modes in order '
                                                 'to compare them')
    parser.add_argument('-fm',
                        '--first_mode',
                        type=str,
                        help='Target directory for the downloaded files.'
                             'Type is string.',
                        required=True
                        )
    parser.add_argument('-sm',
                        '--second_mode',
                        type=str,
                        help='Target directory for the downloaded files.'
                             'Type is string.',
                        required=True
                        )
    parser.add_argument('-n',
                        '--number_of_bins',
                        type=int,
                        help='Number of comma values to divide between '
                             '0 and 1200 cent. Type is integer. '
                             'Default is 53.',
                        default=53)
    parser.add_argument('-f',
                        '--first_last_pct',
                        type=int,
                        default=1,
                        choices=(0, 1),
                        help='If 1, use the first and the last sections. '
                             'If 0, only the entire recording. '
                             'Default is 1.')
    parser.add_argument('-fn',
                        '--features_csv',
                        type=str,
                        default='feature_values.csv',
                        help='Name of the csv file containing feature values '
                             'of instances. Type is string. Default is '
                             'feature_values.csv')
    parser.add_argument('-cn',
                        '--classes_csv',
                        type=str,
                        default='class_values.csv',
                        help='Name of the csv file containing class values '
                             'of instances. '
                             'Type is string. Default is class_values.csv')
    args = parser.parse_args()

    return {'first_mode': args.first_mode,
            'second_mode': args.second_mode,
            'number_of_bins': args.number_of_bins,
            'first_last_pct': args.first_last_pct,
            'features_csv': args.features_csv,
            'classes_csv': args.classes_csv}

def convert_to_cent(pitch_hz, tonic):
    """Converting the pitch values from frequency to cent

        Parameters
        ----------
        pitch_hz : numpy.array
            Frequency values of the pitch
        tonic : float or str
            Tonic frequency to use

        Returns
        -------
        cent_val : numpy.array
            Cent values of the pitch relative to the tonic
    """
    cent_val = 1200 * np.log2(pitch_hz / np.float(tonic))

    # folding the values into the range (0, 1200)
    for k in range(0, cent_val.size):
        while cent_val[k] < 0:
            cent_val[k] = cent_val[k] + 1200
        while cent_val[k] >= 1200:
            cent_val[k] = cent_val[k] - 1200

    return {'cent_val': cent_val}


def write_to_csv_hamr(file_name, column_names, values):
    """Writing the input data into a csv file and store it
       in 'data/csv_file/' directory

        Parameters
        ----------
        file_name : str
            Name of the csv file
        column_names : numpy.ndarray
            Names of the columns
        values : numpy.array
            Values to write

    """
    target_dir = 'data/csv_files/'
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    with open(target_dir + file_name, 'w') as csv_:
        writer = csv.writer(csv_, dialect='excel')

        writer.writerow(column_names[0])
        writer.writerow(values)

def load_data(features_csv='feature_values.csv',
              classes_csv='class_values.csv'):
    """Loading data from csv files stored in 'data/csv_files/' directory

        Parameters
        ----------
        features_csv : str
            Name of the file that contains feature values
        classes_csv : str
            Name of the file that contains class values

        Returns
        -------
        features : numpy.ndarray
            Feature values obtained from the file
        classes : numpy.ndarray
            Class values obtained from the file
    """
    features_dir = 'data/csv_files/' + features_csv
    classes_dir = 'data/csv_files/' + classes_csv
    features = \
        Normalizer(norm='max').fit_transform(pd.read_csv(features_dir))
    classes = np.ravel(pd.read_csv(classes_dir))

    return {'features': features,
            'classes': classes}
