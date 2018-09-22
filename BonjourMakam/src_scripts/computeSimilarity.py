import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage

def computeSimilarity(newTrack,
         databaseMakam,
         distance_func,
         number_of_bins):
    """
        This method computes the distances of average pitch distributions
        of modes and forms hierarchical clusters based on distances
        of pitch distribution templates
        Parameters
        -------
        features_csv : str
            Name of the csv file containing feature values of instances
        classes_csv : str
            Name of the csv file containing class values of instances
        distance_func : str
            Distance function to use
        number_of_bins : int
            Number of comma values to divide between 0 and 1200 cent
    """


    number_of_tracks = len(databaseMakam)

    newTrackSignificant = newTrack[0:number_of_bins]


    dist_all = []
    for i in range(0, number_of_tracks):
        dist_temp = []
        databaseRowSignificant = databaseMakam[i, 0:number_of_bins]

        for j in range(0, number_of_bins):

            dist_temp.append(
                pdist(np.vstack((newTrackSignificant,
                                 np.roll(databaseRowSignificant,
                                         j,
                                         axis=0))),
                      distance_func))

        dist_all.append(min(dist_temp)[0])

    output = np.concatenate((np.transpose(np.matrix(dist_all)), databaseMakam[:,4]), axis=1)


    ind = output.argsort(axis = 0)
    ind = ind[:,0]
    ind = ind.ravel()
    indArray = np.array(ind)
    orderedOutput = output[indArray]

    return orderedOutput

