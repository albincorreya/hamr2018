import subprocess
import numpy as np
import pandas as pd
import os

def split_song_to_wordMusic(words_lyric_path,audiofile,output_path='songs_wav/result/'):
    words = []
    start = []
    end = []
    with open(words_lyric_path) as f:
        for line in f:
            data = line.strip().split(' ')
            print(data)
            words.append(data[2])
            start.append(float(data[0]))
            end.append(float(data[1]))
#            if(words[-1] != 'OH' and words[-1] != 'sp'):
            subprocess.run(['sox',audiofile,'songs_wav/result/{}_{}_{}.wav'.format(start[-1],end[-1],words[-1]),'trim',str(start[-1]),'='+str(end[-1])])
    return words,start,end



def find_wordMusic(text,words,start,end):
    token = text.split(' ')
    file_name = []
    for tok in token:
        ind_list = [i for i,w in enumerate(words) if(tok.upper() == w)]
        length_list = [end[i]-start[i] for i in ind_list]
        ind_dict = dict(zip(ind_list,length_list))
        print(ind_dict, tok)
        sorted_by_value = sorted(ind_dict.items(), key=lambda kv: kv[1])   
    
        if(len(sorted_by_value) == 1):
            ind = sorted_by_value[0][0]
        else:
            ind = sorted_by_value[int(len(sorted_by_value)/2)][0]
        file_name.append(str(start[ind])+'_'+str(end[ind])+'_'+tok.upper()+'.wav')
    return file_name

def make_music(file_name,output_file = "songs_wav/text_to_music/temp.wav",output_file_cp = "songs_wav/text_to_music/temp_cp.wav"):    
    file1 = file_name[0]
    file2 = file_name[1]
    subprocess.run(['sox','songs_wav/result/'+file1,'songs_wav/result/'+file2,output_file])   
    for i,file in enumerate(file_name[2:]):
        subprocess.run(['cp',output_file,output_file_cp])
        subprocess.run(['sox',output_file_cp,'songs_wav/result/'+file,output_file])   
    return output_file

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

def find_best_wordMusic(words_lyric_path,text,words,start,end):
    token = text.split(' ')
    file_name = []
    char_dur_time = calc_time_per_char(words_lyric_path)
    char_dur_average = calc_avetime_per_char(char_dur_time)
    for tok in token:
        ind_list = [i for i,w in enumerate(words) if(tok.upper() == w)]
        length_list = [end[i]-start[i] for i in ind_list]
        best_word_duration = best_word_time(tok,length_list,char_dur_average)
        ind = ind_list[length_list.index(best_word_duration)]
        file_name.append(str(start[ind])+'_'+str(end[ind])+'_'+tok.upper()+'.wav')
    return file_name


def split_song_to_sentenceMusic(sentences_lyric_path,audiofile, output_path='songs_wav/result3/'):
    sentences = []
    starts = []
    ends = []
    with open(sentences_lyric_path) as f:
        for i, line in enumerate(f):
            print(line)
            if i % 4 == 1:
                start = line.split(' ')[0]
                s0 = float('{:.5}'.format(start.split(':')[0]))
                s1 = float('{:.5}'.format(start.split(':')[1]))
                s2 = float('{:.5}'.format(start.split(':')[2].split(',')[0]))
                s3 = float('{:.5}'.format(start.split(':')[2].split(',')[1]))
                starttime = 3600*s0 + 60*s1 + s2 + s3/1000
                
                end = line.split(' ')[2]
                e0 = float('{:.5}'.format(end.split(':')[0]))
                e1 = float('{:.5}'.format(end.split(':')[1]))
                e2 = float('{:.5}'.format(end.split(':')[2].split(',')[0]))
                e3 = float('{:.5}'.format(end.split(':')[2].split(',')[1]))
                endtime = 3600*e0 + 60*e1 + e2 + e3/1000
                
                duration = endtime - starttime
                
                starts.append(starttime)
                ends.append(endtime)
                
            if i % 4 == 2:
                sentences.append(line.strip())
                
            if i % 4 == 3:
                #subprocess.run(['sox', audiofile, '{}_{}_{}.wav'.format(output_path, starts[-1], ends[-1], sentences[-1]), 'trim', str(starts[-1], '='+str(ends[-1]))])
                subprocess.run(['sox', audiofile, output_path + '{}_{}.wav'.format(starts[-1], ends[-1]), 'trim', str(starts[-1]), '='+str(ends[-1])])

    return sentences, starts, ends

def find_sentenceMusic(text, sentences, start, end, df):
    token = text.split('\n')
    file_name = []
    for tok in token:
        print(tok)
        if tok == '':
            continue
        ind_list = [i for i, w in enumerate(sentences) if(w == tok)]
        length_list = [end[i]-start[i] for i in ind_list]
        ind_dict = dict(zip(ind_list, length_list))
        sorted_by_value = sorted(ind_dict.items(), key=lambda kv: kv[1])
        print(ind_list)
        
        if len(sorted_by_value) == 1:
            ind = sorted_by_value[0][0]
        else:
            ind = sorted_by_value[int(len(sorted_by_value)/2)][0]
        file_name.append(str(start[ind]) +'_'+ str(end[ind])+ '.wav')
    return file_name

    
def make_sentence_music(file_name, output_file='songs_wav/text_to_music/temp_sent.wav', output_file_cp = 'songs_wav/text_to_music/temp_sent_cp.wav'):
    file1 = file_name[0]
    file2 = file_name[1]
    subprocess.run(['sox','songs_wav/result3/'+file1,'songs_wav/result3/'+file2,output_file])   

    for i,file in enumerate(file_name[2:]):
        subprocess.run(['cp',output_file,output_file_cp])
        subprocess.run(['sox',output_file_cp,'songs_wav/result3/'+file,output_file])   
    return output_file


def sentence_to_music(text_input):
    audiofile = 'songs_wav/Carly_Rae_Jepsen_-_Call_Me_Maybe_original.wav'
    sentences_lyric_path = 'lyric_database/Carly_Rae_Jepsen_-_Call_Me_Maybe_original.srt'
    sentences, start, end = split_song_to_sentenceMusic(sentences_lyric_path,audiofile)
    df = pd.DataFrame([start, end, sentences])
    text_input = 'Try to chase me\nSo call me, maybe\nHey I just met you\n'
    file_name = find_sentenceMusic(text_input, sentences, start, end, df)
    output_file = make_sentence_music(file_name)
    cwd = os.getcwd()
 #   cwd = cwd+'/songs_wav/'
    return cwd+'/'+output_file


def words_to_music(text):
    words = []
    start = []
    end = []
    song_list = ['Carly_Rae_Jepsen_-_Call_Me_Maybe','30_Seconds_to_Mars_-_Kings_and_Queens']
    char_dur_average_list = []
    for song_name in song_list:
        words_lyric_path = 'lyric_database/aligned/Test/Sing/{}.words'.format(song_name)
        char_dur_time = calc_time_per_char(words_lyric_path)
        audiofile = 'songs_wav/{}.wav'.format(song_name)
        words_sub,start_sub,end_sub = split_song_to_wordMusic(words_lyric_path,audiofile)
        words += words_sub
        start += start_sub
        end += end_sub
        char_dur_average_list.append(calc_avetime_per_char(char_dur_time))    
    char_dur_average = [sum(x) for x in zip(char_dur_average_list[0], char_dur_average_list[1])]            
    file_name = find_best_wordMusic(words_lyric_path,text,words,start,end)
    output_file = make_music(file_name)
    cwd = os.getcwd()
#    cwd = cwd+'/songs_wav/'
    return cwd+'/'+output_file

