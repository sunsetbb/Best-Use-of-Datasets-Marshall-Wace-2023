# Input.py
## This File will provide utilities to aquire and manipulate MIDI
## Datasets
## 4/11/2023 - Benjamin Swaby

import unittest

import pretty_midi


class Input(unittest.TestCase):

    # Returns a 2D list of frequencies in a MIDI file
    ## Each array is it's own instrument that can be treated seperately.
    ## Skips Drums!
    def getNotes(path :str) -> list[list]:

        midi_data = pretty_midi.PrettyMIDI(path)
        
        f = lambda n : 440 * 2**((n - 69)/12)
    
        return  [[f(n.pitch) for n in i.notes] for i in midi_data.instruments if not i.is_drum]


    ## Normalise the data between 0 and 1
    def noramaliseNotes(notes :list):

        m = max(notes)
        n = lambda x : x/m

        return list(map(n, notes))



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

        r = lambda n : round(n)
        
        self.assertEqual(
            [262, 247, 233, 220, 208, 196, 185, 175, 165, 156, 147, 139, 139, 131],
           list(map(r, n[0]))
        )
        
    
    

if __name__ == '__main__':
    
    unittest.main()
    
    
