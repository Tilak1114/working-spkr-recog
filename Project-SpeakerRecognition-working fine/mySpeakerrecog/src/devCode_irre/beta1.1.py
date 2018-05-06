import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM
from speakerfeatures import extract_features
import os
import warnings
from voice_record import record_audio
from write_to_txt import edit_txt
from write_to_txt import del_txt

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

prefix_test = user_name + "\\Test\\wav\\"

print("Welcome "+user_name)

for i in range(3):   # 3 inputs
    trial = "trial"+str(i+1)
    print(trial)
    f_name = user_name+str(i+1)
    record_audio(f_name, dest_dir_train)  # record audio
    edit_txt(f_name, train_file, prefix_train)   # write to train/enroll.txt

file_paths = open(train_file, 'r')  # read enroll.txt

count = 1

features = np.asarray(())
for path in file_paths:  # iterate 3 times cuz 3 audio files
    path = path.strip()
    print(path)

    # read the audio
    sr, audio = read(source + path)

    # extract 40 dimensional MFCC & delta MFCC features
    vector = extract_features(audio, sr)

    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))
    # when features of 3 files of speaker are concatenated, then do model training
    if count == 3:
        gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)

        # dumping the trained gaussian model
        picklefile = user_name + ".gmm"
        cpk.dump(gmm, open(gmm_dir + picklefile, 'wb'))
        print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
        features = np.asarray(())
        count = 0
    count = count + 1

del_txt(train_file)


# del_txt(test_file)

# validation
f_name1 = user_name+"test"
record_audio(f_name1, dest_dir_test)
edit_txt(f_name1, test_file, prefix_test)

file_paths1 = open(test_file, 'r')

features = np.asarray(())
gmm_files = gmm_dir + user_name + ".gmm"

# Load the Gaussian gender Models
models = cpk.load(open(gmm_files, 'rb'))

# Read the test directory and get the list of test audio files
for path1 in file_paths1:
    print(path1[:-1])
    path1 = path1[:-1]
    (sr, audio) = read(source + path1)
    vector = extract_features(audio, sr)

    log_likelihood = np.zeros(1)
    gmm = models # checking with each model one by one
    scores = np.array(gmm.score(vector))
    log_likelihood[0] = scores.sum()
    print(log_likelihood[0])