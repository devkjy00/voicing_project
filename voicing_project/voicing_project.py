# 피아노 12음 4옥타브를 녹음해서 저장, 리스트에 경로 저장
# 알고리즘에 따라서 파일 동시 재생
# pyaudio 는 3.6버젼 까지만 지원되니까 아웃
# 곡의 키를 입력해서 다이아토닉 코드의 리스트 생성, 모달은 빼고 일단, 서브도미넌트까지만 만들자
# 입력 받은 키를 사용해서 스케일을 1도부터 다시 정렬하기

# 코드가 바뀔 때마다 스케일을 재정렬 하는게 좀 헷갈린다
# 키 입력 -> 장,단조확인 -> 근음 기준 음 간격,코드폼,크로매틱 재정렬  -> 음 간격 더해서 음위치 생성
# -> 정렬된 4옥타브 크로매틱에서 슬라이싱[근음:]과 코드 폼에 따른 음 간격을 누적합해서 코드생성

# 현재 탑노트 아래로 closed voicing 만들었으니까 이제 카테고리 보이싱 추가해보자@@ 다이아토닉이랑 연계해서 텐션 고르는 알고리즘 ㄱㄱ
# 탑노트 위치를 잡고 서브도미넌트도 결국 텐션은 다이아토닉.... 다이아토닉 스케일에 인덱스 0,1,2,3 으로 대입해서 텐션을 고르고 어보이드 노트는 빼는 방법
# drop 하기/ 인풋[코드톤, 보이싱톤] - 연산[1,3 인덱스의 값을 -1한다] - 아웃풋[주어진 화음으로 2,2&4 만들기]
####################

import os
import pygame
import time
from tkinter import *



class musico():
    _chromatic_scales = ['C', 'Db', 'D', 'Eb',
                         'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    _octaves = ['1', '2', '3', '4']
    _sorted_chromatic_scale = []
    for octave in _octaves:
        for scale in _chromatic_scales:
            _sorted_chromatic_scale.append(scale+octave)
    _sorted_dia_chord_form = ['', 'M7'], ['m', 'm7'], [
        'm', 'm7'], ['', 'M7'], ['', '7'], ['m', 'm7'], ['mb5', 'm7b5']
    _major_dia_note_idx = [0, 2, 4, 5, 7, 9, 11]
    _minor_dia_note_idx = [0, 2, 3, 5, 7, 8, 10]
    _chord_tone = {'': [0, 4, 7], 'm': [0, 3, 7], 'M7': [0, 4, 7, 11], 'm7': [
        0, 3, 7, 10], '7': [0, 4, 7, 10], 'mb5': [0, 3, 6], 'm7b5': [0, 3, 6, 10]}

    def __init__(self, key):
        # 조성, 다이아토닉 코드 리스트 를 속성으로 갖는다
        self._key = key
        self._dia_chords = []

        # 메이져키인지 마이너키인지 확인
        if 'm' in key:  # 마이너 인 경우
            # 근음의 위치 인덱스 반환
            key_idx = musico._chromatic_scales.index(key[:-1])
            # 다이아토닉 코드폼을 마이너코드폼 순서로 재 정렬
            dia_chord_form = musico._sorted_dia_chord_form[5:] + \
                musico._sorted_dia_chord_form[:5]
            # 마이너 다이아토닉음 인덱스 대입
            diatonic_note_idx = musico._minor_dia_note_idx
        else:           # 메이져 인 경우
            # 근음의 위치 인덱스 반환
            key_idx = musico._chromatic_scales.index(key)
            # 메이져로 이미 정렬 되 있는 코드폼 순서 반환
            dia_chord_form = musico._sorted_dia_chord_form
            # 메이져 다이아토닉음 인덱스 대입
            diatonic_note_idx = musico._major_dia_note_idx
        # 근음의 위치인덱스 값을 기준으로 1옥타브 크로매틱 스케일 재 정렬
        resorted_cromatic = musico._chromatic_scales[key_idx:] + \
            musico._chromatic_scales[:key_idx]
        # 계이름 인덱스와 코드폼으로 다이아토닉 코드 생성
        for idx, note in enumerate(diatonic_note_idx):
            self._dia_chords.append(
                [resorted_cromatic[note], dia_chord_form[idx][1]])
        print(self._key, "key :", self._dia_chords)

    def four_part(self, topnote, chord, Tension, drop, time):
        # 탑 노트 아래로 메커니컬 보이싱을 생성
        # 모든 음역대를 선택하고 위에서 4개의 음만 반환하는 방식으로 시작하자
        voicing_tone = [[], []]
        # 입력받은 코드의 기능 분리
        chord_func = self.decollate_chord_func(chord)
        # 탑 노트 기능 분리
        topnote_func = self.decollate_topnote_func(topnote)
        # 탑 노트 아래의 음역대를 선택(슬라이싱)
        sliced_chro_fromTop = self.get_scale_range(topnote)
        # 텐션 찾기
        tensions, chord_compare = self.get_tension(chord_func)
        # 찾은 텐션으로 보이싱 경우의 수 만들기(코드폼 반환)
        tension_tone = self.tension_voicing(
            tensions, chord_func, chord_compare, Tension)
        if Tension[0] == True:
            the_chord = tension_tone
        else:
            the_chord = musico._chord_tone[chord_func[1]]

        # 코드의 근음 위치 선택/ 탑노트와 같은 옥타브 또는 아래쪽에 코드근음이 있는지 확인
        if chord_func[0]+topnote_func[1] in sliced_chro_fromTop:    # 같은 옥타브에 근음이있는 경우
            # 근음 위치 인덱스구하기
            Root_idx = sliced_chro_fromTop.index(chord_func[0]+topnote_func[1])
            # 코드폼 인덱스 가져와서 한개씩 값 대입
            for idx in the_chord:
                # 근음부터 위로 올라가면서 코드톤 쌓고 탑노트 위에 음은 옥타브 내리기
                try:
                    voicing_tone[0].append(sliced_chro_fromTop[Root_idx+idx])
                except:
                    voicing_tone[1].append(
                        sliced_chro_fromTop[Root_idx-12+idx])
        else:                                                       # 같은 옥타브에 근음이 없는 경우
            # 근음 위치 인덱스구하기(한옥타브 낮춰서)
            Root_idx = sliced_chro_fromTop.index(
                chord_func[0]+str(int(topnote_func[1])-1))
            # 코드폼 인덱스 가져와서 한개씩 값 대입
            for idx in the_chord:
                try:
                    voicing_tone[0].append(sliced_chro_fromTop[Root_idx+idx])
                except:
                    voicing_tone[1].append(
                        sliced_chro_fromTop[Root_idx-12+idx])
        # 옥타브 변경된 노트들 음높이 순서대로 다시 정렬
        voicing_tone = voicing_tone[1]+voicing_tone[0]
        # 드랍 하기
        if drop[0] == True:
            self.drop_24(voicing_tone, drop)
        # 마지막으로 탑노트와 베이스근음 넣기
        voicing_tone.append(topnote)
        voicing_tone.insert(0, chord_func[0]+'1')
        # 사운드 플레이
        self.play_notes(voicing_tone, time)

    def play_notes(self, notes, t):
        for note in notes:
            pygame.mixer.Sound(
                date_path+'/'+note+'.wav').play()
            print(note)
            # time.sleep(0.1)
        time.sleep(t)

    def decollate_chord_func(self, chord):
        # 먼저 앞2글자 슬라이싱
        front_2str = chord[1:2]
        if 'b' in front_2str:   # b인 경우
            note = chord[:2]
            chord_form = chord[2:]
        else:                    # b이 아닌경우
            note = chord[:1]
            chord_form = chord[1:]
        return [note, chord_form]

    def decollate_topnote_func(self, topnote):
        # 탑 노트 기능 분리
        topnote_func = ['', '']
        if len(topnote) == 3:
            topnote_func[0], topnote_func[1] = topnote[:2], topnote[2:]
        else:
            topnote_func[0], topnote_func[1] = topnote[:1], topnote[1:]
        return topnote_func

    def get_scale_range(self, topnote):
        topnote_idx = musico._sorted_chromatic_scale.index(topnote)
        sliced_chro_fromTop = musico._sorted_chromatic_scale[:topnote_idx]
        return sliced_chro_fromTop

    def get_tension(self, cho_func):
        # 다이아토닉노트
        notes = []
        # {다른노트의 카테고리 인덱스:다른노트의 값 차이}
        chord_compare = {}
        for dia in self._dia_chords:
            notes.append(dia[0])
        print(notes)
        # 코드를 다이아토닉스케일과 비교 다이아토닉코드인지, 서브도미넌트 코드인지, 그것도 아니면 아웃

        # 코드가 몇번째 다이아토닉음인지 확인
        try:
            dia_chord_idx = notes.index(cho_func[0])
        except:         # 아니면 종료
            print('다이아토닉도, 서브도미넌트도 아닙니다')
            return
        # 입력받은 코드값과 다이아토닉 코드 비교
        # 다이아토닉 코드톤 =  코드폼간격[다이아토닉 코드들[입력된 노트의 다이아토닉 순서]]
        dia_chord_notes = musico._chord_tone[musico._sorted_dia_chord_form[dia_chord_idx][1]]
        # 입력받은 코드톤 = 코드폼간격[입력받은 코드폼]
        input_chord_notes = musico._chord_tone[cho_func[1]]
        # 인덱스=같은카테고리, 끼리 비교해서 같은 코드톤인지 다르면 어디가 다른지 확인
        for i in range(0, len(input_chord_notes)):  # 3화음이면 3번비교 4화음이면 4번 비교
            if input_chord_notes[i] == dia_chord_notes[i]:
                pass
            else:   # 다이아토닉이 아니면 비교값을 저장
                chord_compare[i] = input_chord_notes[i] - dia_chord_notes[i]
        # 다이아토닉 스케일을 코드를 근음으로 재정열 하고 인덱스를 이용해서 카테고리화, 텐션음들을 저장
        resorted_notes = notes[dia_chord_idx:]+notes[:dia_chord_idx]
        print(resorted_notes)
        tension_tone = []
        tensions = [resorted_notes[1], resorted_notes[3], resorted_notes[5]]
        Root_idx = musico._sorted_chromatic_scale.index(cho_func[0]+'2')
        resorted_cromatic = musico._sorted_chromatic_scale[Root_idx:]
        for tension in tensions:
            if tension+'2' in resorted_cromatic:
                tension_tone.append(resorted_cromatic.index(tension+'2'))
            elif tension+'3' in resorted_cromatic:
                tension_tone.append(resorted_cromatic.index(tension+'3'))
        return tension_tone, chord_compare

    def tension_voicing(self, tension_tone, cho_func, chord_compare, Tension):
        print(Tension[1], '음을 사용')
        if self._key[-1:] == 'm':
            paralal = 3
        else:
            paralal = 0
        voicing_tone = []
        # 인풋코드의 카테고리별 텐션 넣기
        # 근음 카테고리: 9
        if 9 in Tension[1] and cho_func[0]+cho_func[1] != self._dia_chords[paralal+2]:   # 프리지안이 아닌경우
            voicing_tone.append(tension_tone[0])    # 9,b9
        else:
            voicing_tone.append(0)
        # voicing_tone.append(tension_tone[0]+2)  # #9
        # 3음 카테고리 : 9,11
        # 아이오니안이 아닌 경우
        if 11 in Tension[1] and cho_func[0]+cho_func[1] != self._dia_chords[paralal]:
            voicing_tone.append(tension_tone[1])    # 11,#11
        else:
            voicing_tone.append(musico._chord_tone[cho_func[1]][1])
        # 5음 카테고리 : 11,13
        if 13 in Tension[1]:
            # voicing_tone.append(tension_tone[1])    # 11,#11
            voicing_tone.append(tension_tone[2])    # 13,b13
        else:
            voicing_tone.append(musico._chord_tone[cho_func[1]][2])
        # 7음 카테고리 :
        voicing_tone.append(musico._chord_tone[cho_func[1]][3])
        if cho_func[1] in musico. _sorted_dia_chord_form:
            pass
        return voicing_tone

    def drop_24(self, chord, num):
        # 코드의 1,3 인덱스의 마지막문자열(숫자)를 -1 하고 문자열로 다시 더하기
        # drop 2
        drop2 = str(int(chord[3][-1:]) - 1)
        chord.insert(0, chord[3][:-1]+drop2)
        del chord[4]
        if num[1] == 4:
            drop4 = str(int(chord[2][-1:]) - 1)
            chord.insert(0, chord[2][:-1]+drop4)
            del chord[3]
        return chord

def play_overtherainbow():
    C.four_part('G4', 'CM7', [True, [9, 13]], [True, 4], 3)
    C.four_part('C4', 'E7', [True, [9, 13]], [True, 4], 2)
    C.four_part('Ab3', 'E7', [True, [9, 13]], [True, 4], 1.5)
    C.four_part('B3', 'FM7', [True, [9, 13]], [True, 4], 2)
    C.four_part('A3', 'FM7', [True, [9, 13]], [True, 4], 1.5)
    C.four_part('A3', 'A7', [True, [9, 13]], [True, 4], 3)
    C.four_part('A3', 'Dm7', [True, [9, 13]], [True, 4], 3)
    C.four_part('F4', 'A7', [True, [9, 13]], [True, 4], 2)
    C.four_part('Db4', 'A7', [True, [9, 13]], [True, 4], 1.5)
    C.four_part('E4', 'D7', [True, [9, 13]], [True, 4], 2)
    C.four_part('D4', 'D7', [True, [9, 13]], [True, 4], 1.5)
    C.four_part('D4', 'G7', [True, [9, 13]], [True, 4], 1.5)
    C.four_part('E4', 'G7', [True, [9, 13]], [True, 4], 1.5)
    C.four_part('F4', 'G7', [True, [9, 13]], [True, 4], 1.5)


pygame.mixer.init()
# 파일 위치
current_path = os.path.dirname(__file__)
date_path = os.path.join(current_path, "data")
scale_list = os.listdir(date_path)




C = musico("C")
tension_list = [[9], [13], [11], [9, 11], [9, 13], [11, 13], [9, 11, 13]]

play_overtherainbow()



