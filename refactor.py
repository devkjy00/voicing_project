from tkinter.constants import N
from pygame import mixer
import time, os

class ChromaticScale:
    def __init__(self):
        '''스케일 정보'''
        self._chromatic_scale = ['C', 'Db', 'D', 'Eb',
                         'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self._octave = ('1', '2', '3', '4')
        self._long_chromatic = self._get_long_chromatic()
        self._major_dia_scale_idx = [0, 2, 4, 5, 7, 9, 11]
        self._minor_dia_scale_idx = [0, 2, 3, 5, 7, 8, 10]
        
    def _get_long_chromatic(self):  
        ''' C1~B4 튜플 생성  '''
        return tuple(i + j for j in self._octave
                         for i in self._chromatic_scale)
    
    def _sort_chromatic_by(self, key: str): 
        '''
        속성 self._chromatic_scale을 입력된 key가 첫 인덱스가 되도록 정렬
        '''

        prev_scale = self._chromatic_scale
        idx = prev_scale.index(key[0])
        self._chromatic_scale = prev_scale[idx:]+prev_scale[:idx]

    
    def get_sliced_chromatic(self, topnote: str) -> list:
        '''
        topnote 아래로 슬라이싱된 크로매틱스케일 반환
        '''
        topnote_idx = self._long_chromatic.index(topnote)
        sliced_chro_fromTop = self._long_chromatic[:topnote_idx]
        return sliced_chro_fromTop



    
def assert_key(key: str):
    assert type(key) == str, f'{key}는 잘못된 key 입니다'
    assert len(key) < 3, f'{key}는 잘못된 key 입니다'

class Chord(ChromaticScale):
    def __init__(self, key: str = 'C'):
        ''' 코드 정보 '''
        super().__init__()
        assert_key(key)
        self._key = key
        self._sorted_dia_chord_form = ['', 'M7'], ['m', 'm7'], [
        'm', 'm7'], ['', 'M7'], ['', '7'], ['m', 'm7'], ['mb5', 'm7b5']
        self._chord_tone = {'': [0, 4, 7], 'm': [0, 3, 7], 'M7': [0, 4, 7, 11], 'm7': [
        0, 3, 7, 10], '7': [0, 4, 7, 10], 'mb5': [0, 3, 6], 'm7b5': [0, 3, 6, 10]}
        
        self._diatonic_note_idx = []
        self._set_minor_attr() if 'm' in self._key else self._set_major_attr()
        self.dictonic = self._get_diatonic()
    

    def _set_minor_attr(self):
        self._diatonic_note_idx = self._minor_dia_scale_idx
        self._resort_minor_dia_chord_form()

    def _set_major_attr(self):
        self._diatonic_note_idx = self._major_dia_scale_idx

    def _get_diatonic(self) -> list:
        ''' 
        키 속성에 적합한 다이아 토닉코드 생성
        self._key = 'C' 이면
        ['C','M7],['D','m7'].... 으로 리스트 반환
        '''
        diatonic_chords = []
            
        self._sort_chromatic_by(self._key) # self._chromatic_scale 정렬
 
        for idx, note in enumerate(self._diatonic_note_idx):
            diatonic_chords.append(
                [self._chromatic_scale[note], 
                self._sorted_dia_chord_form[idx][1]])

        return diatonic_chords

    def _resort_minor_dia_chord_form(self):
        '''
        self._sorted_dia_chord_form 리스트를 메이져에서 마이너로 다시 정렬
        '''
        self._resort_dia_chord_form = self._sorted_dia_chord_form[5:] + \
                self._sorted_dia_chord_form[:5]
        


   
class Voicer(Chord):
    '''
        코드정보를 연주할수 있는 노트로 변환
    '''
    def __init__(self, key: str, topnote: str = 'B4'):
        super().__init__(key)
        self.topnote = topnote

    def _get_diatonic_notes(self, chord_num: int) -> list:
        chord_num -= 1
        self.dictonic[chord_num]
        # 슬라이스된 스케일에서 탑노트와 같은 옥타브에 근음이 있는지 확인
            # 없으면 한옥타브 낮춰서 노트찾기
        # 근음인덱스 찾고 코드폼대입해서 리스트반환
        
    


class Play:
    # 파일 위치
    current_path = os.path.dirname(__file__)
    date_path = os.path.join(current_path, "data")
    
    def __init__(self, key: str = 'C') -> None:
        '''
        Voicer객체를 포함해서 원하는 코드를 플레이한다
        '''
        mixer.init()
        self.voicer = Voicer(key)

    def play(notes):
        
        data_path = ''
        for note in notes:
            mixer.Sound(
                data_path+'/'+note+'.wav').play()
            print(note) 
        time.sleep(1)



C = Play()



