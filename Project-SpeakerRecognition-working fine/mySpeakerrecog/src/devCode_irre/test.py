import os
import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
import time

warnings.filterwarnings("ignore")


# path to training data
source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\development_set\\"

modelpath = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\development_set\\"

test_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\SpeakerID\\development_set_test.txt"

file_paths = open(test_file, 'r')

gmm_files = [os.path.join(modelpath, fname) for fname in
             os.listdir(modelpath) if fname.endswith('.gmm')]

# Load the Gaussian gender Models
models = [cpk.load(open(fname, 'rb')) for fname in gmm_files]
speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname
            in gmm_files]

# Read the test directory and get the list of test audio files
for path in file_paths:

    path = path.strip()
    print(path)
    (sr, audio) = read(source + path)
    vector = extract_features(audio, sr)

    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i] # checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        print(log_likelihood[i])
    winner = np.argmax(log_likelihood)

    '''print(winner)
    print("\tdetected as - ", speakers[winner])
    time.sleep(1.0)'''
