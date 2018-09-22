#!/usr/bin/env pyt
import numpy as np
import pandas as pd
import subprocess
from util import *

audiofile = 'songs_wav/Carly_Rae_Jepsen_-_Call_Me_Maybe_original.wav'
sentences_lyric_path = 'lyric_database/Carly_Rae_Jepsen_-_Call_Me_Maybe_original.srt'


  

sentences, start, end = split_song_to_sentenceMusic(sentences_lyric_path,audiofile)
df = pd.DataFrame([start, end, sentences])
test_input = 'Try to chase me\nSo call me, maybe\nHey I just met you\n'
file_name = find_sentenceMusic(test_input, sentences, start, end, df)
make_sentence_music(file_name)