import numpy as np
from scipy.io.wavfile import read
from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import ssc
import warnings
from voice_record import record_audio
from write_to_txt import edit_txt
from write_to_txt import del_txt
import matplotlib.pyplot as plt

import os

warnings.filterwarnings("ignore")

source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\"

train_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\enroll.txt"

features = np.asarray(())

user_name = input("Enter username")

os.makedirs("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Train\\wav\\")

dest_dir_train = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Train\\wav\\"

prefix_train = user_name + "\\Train\\wav\\"

os.makedirs("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Test\\wav\\")

test_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\test.txt"

dest_dir_test = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Test\\wav\\"

prefix_test = user_name + "\\Test\\wav\\"

print("Welcome "+user_name)

for i in range(3):
    trial = "trial"+str(i+1)
    print(trial)
    f_name = user_name+str(i+1)
    record_audio(f_name, dest_dir_train)
    edit_txt(f_name, train_file, prefix_train)

file_paths = open(train_file, 'r')
dataset = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\dataset.txt"
sum_of_features = 0
list_mfcc_ft = []
list_fbank_ft = []
list_ssc_ft = []
for path in file_paths:
        path = path.strip()
        print(path)
        # read the audio
        sr, audio = read(source + path)
        mfcc_feat = mfcc(audio, sr)
        rows, cols = mfcc_feat.shape
        print(rows)
        print(cols)
del_txt(train_file)

# testing
