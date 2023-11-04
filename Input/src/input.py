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


    def test_getNotes(self):

        n = Input.getNotes('TestDat/test.mid')

        r = lambda n : round(n)
        
        self.assertEqual(
            [262, 247, 233, 220, 208, 196, 185, 175, 165, 156, 147, 139, 139, 131],
           list(map(r, n[0]))
        )
        
    
    

if __name__ == '__main__':

    n = Input.getNotes('TestDat/test.mid')
    print(n)
    unittest.main()
    
    
