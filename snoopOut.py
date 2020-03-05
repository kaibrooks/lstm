from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.optimizers import Adam
from keras.utils.data_utils import get_file
from keras.layers import Dropout # dropout crew 4 lyf
from IPython.display import clear_output # clear plot after each epoch
import tensorflow as tf
from tensorflow import keras as keras
import numpy as np
import random
import sys
import io
import os
import h5py
import matplotlib.pyplot as plt # fancy plots
from matplotlib import pyplot as plt
from datetime import datetime # so we know how much time we've wasted

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

## load a model for testing
model_path = os.path.join('MODELNAME.h5') # load external file
model = load_model(model_path)
print('Loaded', model_path)

## load the corpus
path = os.path.join('SNOOP.txt') # path to the corpus

with open(path, encoding='utf-8', errors='ignore') as f: # errors=ignore strips non utf-8 chars
    text = f.read().lower()

chars = sorted(list(set(text)))

char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

print('corpus length :', len(text))
print('unique chars  :', len(chars))
print('total patterns:', len(sentences))
print('') # empty line

## generate output
start_index = random.randint(0, len(text) - maxlen - 1)
sentence = text[start_index: start_index + maxlen]

temperature = 0.5 # 0.5-2ish, higher numbers give more unique output
maxChars = 400 # length of new output

seed = sentence.replace('\n','') # cut newlines
seed = seed.replace('\t','')

print('*** seed: <', seed ,'>') # print the seed (text input)
print('\n',seed, end = '')

# make some words
for i in range(maxChars):
    x_pred = np.zeros((1, maxlen, len(chars)))
    for t, char in enumerate(sentence):
        x_pred[0, t, char_indices[char]] = 1.

    preds = model.predict(x_pred, verbose=0)[0]
    next_index = sample(preds, temperature)
    next_char = indices_char[next_index]

    sentence = sentence[1:] + next_char

    sys.stdout.write(next_char)
    sys.stdout.flush()
print()
