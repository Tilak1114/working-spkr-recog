import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM
from speakerfeatures import extract_features
import warnings

warnings.filterwarnings("ignore")

# path to training data
source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\"

# path where training speakers will be saved
dest = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\"

train_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\enroll.txt"

file_paths = open(train_file, 'r')

count = 1

# Extracting features for each speaker (5 files per speakers)
features = np.asarray(())
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
    if count == 1:
        gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)

        # dumping the trained gaussian model
        temp_path = path
        temp_path = path.strip(".wav")

        picklefile = temp_path + ".gmm"
        cpk.dump(gmm, open(dest + picklefile, 'wb'))
        print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
        features = np.asarray(())
        count = 0
    count = count + 1
