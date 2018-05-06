import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM
from speakerfeatures import extract_features
import warnings
from voice_record import record_audio
from write_to_txt import enroll_edit
warnings.filterwarnings("ignore")

source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\"

dest = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\"

dest_dir = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\Tilak\\wav\\"

train_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\enroll.txt"

prefix = "Tilak\\wav\\"

features = np.asarray(())

user_name = input("Enter username")
print("Welcome "+user_name)
for i in range(3):
    trial = "trial"+str(i+1)
    print(trial)
    f_name = user_name+str(i+1)
    record_audio(f_name, dest_dir)
    enroll_edit(f_name, train_file, prefix)

file_paths = open(train_file, 'r')

count = 1

for path in file_paths:
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
    # when features of 5 files of speaker are concatenated, then do model training
    if count == 3:
        gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)

        # dumping the trained gaussian model
        temp_path = path.strip(".wav")
        picklefile = temp_path.strip("3") + ".gmm"
        cpk.dump(gmm, open(dest + picklefile, 'wb'))
        print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
        features = np.asarray(())
    count = count + 1
