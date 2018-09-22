
import numpy as np
import essentia.standard as ess
from utils import pitch_to_freq


def vibrato_ZeroCrossingRate(pitch_midi, pitch_dgm, vibrato_threshold):
    '''
    This function takes the pitch_midi & pitch_dgm arrays as input (see intonation.ipynb)
    and returns the onset indexes of the notes with vibratos which are detected using ZeroCrossingRates.
    '''

    sr = 44100
    for i in range(len(pitch_midi)):
        pitch_midi[i] = np.nan_to_num(pitch_midi[i])
        pitch_dgm[i] = np.nan_to_num(pitch_dgm[i])

    freqs_dgm = []
    for i in range(len(pitch_dgm)):
        freq = pitch_to_freq(pitch_dgm[i])
        freqs_dgm.append(freq)

    notes = []
    freqs = []
    vibratos =[]

    for i in range(1,len(pitch_midi)):

        if pitch_midi[i] != pitch_midi[i-1]:
            duration = len(notes)*86.1328125/sr

            if freqs:
                medianFreq = np.median(freqs)
                zrc = ess.ZeroCrossingRate(threshold = medianFreq)(freqs)

            if zrc > duration* vibrato_threshold : #threshold set experimentally
                vibratos.append(pitch_dgm[i])

            else:
                vibratos.append(0)
                notes = []
                freqs = []

        if pitch_midi[i] == pitch_midi[i-1]:
            notes.append(pitch_midi[i])
            freqs.append(freqs_dgm[i])
            vibratos.append(0)


    vibratos.insert(0,0)

    vibrato_onsets=[]
    for i in range(len(vibratos)):
        if vibratos[i] == 0 :
            vibratos[i] = np.nan

    return(vibratos)

def ExtractResidualFeatures(audioFile, params):

    fs = params.fs

    audio = ess.MonoLoader(filename = audioFile, sampleRate = fs)()
    audio = ess.DCRemoval()(audio) ##preprocessing / apply DC removal for noisy regions
    audio = ess.EqualLoudness()(audio)
    #audio = ess.HighPass(cutoffFrequency=200)(audio)

    windowSize=int(params.windowSize/2)*2 #assuring window size is even
    hopSize=int(params.hopSize/2)*2 #assuring hopSize is even

    zeroCrossingRateArray = []
    energyArray = []
    instantPowerArray = []
    rmsArray = []
    fluxArray = []

    for frame in ess.FrameGenerator(audio, frameSize=windowSize, hopSize=hopSize, startFromZero=True):
        frame=ess.Windowing(size=windowSize, type=params.windowFunction)(frame)
        mX = ess.Spectrum(size=params.fftN)(frame)
        #mX[mX<np.finfo(float).eps]=np.finfo(float).eps

        zeroCrossingRate = ess.ZeroCrossingRate()(frame)
        energy = ess.Energy()(frame)
        instantPower = ess.InstantPower()(frame)
        rms = ess.RMS()(frame)
        flux = ess.Flux()(mX)

        zeroCrossingRateArray.append(zeroCrossingRate)
        energyArray.append(energy)
        instantPowerArray.append(instantPower)
        rmsArray.append(rms)
        fluxArray.append(flux)

    return zeroCrossingRateArray, energyArray, instantPowerArray, rmsArray, fluxArray
