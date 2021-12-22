# TDD로 다시 짜기


class ChromaticScale:
    def __init__(self) -> None:
        '''음역대 정보'''
        self._chromatic_scale = ('C', 'Db', 'D', 'Eb',
                         'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
        self._octave = ('1', '2', '3', '4')
        self._long_chromatic = self._get_long_chromatic()
        
    def _get_long_chromatic(self) -> None:  
        ''' C1~B4 생성  '''
        return tuple(i + j for j in self._octave
                        for i in self._chromatic_scale)
    
    def sort_chromatic_by(self, key: str) -> None: 
        prev_scale = self._chromatic_scale
        idx = prev_scale.index(key)
        self._chromatic_scale = prev_scale[idx:]+prev_scale[:idx]
    

class Chord:
    def __init__(self) -> None:
        _sorted_dia_chord_form = ['', 'M7'], ['m', 'm7'], [
        'm', 'm7'], ['', 'M7'], ['', '7'], ['m', 'm7'], ['mb5', 'm7b5']
        _chord_tone = {'': [0, 4, 7], 'm': [0, 3, 7], 'M7': [0, 4, 7, 11], 'm7': [
        0, 3, 7, 10], '7': [0, 4, 7, 10], 'mb5': [0, 3, 6], 'm7b5': [0, 3, 6, 10]}
        _major_dia_note_idx = [0, 2, 4, 5, 7, 9, 11]
        _minor_dia_note_idx = [0, 2, 3, 5, 7, 8, 10]


   
class Voicer:

    def __init__(self) -> None:
        pass

    


