import numpy as np
import begin
import pickle
import cv2


class PadProcessor:

    def __init__(self, pad):
        self.pad = pad

    def __call__(self, data):
        pad_start = np.repeat(data[:1], self.pad, axis=0)
        pad_stop = np.repeat(data[-1:], self.pad, axis=0)
        return np.concatenate((pad_start, data, pad_stop))


def _make_preprocessor(settings, pad):
    from madmom.audio.spectrogram import (
        LogarithmicFilteredSpectrogramProcessor,
        SpectrogramDifferenceProcessor)
    from madmom.audio.filters import LogarithmicFilterbank
    from madmom.audio.signal import SignalProcessor, FramedSignalProcessor
    from madmom.audio.stft import ShortTimeFourierTransformProcessor
    from madmom.processors import SequentialProcessor

    sig = SignalProcessor(num_channels=1, sample_rate=settings['sample_rate'])
    frames = FramedSignalProcessor(frame_size=settings['frame_size'], fps=settings['fps'])
    stft = ShortTimeFourierTransformProcessor()  # caching FFT window
    spec = LogarithmicFilteredSpectrogramProcessor(
        num_channels=1, sample_rate=settings['sample_rate'],
        filterbank=LogarithmicFilterbank, frame_size=settings['frame_size'], fps=settings['fps'],
        num_bands=settings['num_bands'], fmin=settings['fmin'], fmax=settings['fmax'],
        norm_filters=settings['norm_filters'])
    if settings['diff']:
        if 'pad' in settings and settings['pad']:
            stack = _crnn_drum_processor_stack
        else:
            stack = np.hstack
        diff = SpectrogramDifferenceProcessor(
            diff_ratio=0.5, positive_diffs=True,
            stack_diffs=stack)
        # process input data
        if pad > 0:
            pre_processor = SequentialProcessor(
                (sig, frames, stft, spec, diff, PadProcessor(pad)))
        else:
            pre_processor = SequentialProcessor((sig, frames, stft, spec, diff))

    else:
        if pad > 0:
            pre_processor = SequentialProcessor(
                (sig, frames, stft, spec, PadProcessor(pad)))
        else:
            pre_processor = SequentialProcessor((sig, frames, stft, spec))

    return pre_processor


ISMIR18_7_SET = {'beat_targ': False,
 'diff': False,
 'drum_annot': 'm',
 'drum_targ': True,
 'fmax': 15000,
 'fmin': 30,
 'fps': 100,
 'frame_size': 2048,
 'name': 'feat_ismir18_7',
 'norm_filters': True,
 'num_bands': 12,
 'pad': False,
 'sample_rate': 44100,
 'soft_target': 0,
 'start_silence': 0.25,
 'target_shift': 0.0}


def compute_activations(audio_file):
    preproc = _make_preprocessor(ISMIR18_7_SET, 12)
    nn = pickle.load(open('madmom-0.16.dev0/madmom/models/drums/2018/drums_cnn0_O8_S2.pkl'))
    nn.layers = nn.layers[:-8]

    spec = preproc(audio_file)
    output = nn(spec)
    output = output.reshape(output.shape[0], -1)
    return output


@begin.start
def main(audio_file, video_file, save_activations=False):

    output = compute_activations(audio_file)

    if save_activations:
        np.save(video_file, output)
        return 0

    from sklearn.cluster import KMeans
    z = (output - output.mean(0, keepdims=True)) / \
          np.maximum(0.0001, output.std(0, keepdims=True))
    clusters = KMeans(4).fit(abs(z).T).predict(abs(z).T)
    exclude_cluster = np.bincount(clusters).argmax()

    img = []
    for c in range(4):
        if c == exclude_cluster:
            continue
        img.append(np.hstack([output[:, clusters == c]] * 10)[:, :256].reshape(-1, 16, 16))

    img = np.stack(img, axis=-1)
    print img.shape
    img[..., 1] = 1.0
    img[..., 2] = 1.0

    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video_writer = cv2.VideoWriter(video_file, fourcc, 100, (16, 16))
    for i in range(len(img)):
        frame = cv2.cvtColor((img[i] * 255).astype(np.uint8), cv2.COLOR_HSV2RGB)
        video_writer.write(frame.astype(np.uint8))
    video_writer.release()




