import numpy as np
import os
import warnings
from voice_record import record_audio
from write_to_txt import edit_txt
from write_to_txt import del_txt
import pickle as cpk
from scipy.io.wavfile import read
from sklearn.mixture import GMM
from speakerfeatures import extract_features
import random
import time

warnings.filterwarnings("ignore")


def rand_phrase():
    list_keyphrases = ['bruce wayne', 'superman', 'the flash', 'cyborg', 'wonder woman', 'iron man', 'captain america',
                       'thor']
    secure_random = random.SystemRandom()
    key_phrase = secure_random.choice(list_keyphrases)
    return key_phrase


def enroll(user_name):

    source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Enroll\\"

    os.makedirs("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Enroll\\" + user_name + "\\wav\\")

    train_dir = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Enroll\\" + user_name + "\\wav\\"

    gmm_dir = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Enroll\\" + user_name + "\\"

    prefix_train = user_name + "\\wav\\"

    f = open("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Enroll\\" + user_name + "\\enroll.txt", 'w')

    enroll_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Enroll\\" + user_name + "\\enroll.txt"

    global logavg

    print("Welcome"+user_name)

    for i in range(3):
        trial = "trial" + str(i + 1)
        print(trial)
        key_phrase = rand_phrase()
        print("Please say '" + key_phrase + "' once the system starts listening")
        time.sleep(2)
        f_name = user_name + str(i + 1)
        record_audio(f_name, train_dir)
        edit_txt(f_name, enroll_file, prefix_train)

    file_paths = open(enroll_file, 'r')
    file_paths1 = open(enroll_file, 'r')

    count = 1

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
            picklefile = user_name + ".gmm"
            cpk.dump(gmm, open(gmm_dir + picklefile, 'wb'))
            print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
            features = np.asarray(())
            count = 0
        count = count + 1

    gmm_files = gmm_dir + user_name + ".gmm"
    models = cpk.load(open(gmm_files, 'rb'))

    logsum = 0

    for path1 in file_paths1:
        path1 = path1.strip()
        print(path1)
        (sro, audioo) = read(source + path1)
        vector_o = extract_features(audioo, sro)

        log_likelihood_orig = np.zeros(1)
        gmm = models  # checking with each model one by one
        scores = np.array(gmm.score(vector_o))
        log_likelihood_orig[0] = scores.sum()
        print(log_likelihood_orig[0])
        logsum = logsum + log_likelihood_orig[0]
    logavg = logsum/3
    print(logavg)
    del_txt(enroll_file)
    return logavg


def validate(user_name):

    source = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Test\\"

    os.makedirs("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Test\\" + user_name + "\\wav\\")

    f = open("C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Test\\" + user_name + "\\test.txt", 'w')

    test_file = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Test\\" + user_name + "\\test.txt"

    dir_test = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Test\\" + user_name + "\\wav\\"

    gmm_dir = "C:\\Users\\Tilak1114\\Desktop\\DEVHACK2018\\22apr2018\\Enroll\\" + user_name + "\\"

    prefix_test = user_name + "\\wav\\"

    f_name1 = user_name + "test"
    record_audio(f_name1, dir_test)
    edit_txt(f_name1, test_file, prefix_test)

    file_paths1 = open(test_file, 'r')

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
        gmm = models  # checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[0] = scores.sum()
        print(log_likelihood[0])
    if ((logavg/log_likelihood[0])*100) > 50:
        print("legit user")
    else:
        print("Invalid user")
# enroll speakers by choosing '1' and test using '2'


flag = 1

while flag:
    print("Select:")
    print("1. Enroll")
    print("2. Verify")
    choice = input()
    choice = int(choice)
    if choice == 1:
        print("Enrollment...")
        user_name = input("Enter username")
        enroll(user_name)
    elif choice == 2:
        print("Verification...")
        user_name = input("Enter username")
        validate(user_name)
        flag = 0
    else:
        print("Invalid choice")
