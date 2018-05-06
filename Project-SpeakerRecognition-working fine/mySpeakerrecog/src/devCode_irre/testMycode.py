import os
import pickle as cpk
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
from voice_record import record_audio
from write_to_txt import enroll_edit
import time

def train():
    warnings.filterwarnings("ignore")

    # path to training data
    source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\Training\\"

    modelpath = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\TestSource\\"

    dest_dir = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\Tilak\\wav\\"

    test_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\18apr2018\\test.txt"

    prefix = "Tilak\\wav\\"

    file_paths = open(test_file, 'r')

    record_audio("testVoice", dest_dir)
    enroll_edit("testVoice", test_file, prefix)

    gmm_files = [os.path.join(source, fname) for fname in
                 os.listdir(source) if fname.endswith('.gmm')]

    # load model

    models = [cpk.load(open(fname, 'rb')) for fname in gmm_files]
    speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname
                in gmm_files]

    sr, audio = read(dest_dir + "testVoice.wav")
    vector = extract_features(audio, sr)

