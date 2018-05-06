import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
import os
import warnings
from voice_record import record_audio
from write_to_txt import edit_txt
from write_to_txt import del_txt
from sidekit.features_extractor import FeaturesExtractor

warnings.filterwarnings("ignore")

source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\"

train_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\enroll.txt"

features = np.asarray(())

user_name = input("Enter username")

os.makedirs("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Train\\wav\\")

dest_dir_train = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Train\\wav\\"

gmm_dir = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Train\\"


prefix_train = user_name + "\\Train\\wav\\"

os.makedirs("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Test\\wav\\")

test_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\test.txt"

dest_dir_test = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Test\\wav\\"

gmm_dir_test = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\" + user_name + "\\Test\\"

prefix_test = user_name + "\\Test\\wav\\"

print("Welcome "+user_name)

for i in range(3):
    trial = "trial"+str(i+1)
    print(trial)
    f_name = user_name+str(i+1)
    record_audio(f_name, dest_dir_train)
    edit_txt(f_name, train_file, prefix_train)

file_paths = open(train_file, 'r')

count = 1

features = np.asarray(())
for path in file_paths:
    path = path.strip()
    print(path)
    