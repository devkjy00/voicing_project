# TDD로 다시 짜기


class ChromaticScale:
    def __init__(self) -> None:
        '''음역대 정보'''
        self._chromatic_scale = ('C', 'Db', 'D', 'Eb',
                         'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
        self._octave = ('1', '2', '3', '4')
        self._long_chromatic = self.get_long_chromatic()
        
    def get_long_chromatic(self):  
        ''' C1~B4 생성  '''
        return tuple(i + j for j in self._octaves
                        for i in self._chromatic_scale)
    
    def sort_chromatic_by(self, key):
        prev_scale = self._chromatic_scale
        idx = prev_scale.index(key)
        self._chromatic_scale = prev_scale[idx:]+prev_scale[:idx]
    

class SongKey:
    
    def __get__(self, instance, owner):
        try:
            print(f'{instance}의 키는 {instance.__dict__[self.key]}입니다')
        except AttributeError:
            print( '키가 생성되지 않았습니다')

    def __set__(self, instance, value):
        pass

class Voicer:

    def __init__(self) -> None:
        pass

    
a = ChromaticScale()

