
import numpy as np

#audiofile = 'songs_wav/30_Seconds_to_Mars_-_Kings_and_Queens.wav'
#text_verse = 'We were the kings and queens of promise We were the victims of ourselves'
#generative_text = 'We Have only broken our dreams'
#generative_other = 'Into the night'
#text = generative_other
#words_lyric_path = 'lyric_database/aligned/Test/Sing/30_Seconds_to_Mars_-_Kings_and_Queens.words'

def calc_time_per_char(words_lyric_path):
    f = open(words_lyric_path)
    lyric = f.read()
    f.close()
    
    char_dur_time = []
    for i in range(26):
        char_dur_time.append([chr(ord('A') +i)])
    
    lines = lyric.split('\n')
    for line in lines:
        words = line.split(' ')
        if line == '' or words[2] == 'OH' or words[2] == 'sp':
            continue
        start = float('{:.5}'.format(words[0]))
        end = float('{:.5}'.format(words[1]))
        duration_word = end - start
        char_num = len(words[2])
        for c in words[2]:
            char_dur = duration_word / char_num
            if ord(c) - ord('A') < 0 or ord(c) - ord('A') > 25:
                continue
            char_dur_time[ord(c) - ord('A')].append(char_dur)
    return char_dur_time
    
"""
X, Z do not exist in the lyric
"""
def calc_avetime_per_char(char_dur_time):
    char_dur_average = []
    for i in range(26):
        if len(char_dur_time[i]) == 1:
            char_dur_average.append(0)
        else:
            avg_time = np.mean(char_dur_time[i][1:])
            char_dur_average.append(np.mean(avg_time))
    return char_dur_average
        
def time_char(c,char_dur_average):
    print(ord(c))
    print(ord('A'))
    return char_dur_average[ord(c.upper()) - ord('A')]

def time_word(word,char_dur_average):
    duration = 0
    for c in word:
        duration += time_char(c,char_dur_average)
    return duration

def best_word_time(word, timelist,char_dur_average):
    avgtime = time_word(word,char_dur_average)
    
    idx = np.abs(np.asarray(timelist) - avgtime).argmin()
    return timelist[idx]


#char_dur_time = calc_time_per_char(words_lyric_path)
#char_dur_average = calc_avetime_per_char(char_dur_time)
#time_a = [0.5, 1, 1.5]
#print(time_word('WORD'))
#print(best_word_time('WORD', time_a))