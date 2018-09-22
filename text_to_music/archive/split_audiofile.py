import subprocess
from util import *

audiofile = 'songs_wav/30_Seconds_to_Mars_-_Kings_and_Queens.wav'
text_verse = 'We were the kings and queens of promise We were the victims of ourselves'
generative_text = 'We Have only broken our dreams'
generative_other = 'Into the night'
text = generative_other
words_lyric_path = 'lyric_database/aligned/Test/Sing/30_Seconds_to_Mars_-_Kings_and_Queens.words'

def split_song_to_wordMusic(words_lyric_path):
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
            if(words[-1] != 'OH' or words[-1] != 'sp'):
                subprocess.run(['sox',audiofile,'songs_wav/result/{}_{}_{}.wav'.format(start[-1],end[-1],words[-1]),'trim',str(start[-1]),'='+str(end[-1])])
    return words,start,end



def find_wordMusic(text,words,start,end):
    token = text.split(' ')
    file_name = []
    for tok in token:
        ind_list = [i for i,w in enumerate(words) if(tok.upper() == w)]
        length_list = [end[i]-start[i] for i in ind_list]
        ind_dict = dict(zip(ind_list,length_list))
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
    

words,start,end = split_song_to_wordMusic(words_lyric_path)
file_name = find_wordMusic(text_verse,words,start,end)
make_music(file_name)
