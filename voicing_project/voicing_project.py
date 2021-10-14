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

    def progression():
        pass

    def four_part(self, topnote, chord):
        # 탑 노트 아래로 메커니컬 보이싱을 생성
        # 모든 음역대를 선택하고 위에서 4개의 음만 반환하는 방식으로 시작하자
        voicing_tone = []
        # 입력받은 코드의 기능 분리
        chord_func = self.decollate_chord_func(chord)
        # 탑 노트 기능 분리
        topnote_func = self.decollate_topnote_func(topnote)
        # 탑 노트 아래의 음역대를 선택(슬라이싱)
        sliced_chro_fromTop = self.get_scale_range(topnote)
        # 텐션 찾기
        tensions = self.get_tension(chord_func)
        # 찾은 텐션으로 보이싱 경우의 수 만들기(코드폼 반환)
        tension_tone = self.tension_voicing(tensions, chord_func)
        # 코드의 근음 위치 선택/ 탑노트와 같은 옥타브 또는 아래쪽에 코드근음이 있는지 확인
        if chord_func[0]+topnote_func[1] in sliced_chro_fromTop:    # 같은 옥타브에 근음이있는 경우
            # 근음 위치 인덱스구하기
            Root_idx = sliced_chro_fromTop.index(chord_func[0]+topnote_func[1])
            # 코드폼 인덱스 가져와서 한개씩 값 대입
            for idx in musico._chord_tone[chord_func[1]]:
                # 근음부터 위로 올라가면서 코드톤 쌓고 탑노트 위에 음은 옥타브 내리기
                try:
                    voicing_tone.append(sliced_chro_fromTop[Root_idx+idx])
                except:
                    voicing_tone.append(sliced_chro_fromTop[Root_idx-12+idx])
        else:                                                       # 같은 옥타브에 근음이 없는 경우
            # 근음 위치 인덱스구하기(한옥타브 낮춰서)
            Root_idx = sliced_chro_fromTop.index(
                chord_func[0]+str(int(topnote_func[1])-1))
            # 코드폼 인덱스 가져와서 한개씩 값 대입
            for idx in musico._chord_tone[chord_func[1]]:
                try:
                    voicing_tone.append(sliced_chro_fromTop[Root_idx+idx])
                except:
                    voicing_tone.append(sliced_chro_fromTop[Root_idx-12+idx])

        # 드랍 하기

        # 마지막으로 탑노트와 베이스근음 넣기
        voicing_tone.append(topnote)
        voicing_tone.append(chord_func[0]+'1')
        # 사운드 플레이
        self.play_notes(voicing_tone)

    def play_notes(self, notes):
        for note in notes:
            pygame.mixer.Sound(
                date_path+'/'+note+'.wav').play()
            # time.sleep(0.1)
        time.sleep(1)

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
        tensions = [resorted_notes[1], resorted_notes[3], resorted_notes[5]]
        return tensions

    def tension_voicing(self, tensions, cho_func):
        # 근음 카테고리
        pass
# def play_diatonic7th_chord_progression(chromatic_scales, dia_note_idx,  dia_chord_form):
    #     # 완성된 다이아토닉 코드변수 [0]계이름,[1]코드폼
    #     diatonic = []
    #     # 코드생성 근음의 옥타브 변수
    #     Root_octave = '3'
    #     # 슬라이싱에 쓸 루트위치 인덱스
    #     Root_idx = 0
    #     # 다이아토닉에 대입해서 코드진행 생성
    #     chord_progression = [1, 5, 6, 4, 3, 6, 2, 5]
    #     # 코드진행에 따른 코드순서리스트 완성값
    #     diatonic_progression = []

    #     # 다이아토닉 완성 시키기 :[0]정렬된 크로매틱[음 위치] [1]정렬된 코드폼  순서대로 대입
    #     for idx, note in enumerate(dia_note_idx):
    #         diatonic.append([chromatic_scales[note], dia_chord_form[idx][1]])
    #     # 코드진행따라서 다이아토닉 코드 순서대로 리스트에 넣기
    #     for i in chord_progression:
    #         diatonic_progression.append(diatonic[i-1])

    #     for chord in diatonic_progression:
    #         # 코드근음 위치: 코드근음+옥타브
    #         Root = chord[0] + Root_octave
    #         # 4옥타브 크로매틱에서 근음의 인덱스 반환
    #         Root_idx = sorted_chromatic_scale.index(Root)
    #         # 근음 인덱스을 기준으로 슬라이싱하기
    #         sliced_cro_scale = sorted_chromatic_scale[Root_idx:]
    #         # 진행중인 코드근음으로 시작하는 스케일, 코드 톤 음 간격 을 인자로 코드를 연주하는 함수
    #         print(sliced_cro_scale)
    #         play_chord(sliced_cro_scale, musico._dia_chord_tone[chord[1]],)
    #         time.sleep(1)


# def go():
#     print(entry)
#     key = entry.get()
#     sorted_scale, sorted_interval, diatonic_chords = sort_by_key(key)
#     play_diatonic7th_chord_progression(sorted_interval, sorted_scale, diatonic_chords)
# root = Tk()
pygame.mixer.init()


# frame = Frame(root).pack()
# entry = Entry(frame)
# entry.pack()
# btn = Button(frame, text="다이아토닉 재생", command=go).pack(side="left")

# 파일 위치
current_path = os.path.dirname(__file__)
date_path = os.path.join(current_path, "data")
scale_list = os.listdir(date_path)

C = musico("C")
C.four_part('E4', 'Am7')

# root.mainloop()
