from pygame import mixer
import time
import os


class ChromaticScale:
    def __init__(self, key: str) -> None:
        self._chromatic_scale = ['C', 'Db', 'D', 'Eb',
                                 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self._octave = ('1', '2', '3', '4')
        self._long_chromatic = self._get_long_chromatic()
        self._major_dia_scale_idx = [0, 2, 4, 5, 7, 9, 11]
        self._minor_dia_scale_idx = [0, 2, 3, 5, 7, 8, 10]
        self._sort_chromatic_by(key)

    def _get_long_chromatic(self) -> tuple:
        """
        Set scale of 4 octaves
        :return:  Chromatic scale of 4 octaves
        """
        return tuple(i + j for j in self._octave
                     for i in self._chromatic_scale)

    def _sort_chromatic_by(self, key: str) -> None:
        """
        Using key string, sort _chromatic_scale attribute
        and set self._chromatic_scale
        :param key: 'C'
        :return: None
        """
        prev_scale = self._chromatic_scale
        idx = prev_scale.index(key[0])
        self._chromatic_scale = prev_scale[idx:] + prev_scale[:idx]

    def sort_chromatic_by(self, key: str) -> list:
        """
        Using key string, sort _chromatic_scale attribute
        :param key: 'C'
        :return: ['C', 'Db', 'D', ... 'B']
        """
        prev_scale = self._chromatic_scale
        idx = prev_scale.index(key)
        return prev_scale[idx:] + prev_scale[:idx]
    
    def get_sliced_chromatic(self, top_note: str) -> list:
        """
        Slice self._long_chromatic attr from the top note
        :param top_note: B4
        :return:  [C1, Db1, D1, ~ ~ , Bb4]
        """
        top_note_idx = self._long_chromatic.index(top_note)
        sliced_chromatic_from_top = self._long_chromatic[:top_note_idx]
        return sliced_chromatic_from_top


def assert_key(key: str):
    assert type(key) == str, f'{key}는 잘못된 key 입니다'
    assert len(key) < 3, f'{key}는 잘못된 key 입니다'


class Chord(ChromaticScale):
    def __init__(self, key: str):
        assert_key(key)
        super().__init__(key)
        self._key = key
        self._sorted_dia_chord_form = ['', 'M7'], ['m', 'm7'], [
            'm', 'm7'], ['', 'M7'], ['', '7'], ['m', 'm7'], ['mb5', 'm7b5']
        self._chord_tone = {'': [0, 4, 7], 'm': [0, 3, 7], 'M7': [0, 4, 7, 11], 'm7': [
            0, 3, 7, 10], '7': [0, 4, 7, 10], 'mb5': [0, 3, 6], 'm7b5': [0, 3, 6, 10]}

        self._diatonic_note_idx = []
        # set _diatonic_note_idx
        self._set_minor_attr() if 'm' in self._key else self._set_major_attr()

        self.diatonic = self._get_diatonic()

    def _set_minor_attr(self):
        """
        set attribute as minor
        :return: None
        """
        self._diatonic_note_idx = self._minor_dia_scale_idx
        self._resort_dia_chord_form = self._sorted_dia_chord_form[5:] + self._sorted_dia_chord_form[:5]

    def _set_major_attr(self):
        """
        set attribute as major
        :return: None
        """
        self._diatonic_note_idx = self._major_dia_scale_idx

    def _get_diatonic(self) -> list:
        """
        get diatonic chords
        if self._key is 'C'
        :return: ['C','M7],['D','m7']....
        """
        diatonic_chords = []

        for idx, note in enumerate(self._diatonic_note_idx):
            diatonic_chords.append(
                [self._chromatic_scale[note],
                 self._sorted_dia_chord_form[idx][1]])

        return diatonic_chords


class Voicer(Chord):
    def __init__(self, key: str = 'C'):
        super().__init__(key)

    def four_part_voicing(self, chord_num: str):
        """
        set notes of chord to play
        choose the octave of notes below top_note
        if self._key = 'C', top_note = 'B4'
        :param chord_num: '1' / '2b7'
        :return: ['C4', 'E4', 'G4', 'B3'] / ['Db', 'F', 'Ab', 'B']
        """
        voicing_notes = []
        root, chord_form = self.parse_chord_num(chord_num)
        all_scale = self.get_sliced_chromatic('B4')

        # root_oct = root + '4' if root + '4' in all_scale else root + '3'

        chord_scale = self.sort_chromatic_by(root)
        for i in self._chord_tone[chord_form]:
            note = chord_scale[i]
            voicing_notes.append(note)
        
        return voicing_notes
        # try:
        #     voicing_notes[0].append(root_idx)
        # except:
        #     voicing_tone[1].append(
        #         sliced_chro_fromTop[Root_idx - 12 + idx])

        # chord_num = 1
        # self.dictonic[chord_num]
        # 슬라이스된 스케일에서 탑노트와 같은 옥타브에 근음이 있는지 확인
        # 없으면 한옥타브 낮춰서 노트찾기
        # 근음인덱스 찾고 코드폼대입해서 리스트반환

    def parse_chord_num(self, chord_num: str) -> tuple:
        """
        Analyze chord_num
        if self._key is 'C'
        :param chord_num: '2b7'
        :return: 'Db', '7'
        """
        chord_root, *chord_form = chord_num

        assert '0' < chord_root < '8', f"{chord_root} is wrong chord_root"

        if chord_form:
            root_idx = self._diatonic_note_idx[int(chord_root) - 1]

            if 'b' in chord_form:
                root_idx -= 1
            if '#' in chord_form:
                root_idx += 1

            root = self._chromatic_scale[root_idx]
            chord_form = '7'

        else:
            root, chord_form = self.diatonic[int(chord_root) - 1]

        return root, chord_form


class Play:
    # 파일 위치
    current_path = os.path.dirname(__file__)
    data_path = os.path.join(current_path, "data")
    mixer.init()

    def __init__(self, key: str = 'C') -> None:
        self.voicer = Voicer(key)
        self.chord = []

    def add_chord(self, chord_num: str) -> None:
        """
        add chord_notes to self.chord 
        :param chord_num: "2b7",,,
        :return: None
        """
        self.chord.append(self.voicer.four_part_voicing(chord_num))
        print(self.voicer.four_part_voicing(chord_num)) 
        

    def play(self):
        for notes in self.chord:
            for note in notes:
                mixer.Sound(
                    self.data_path + '/' + note + '3.wav').play()
            time.sleep(1)

C = Play('C')
C.add_chord('3b7')
C.add_chord('2')
C.add_chord('5')
C.add_chord('1')
C.play()

