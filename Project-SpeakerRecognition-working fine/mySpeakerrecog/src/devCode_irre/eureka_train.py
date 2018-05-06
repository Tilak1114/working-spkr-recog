import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM
from speakerfeatures import extract_features
import warnings

warnings.filterwarnings("ignore")

# path to training data
source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\"

# path where training speakers will be saved
dest = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\"

dest_test = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\"

train_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\train.txt"

test_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\test.txt"

file_paths = open(train_file, 'r')

file_paths1 = open(test_file, 'r')
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
    # when features of 3 files of speaker are concatenated, then do model training
    if count == 3:
        gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)

        # dumping the trained gaussian model
        picklefile = "ariyan\\wav\\BGM" + ".gmm"
        print(picklefile)
        cpk.dump(gmm, open(dest + picklefile, 'wb'))
        print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
        features = np.asarray(())
        count = 0
    count = count + 1

ind = 0

for path1 in file_paths1:
    path1 = path1.strip()
    print(path1)

    # read the audio
    sr, audio = read(source + path1)

    # extract 40 dimensional MFCC & delta MFCC features
    vector = extract_features(audio, sr)

    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))
    # when features of 1 files of speaker are concatenated, then do model training
    if count == 1:
        gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)

        # dumping the trained gaussian model
        picklefile = "target" + str(ind) + ".gmm"
        print(picklefile)
        cpk.dump(gmm, open(dest + picklefile, 'wb'))
        print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
        features = np.asarray(())
        count = 0
        ind = ind + 1
    count = count + 1
