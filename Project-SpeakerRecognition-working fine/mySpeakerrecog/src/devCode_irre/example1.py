from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

(rate,sig) = wav.read("Rak_train.wav")
mfcc_feat = mfcc(sig,rate)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat1 = logfbank(sig,rate)
fbank_feat1 = fbank_feat1.sum()
print(fbank_feat1)

(rate,sig) = wav.read("Qwer2.wav")
mfcc_feat = mfcc(sig,rate)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat2 = logfbank(sig,rate)
fbank_feat2 = fbank_feat2.sum()
print(fbank_feat2)

if fbank_feat2>fbank_feat1:
    likely = (fbank_feat1/fbank_feat2)*100
    print(likely)
else:
    likely = (fbank_feat2 / fbank_feat1) * 100
    print(likely)