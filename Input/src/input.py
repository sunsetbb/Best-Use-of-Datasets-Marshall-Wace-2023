# Input.py
## This File will provide utilities to aquire and manipulate MIDI
## Datasets
## 4/11/2023 - Benjamin Swaby

import unittest
import math

import pretty_midi


class Note:

        time_ :float
        freq_ :float
        amp_  :float
        note_ :str


        def generateNote(self):
              notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

              note_number = 12 * math.log2(self.freq_ / 440) + 49  
              note_number = round(note_number)
        
              note = (note_number - 1 ) % len(notes)
              note = notes[note]
    
              octave = (note_number + 8 ) // len(notes)

              self.note_ = note + str(octave)
    

            
        def __init__(self, time, freq, amp):
            self.time_ = time
            self.freq_ = freq
            self.amp_ = amp
            self.generateNote()

        def getFreq(self):
            return self.freq_

                
        def __str__(self):
            return f'(t:{self.time_}, f:{self.freq_}hz, a:{self.amp_} n:{self.note_})'

        def __repr__(self):
            return self.__str__()

class Input(unittest.TestCase):
    
    
    
    # Returns a 2D list of frequencies in a MIDI file
    ## Each array is it's own instrument that can be treated seperately.
    ## Skips Drums!
    def getNotes(path :str) -> list[list]:

        midi_data = pretty_midi.PrettyMIDI(path)
        
        f = lambda n : 440 * 2**((n - 69)/12)
    
        return [[Note(n.start, f(n.pitch), n.velocity) for n in i.notes] for i in midi_data.instruments if not i.is_drum]        



    def getFrequencies(path :str) -> list[list]:

        midi_data = pretty_midi.PrettyMIDI(path)
        
        f = lambda n : 440 * 2**((n - 69)/12)


        return [[f(n.pitch) for n in i.notes]for i in midi_data.instruments if not i.is_drum][0]

        

    def getJustNotes(path :str) -> list[list]:

        midi_data = pretty_midi.PrettyMIDI(path)
        
        f = lambda n : 440 * 2**((n - 69)/12)
    
        return [[Note(n.start, f(n.pitch), n.velocity).note_ for n in i.notes]
                for i in midi_data.instruments if not i.is_drum]
        
        
    ## Normalise the data between 0 and 1
    def noramaliseNotes(notes :list):

        m = max(notes)
        n = lambda x : x/m

        return list(map(n, notes))


    ## Test to check normalisation methods
    def test_normaliseNotes(self):

        td = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        rd = Input.noramaliseNotes(td)

        self.assertEqual(
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            rd
        )
        

    
    # Test getting notes 
    def test_getNotes(self):

        n = Input.getNotes('TestDat/test.mid')

        r = lambda n : round(n.getFreq())
        
        self.assertEqual(
            [262, 247, 233, 220, 208, 196, 185, 175, 165, 156, 147, 139, 139, 131],
           list(map(r, n[0]))
        )
        
    
    

if __name__ == '__main__':

    n = Input.getNotes('TestDat/test.mid')

    print(n)
    
    unittest.main()
    
    
