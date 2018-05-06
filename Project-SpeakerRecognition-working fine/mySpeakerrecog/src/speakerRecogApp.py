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
from sms import sendotph
import random
import time
from passphverify import spchrcg

warnings.filterwarnings("ignore")


def rand_phrase_train():
    list_keyphrases = ['bruce wayne', 'superman', 'the flash', 'cyborg', 'wonder woman', 'iron man', 'captain america',
                       'thor']
    secure_random = random.SystemRandom()
    key_phrase = secure_random.choice(list_keyphrases)
    return key_phrase
def rand_phrase_test():
    list_keyphrases = ['I am going to make him an offer he cannot refuse']
    secure_random = random.SystemRandom()
    key_phrase = secure_random.choice(list_keyphrases)
    return key_phrase

def enroll(user_name):

    source_enroll = "..\\Enroll\\"

    os.makedirs("..\\Enroll\\" + user_name + "\\wav\\")

    train_dir = "..\\Enroll\\" + user_name + "\\wav\\"

    gmm_dir = "..\\Enroll\\" + user_name + "\\"

    prefix_train = user_name + "\\wav\\"

    f = open("..\\Enroll\\" + user_name + "\\enroll.txt", 'w')

    enroll_file = "..\\Enroll\\" + user_name + "\\enroll.txt"

    print("Welcome"+user_name)

    for i in range(5):
        trial = "trial" + str(i + 1)
        print(trial)
        key_phrase = rand_phrase_train()
        print("Please say '" + key_phrase + "' once the system starts listening")
        time.sleep(2)
        f_name = user_name + str(i + 1)
        record_audio(f_name, train_dir)
        edit_txt(f_name, enroll_file, prefix_train)

    file_paths = open(enroll_file, 'r')

    count = 1

    features = np.asarray(())
    for path in file_paths:
        path = path.strip()
        print(path)

        # read the audio
        sr, audio = read(source_enroll + path)

        # extract 40 dimensional MFCC & delta MFCC features
        vector = extract_features(audio, sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
        # when features of 5 files of speaker are concatenated, then do model training
        if count == 5:
            gmm = GMM(n_components=8, n_iter=200, covariance_type='diag', n_init=3)
            gmm.fit(features)

            # dumping the trained gaussian model
            picklefile = user_name + ".gmm"
            cpk.dump(gmm, open(gmm_dir + picklefile, 'wb'))
            print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
            features = np.asarray(())
            count = 0
        count = count + 1


def validate(user_name):

    global log_likelihood

    log_likelihood = np.zeros(1)

    source_enroll = "..\\Enroll\\"

    source_test = "..\\Test\\"

    os.makedirs("..\\Test\\" + user_name + "\\wav\\")

    f = open("..\\Test\\" + user_name + "\\test.txt", 'w')

    test_file = "..\\Test\\" + user_name + "\\test.txt"

    dir_test = "..\\Test\\" + user_name + "\\wav\\"

    gmm_dir = "..\\Enroll\\" + user_name + "\\"

    enroll_file = "..\\Enroll\\" + user_name + "\\enroll.txt"

    prefix_test = user_name + "\\wav\\"
    # ead = input("Enter email address so that an otp can be sent:")
    # pwd = input("enter your mails password")
    messg = rand_phrase_test()
    # sendotph(ead, pwd, messg)
    rt = input("Are you ready to validate? hit 'y' if you have the key-phrase sent via email")
    if rt == 'y':
        print("say your key-phrase '"+messg+"'")
        f_name1 = user_name + "test"

        record_audio(f_name1, dir_test)


        edit_txt(f_name1, test_file, prefix_test)

    gmm_files = gmm_dir + user_name + ".gmm"
    models = cpk.load(open(gmm_files, 'rb'))

    file_paths_orig = open(enroll_file, 'r')

    logsum = 0
    log_likelihood_orig = np.zeros(1)

    for path_orig in file_paths_orig:
        path_orig = path_orig.strip()
        print(path_orig)
        (sro, audioo) = read(source_enroll + path_orig)
        vector_o = extract_features(audioo, sro)
        gmm = models  # checking with each model one by one
        scores = np.array(gmm.score(vector_o))
        log_likelihood_orig[0] = scores.sum()
        print(log_likelihood_orig[0])
        logsum = logsum + log_likelihood_orig[0]
    logavg = logsum / 5
    print(logavg)  # uncomment later

    file_paths1 = open(test_file, 'r')

    # Read the test directory and get the list of test audio files
    for path1 in file_paths1:
        print(path1[:-1])
        path1 = path1[:-1]
        (sr, audio) = read(source_test + path1)
        vector = extract_features(audio, sr)
        gmm = models  # checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[0] = scores.sum()
        print(log_likelihood[0]) #uncomment for reference

    if ((logavg/log_likelihood[0])*100) > 85:
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
