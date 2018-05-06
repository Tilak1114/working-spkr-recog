import os
import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
import time

warnings.filterwarnings("ignore")


# path to training data
source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\"

modelpath = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\ariyan\\wav\\"

modelpath1 = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\"

test_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\eureka\\test.txt"

file_paths = open(test_file, 'r')

gmm_files = [os.path.join(modelpath, fname) for fname in
             os.listdir(modelpath) if fname.endswith('.gmm')]

gmm_files1 = [os.path.join(modelpath1, fname) for fname in
             os.listdir(modelpath1) if fname.endswith('.gmm')]

# Load the Gaussian gender Models
models = [cpk.load(open(fname, 'rb')) for fname in gmm_files]

models1 = [cpk.load(open(fname1, 'rb')) for fname1 in gmm_files1]

speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname
            in gmm_files]

# Read the test directory and get the list of test audio files
for path in file_paths:

    path = path.strip()
    print(path)
    (sr, audio) = read(source + path)
    vector = extract_features(audio, sr)

    log_likelihood = np.zeros(len(models))

    log_likelihood1 = np.zeros(len(models1))

    for i in range(len(models)):
        gmm = models[i] # checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        gmm1 = models1[i]
        scores1 = np.array(gmm1.score(vector))
        log_likelihood1[i] = scores1.sum()
        if log_likelihood[i]<log_likelihood1[i]:
            lr = (log_likelihood1[i])/(log_likelihood[i])
        else:
            lr = (log_likelihood[i]) / (log_likelihood1[i])
        print(lr)
    '''winner = np.argmax(log_likelihood)
    print(winner)
    print("\tdetected as - ", speakers[winner])
    time.sleep(1.0)'''
