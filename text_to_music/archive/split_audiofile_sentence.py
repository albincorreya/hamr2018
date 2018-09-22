
import subprocess


#audiofile = 'songs_wav/30_Seconds_to_Mars_-_Kings_and_Queens.wav'
audiofile = 'songs_wav/Carly_Rae_Jepsen_-_Call_Me_Maybe_original.wav'
text_verse = 'We were the kings and queens of promise We were the victims of ourselves'
generative_text = 'We Have only broken our dreams'
generative_other = 'Into the night'
text = generative_other
words_lyric_path = 'lyric_database/aligned/Test/Sing/30_Seconds_to_Mars_-_Kings_and_Queens.words'
sentences_lyric_path = 'lyric_database/Carly_Rae_Jepsen_-_Call_Me_Maybe_original.srt'

def split_song_to_wordMusic(words_lyric_path,output_path='songs_wav/result/'):
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
                subprocess.run(['sox',audiofile,'{}_{}_{}.wav'.format(output_path,start[-1],end[-1],words[-1]),'trim',str(start[-1]),'='+str(end[-1])])
    return words,start,end

def split_song_to_sentenceMusic(sentences_lyric_path, audiofile,output_path='songs_wav/result2/'):
    sentences = []
    starts = []
    ends = []
    with open(sentences_lyric_path) as f:
        for i, line in enumerate(f):
            print(data)
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
                sentences.append(line)
                
            if i % 4 == 3:
                #subprocess.run(['sox', audiofile, '{}_{}_{}.wav'.format(output_path, starts[-1], ends[-1], sentences[-1]), 'trim', str(starts[-1], '='+str(ends[-1]))])
                subprocess.run(['sox', audiofile, output_path + '{}_{}_{}.wav'.format(starts[-1], ends[-1], sentences[-1]), 'trim', str(starts[-1]), '='+str(ends[-1])])

    return sentences, starts, ends

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
