from input import *

import glob

import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import utils
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

if __name__ == '__main__':



    paths = glob.glob('./Midi-Data/bach/*.mid')
    

    print("Loading Songs:")
    songs = [' '.join(Input.getJustNotes(p)[0]) for p in paths]
    print(f"Loaded {len(songs)} Songs")


    ## Tokenising and preprocessing
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(songs)
    total_notes = len(tokenizer.word_index) + 1
    print(f'Total Note: {total_notes}')
    
    input_sequences = []
    for song in songs:
        token_list = tokenizer.texts_to_sequences([song])[0]
        
        for i in range(1, len(token_list)):
            partial_sequence = token_list[:i+1]
            input_sequences.append(partial_sequence)
            
    
            
    max_sequence_len = max([len(x) for x in songs])

    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    # all except the last
    predictors = input_sequences[:, :-1]

    # labels are the last word
    labels = input_sequences[:,-1]
    print(labels[:5])

    labels = utils.to_categorical(labels, num_classes=total_notes)

    ## Model Creation!!
    input_len = max_sequence_len - 1

    model = Sequential()
    model.add(Embedding(total_notes, 10, input_length=input_len))

    model.add(LSTM(100)) # LSTM with 100 units

    model.add(Dropout(0.1))

    model.add(Dense(total_notes, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    history = model.fit(predictors, labels, epochs=30, verbose=1)

    model.save('MusicMaker.keras')
    
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig('performance.png')
    
    

    
    
    
