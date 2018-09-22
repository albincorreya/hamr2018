from util import *
from char_duration_calc2 import *

#    song_name = 'Carly_Rae_Jepsen_-_Call_Me_Maybe'
#    song_name = '2pac_-_Let_Em_Have_It'
#    words_lyric_path = 'lyric_database/aligned/Test/Rap/{}.words'.format(song_name)


text_verse = 'We were the kings and queens of promise We were the victims of ourselves'
generative_text = 'We Have only broken our dreams'
generative_other = 'bad and this is crazy but you look right'
generative_rap = 'You want it for a long time'
text = generative_other


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
make_music(file_name)
