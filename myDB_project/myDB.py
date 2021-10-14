# 편곡 아이디어 라이브러리
# + 카테고리 설정해서 검색 후에 해당 값을 가지고있는 리스트 다 불러오기
# + 클래스를 이용해서 함수구조 단순하게 바꾸고 글로벌변수 없앰
# + 불러온 검색결과 리스트 텍스트위젯으로 출력/
# + 섹션을 나눠서 편곡정보를 작성할 수 있도록 하자 intro..verse....
# + 섹션정보명과 추가정보명을 리스트로 값에 추가해서 값의 길이가 달라져도 접근할수 있게함
# + 저장된값을 수정,삭제 할 수 있도록 변경
# - 삭제시 파일을 쓰는 과정에서 모든정보를 한번에 써서 읽어올때 한번에 다 읽어와져서
#   생기는 for문 오류 -> for문으로 각각 파일에 저장
# - 카테고리로 분류된 정보가 삭제후에도 똑같은 오류 -> 삭제를 누를 경우 카테고리 분류정보 초기화
# + 정보 수정시에 입력란에 남아있는 문자열 다 지우기
# song_info 리스트 [0]에 기본정보 스트링 넣고 [1]에 기본정보 클래스로 저장하기
# 완성된 클래스를 쓰는 느낌으로 수정하자


#############
# 음원 재생할 수 있도록 만들기 -> 저장시에 곡 제목의 폴더 생성

import pickle
import os
from posix import F_OK
from tkinter import *
import tkinter.ttk as ttk
import re
import tkinter.messagebox as msgbox
import time
from playsound import playsound
from pydub import AudioSegment
import subprocess
import sys


class jy:
    def __init__(self):
        self.root = Tk()
        self.category_info = ["artist", "song name",
                              "key", "meter", "tempo", "genre", "chord"]
        # 기본 정보 (입력된 전체 정보를 받을 값)
        # [0] = 기본정보 카테고리[사전키값],   [1] = 기본정보사전
        # [2] = 섹션정보 카테고리[사전키값],   [3] = 섹션정보사전
        # [4] = 추가정보 카테고리[사전키값],   [5] = 추가정보사전
        # [6] = 오디오 파일명[사전키값],     [7] = 오디오경로사전
        self.song_info = []

        # 추가 정보이름 배열
        self.added_info_name = []
        # 섹션 정보이름 배열
        self.section_info = []

        # 추가정보 개수
        self.added_song_info = 0
        self.added_section_info = 0
        # 각 카테고리별로 분류된 정보
        self.category_seperate_info = {}
        # 저장된 자료 개수
        self.program_info = 0
        # 정보갱신여부
        self.renew_info = False

        self.searched_list = []
        current_past = os.path.dirname(__file__)
        self.date_path = os.path.join(current_past, "data")
        self.audio_path = os.path.join(self.date_path, "audio")

        if os.access(self.date_path+"/program_date.pickle", F_OK) == True:
            # 프로그램 파일이 있는지 확인
            print("프로그램 파일 확인")
            with open(self.date_path+"/program_date.pickle", "rb") as file:
                self.program_info = pickle.load(file)
                print(self.program_info, " 개의 저장된 자료")
                # 저장된 정보갯수 가져오기
        else:
            print("프로그램 파일 없음")

    def create_fra_ent_dic(self):
        for idx, name in enumerate(self.category_info):
            # 카테고리사이즈 만큼 프레임과 엔트리 생성
            frame_for = LabelFrame(frame_basic_info, text=name)
            frame_for.pack(fill="both")
            globals()[f"frame_{name}"] = frame_for
            entry_for = Entry(frame_for)
            entry_for.pack(fill="both")
            globals()[f"entry_{name}"] = entry_for

            self.category_seperate_info[name] = []

        print("분류된 클래스정보 생성")
        print(self.category_seperate_info)

    def plus_info(self):
        # 추가정보콤보박스 추가하기
        self.frame_info = Frame(frame_secondary_info, relief="solid", bd=1)
        self.frame_info.pack(fill="both")
        globals()[f"frame_list_{self.added_song_info}"] = self.frame_info

        cbx_info = ttk.Combobox(self.frame_info, height="6", values=arr_info)
        cbx_info.pack(side="left")
        globals()[f"cbx_list_{self.added_song_info}"] = cbx_info

        text_info = Text(self.frame_info, width="30", height="3")
        text_info.pack(fill="both")
        globals()[f"text_list_{self.added_song_info}"] = text_info

        self.added_song_info += 1

    def section_info_plus(self):
        # 섹션정보위젯 추가
        self.frame_sec_info = Frame(frame_section_info, relief="solid", bd=1)
        self.frame_sec_info.pack(fill="both")
        globals()[
            f"frame_sect_{self.added_section_info}"] = self.frame_sec_info

        cbx_sec_info = ttk.Combobox(
            self.frame_sec_info, height="6", values=section_name)
        cbx_sec_info.pack(side="left")
        globals()[f"cbx_sect_{self.added_section_info}"] = cbx_sec_info

        text_sec_info = Text(self.frame_sec_info, width="30", height="3")
        text_sec_info.pack(fill="both")
        globals()[f"text_sect_{self.added_section_info}"] = text_sec_info

        self.added_section_info += 1

    def renew_file(self):
        if self.renew_info == True:
            # 정보갱신일 경우 기존 정보 지우기
            with open(self.date_path+"/songinfo.pickle", "rb") as file:
                for i in range(0, self.program_info):
                    self.song_info.append(pickle.load(file))
                    # 파일에서 정보 불러오기
            del self.song_info[self.renew_idx]
            # 기존 정보 지우기
            with open(self.date_path + "/songinfo.pickle", "wb") as file:
                pickle.dump(list(self.song_info), file)
                # 바뀐정보 다시 쓰기
            self.renew_info = False
            self.program_info -= 1

    def get_info(self):

        # self.renew_file()

        # 라이브러리 저장 버튼
        del self.song_info
        self.song_info = []

        # 현재 선언된 카테고리 인포를 곡정보에 첫 정보로 선언
        # 나중에 카테고리가 추가되서 달라질수 있기 때문에 각각의 곡에 카테고리 정보를 저장하자
        self.song_info.append(self.category_info)

        # 배열에 묶음으로 넣기위해서 이전배열의 값을 첨자로 쓰는 사전선언
        basic_dic = {}
        for idx, name in enumerate(self.category_info):
            basic_dic[name] = globals()[f"entry_{name}"].get()
            if name == "song name":
                basic_dic[name] = basic_dic[name].replace(" ", "_")
        self.song_info.append(basic_dic)

        # 섹션정보 값을 저장
        self.section_info.clear()
        for i in range(0, self.added_section_info):
            self.section_info.append(globals()[f"cbx_sect_{i}"].get())
            # 저장된 섹션의 정보의 이름을 배열로 저장
        self.song_info.append(self.section_info)

        # 배열에 묶음으로 넣기위해서 이전배열의 값을 첨자로 쓰는 사전선언
        sect_dic = {}
        for i in range(0, self.added_section_info):
            sect_dic[globals()[f"cbx_sect_{i}"].get()] = globals()[
                f"text_sect_{i}"].get(1.0, END)
        # print(sect_dic)
        self.song_info.append(sect_dic)

        self.added_info_name.clear()
        # 추가 정보
        for i in range(0, self.added_song_info):
            self.added_info_name.append(globals()[f"cbx_list_{i}"].get())
        self.song_info.append(list(self.added_info_name))

        # 배열에 묶음으로 넣기위해서 사전선언
        added_dic = {}
        for i in range(0, self.added_song_info):
            added_dic[globals()[f"cbx_list_{i}"].get()] = globals()[
                f"text_list_{i}"].get(1.0, END)
        # print(added_dic)
        self.song_info.append(added_dic)

        # 오디오 정보를 저장할 첨자 선언
        self.song_info.append([])
        self.song_info.append({})

        # 입력한 곡정보 파일에 쓰기
        with open(self.date_path + "/songinfo.pickle", "ab") as file:
            pickle.dump(list(self.song_info), file)

        # 라이브러리에 몇개의 정보가 있는지 업데이트
        self.program_info += 1
        with open(self.date_path + "/program_date.pickle", "wb") as file:
            pickle.dump(int(self.program_info), file)
            print(self.program_info)

        print(self.song_info)
        # 정보와 관련된 오디오를 저장할 폴더 생성
        new_folder_dir = self.audio_path+"/"+self.song_info[1]["song name"]
        self.create_folder(new_folder_dir)

    def search_info_screen(self):
        # 검색하기 버튼

        del self.song_info
        self.song_info = []

        with open(self.date_path+"/songinfo.pickle", "rb") as file:
            for i in range(0, self.program_info):
                self.song_info.append(pickle.load(file))
                # 한번에 쓴 자료는 한번에 읽어오고 여러번 쓴자료는 여러번에 걸쳐서읽어옴
        print(self.song_info)
        # self.출력()
        # 검색창 새로 생성
        self.search_root = Tk()
        self.search_root.geometry("600x400")
        self.frame_search = LabelFrame(self.search_root, text="검색 카테고리")
        self.frame_search.pack(fill="both")

        # 카테고리에 입력된 모든 정보가져와서 사용자입력(cbx)과 같은 모든 정보 출력
        self.init_catagory()

        self.cbx_category = ttk.Combobox(
            self.frame_search, height="5", values=self.category_info)
        self.cbx_category.pack(side="left")

        self.frame_search_but = Frame(self.search_root)
        self.frame_search_but.pack(fill="both")

        button_cate_confirm = Button(
            self.frame_search_but, text="카테고리 검색", command=self.search_confirmed)
        button_cate_confirm.pack(side="left")

        self.cbx_searched_result = ttk.Combobox(
            self.frame_search, height="5", values=self.searched_list)
        self.cbx_searched_result.pack(side="right")

        button_arti_info = Button(
            self.frame_search_but, text="검색하기", command=self.search_info)
        button_arti_info.pack(side="left")

        self.listbox_search_result = Listbox(
            self.search_root, fg="yellow", selectmode="single")
        self.listbox_search_result.pack(fill="both")
        self.listbox_search_result.configure(font=("Courier", 16, "italic"))

        # frame_search_root_edit = Frame(self.search_root)
        # frame_search_root_edit.pack(fill="both")

        self.btn_listbox_info = Button(self.search_root, text="전체보기")
        self.btn_listbox_info.pack(side="left")

        self.btn_search_audio = Button(
            self.search_root, text="오디오 검색", command=self.search_audio).pack(side="left")

        self.btn_folder_open = Button(self.search_root, text="오디오폴더")
        self.btn_folder_open.pack(side="left")

        self.btn_listbox_del = Button(self.search_root, text="삭제")
        self.btn_listbox_del.pack(side="right")

        self.btn_listbox_edit = Button(self.search_root, text="수정")
        self.btn_listbox_edit.pack(side="right")

        self.search_root.mainloop()

    def search_confirmed(self):
        # 카테고리검색버튼, 카테고리값 입력 -> 해당카테고리를 키값으로 가지는 사전정보를 콤보박스에 출력

        searched = self.cbx_category.get()
        self.listbox_search_result.delete(0, END)
        # 리스트 박스에 이전정보 지우기

        # 선택한 카테고리 값
        for idx, name in enumerate(self.category_info):
            if searched == name:
                seperate_info = self.category_seperate_info[name]
                searched_set = set(seperate_info)
                # 중복되는 정보는 무시
                # 교집합으로 같은이름의 정보가 몇개있는지도 할수있음
                self.searching_name = name
                # song_info 검색에서 쓸 카테고리 첨자
        self.searched_list = list(searched_set)
        # 각각의 값 접근을 위해 다시 리스트형으로 변환
        print(self.searched_list)
        self.cbx_searched_result.config(values=self.searched_list)
        # 위젯 내용을 업데이트 하거나 바꿀때 config(내용)

    def search_info(self):
        # 검색하기 버튼, 키워드 값 입력 -> 입력된값을 포함하는 정보 출력

        search_confirmed = self.cbx_searched_result.get()
        # 검색 키워드 값

        self.btn_listbox_info.config(command=self.load_all)
        self.btn_listbox_del.config(command=self.del_info)
        self.btn_listbox_edit.config(command=self.edit_info)
        self.btn_folder_open.config(command=self.open_folder)
        # 검색을 완료한 후에 버튼에 명령선언하기

        for i in range(0, self.program_info):
            # 모든 곡을 비교해서 같은 값 찾기
            if search_confirmed == self.song_info[i][1][self.searching_name]:
                # 검색값 == 곡정보[모든 곡][기본정보사전][카테고리첨자](검색한 값과 동일한 모든 경우)

                # 검색한 값과 동일한 곡 정보에 모두 실행

                # 기본정보 리스트박스에 입력
                for idx, name in enumerate(self.category_info):
                    if self.cbx_category.get() == name:
                        self.listbox_search_result.insert(
                            END, self.song_info[i][1][self.category_info[1]] + " / " + self.song_info[i][1][self.category_info[0]])

    def load_all(self):
        # 리스트박스에서 선택한 정보와오디오 전부 불러오기

        # 정보매칭
        song_num = self.find_choosed_info()

        # 폴더에 있는 파일 정보 저장
        self.find_audio(song_num)

        root_info = Tk()

        text_loaded_info = Text(root_info)
        text_loaded_info.pack(side="left")
        text_loaded_info.configure(font=("Courier", 16, "italic"))
        frame_audio = Frame(root_info)
        frame_audio.pack(side="right")

        # 오디오 리스트박스와 재생 버튼 생성
        self.song_num = song_num
        self.listbox_audio = Listbox(frame_audio, height="20")
        self.listbox_audio.pack(fill="both")
        for name in self.song_info[song_num][6]:
            self.listbox_audio.insert(END, name)

        btn_play_audio = Button(frame_audio, text="재생하기",
                                command=self.play_audio)
        btn_play_audio.pack()

        # 기본정보 텍스트에 입력
        for idx, name in enumerate(self.song_info[song_num][0]):
            text_loaded_info.insert(
                END, name + " : " + self.song_info[song_num][1][name]+"\n")

        text_loaded_info.insert(END, "\n")

        # 섹션 정보 텍스트에 입력
        for idx, name in enumerate(self.song_info[song_num][2]):
            if name == False:
                print("값 없음")
                break
            text_loaded_info.insert(
                END, name + " : " + self.song_info[song_num][3][name] + "\n")

        text_loaded_info.insert(END, "\n")

        # 추가 정보 텍스트에 입력
        for idx, name in enumerate(self.song_info[song_num][4]):
            if name == False:
                print("값 없음")
                break
            text_loaded_info.insert(
                END, name + " : " + self.song_info[song_num][5][name] + "\n")
        text_loaded_info.insert(END, "\n============================\n\n")
        print(f"{song_num}번곡 텍스트에 출력 완료")

        root_info.mainloop()

    def del_info(self):
        search_confirmed = self.cbx_searched_result.get()
        # 검색 키워드
        searched_listbox = list(self.listbox_search_result.curselection())[0]
        # 같은 키워드값중에서 몇번째 순서의 정보인지(예 :tom misch의 몇번째 곡인지) 한곡만 지목하기 위해서
        # 리스트 박스의 반환값은 튜플임 그래서 변환해서 첨자지정해서 쓰자
        choice = msgbox.askokcancel(title="경고", message="파일을 정말 삭제 하시겠습니까?")
        if choice == 1:
            pass
        else:
            return

        # 정보매칭
        song_num = self.find_choosed_info()
        # 해당 정보 삭제
        del self.song_info[song_num]

        self.program_info -= 1

        print(f"{song_num}번째 곡 정보 삭제됨\n")
        with open(self.date_path + "/songinfo.pickle", "wb") as file:
            for i in range(0, self.program_info):
                pickle.dump(self.song_info[i], file)

            # 삭제된 정보 빼고 파일 다시 쓰기

        with open(self.date_path + "/program_date.pickle", "wb") as file:
            pickle.dump(self.program_info, file)
            # print("num",self.program_info)
            # 프로그램정보도 1빼기

        # 삭제된 정보때문에 카테고리 정보갱신
        self.init_catagory()

        # 파일에서정보 받아오기위해 기존 정보 삭제
        del self.song_info
        self.song_info = []

        with open(self.date_path + "/songinfo.pickle", "rb") as file:
            for i in range(0, self.program_info):
                self.song_info.append(pickle.load(file))
            # print("지우고나서",self.song_info)

        return

    def edit_info(self):
        # 입력란 비우기
        self.init_input_string()
        # 정보매칭
        song_num = self.find_choosed_info()

        # 수정하고 저장하면 기존의 정보를 지우기위한 변수
        self.renew_info = True
        self.renew_idx = song_num

        # 기본정보 엔트리에 검색한키워드의 정보를 입력
        for idx, name in enumerate(self.song_info[song_num][0]):
            globals()[f"entry_{name}"].insert(
                END, self.song_info[song_num][1][name])
        # 섹션정보 입력
        for idx, name in enumerate(self.song_info[song_num][2]):

            self.frame_sec_info = Frame(
                frame_section_info, relief="solid", bd=1)
            self.frame_sec_info.pack(fill="both")
            globals()[
                f"frame_sect_{self.added_section_info}"] = self.frame_sec_info

            cbx_sec_info = ttk.Combobox(
                self.frame_sec_info, height="6", values=section_name)
            cbx_sec_info.pack(side="left")
            globals()[f"cbx_sect_{self.added_section_info}"] = cbx_sec_info
            globals()[f"cbx_sect_{self.added_section_info}"].set(name)

            text_sec_info = Text(self.frame_sec_info, width="30", height="3")
            text_sec_info.pack(fill="both")
            globals()[f"text_sect_{self.added_section_info}"] = text_sec_info
            globals()[f"text_sect_{self.added_section_info}"].insert(
                END, self.song_info[song_num][3][name])

            self.added_section_info += 1
        print(self.added_section_info, "개의 섹션정보 입력됨")
        # 섹션정보란에 정보 입력
        # 추가정보 입력
        for idx, name in enumerate(self.song_info[song_num][4]):

            self.frame_info = Frame(frame_secondary_info, relief="solid", bd=1)
            self.frame_info.pack(fill="both")
            globals()[f"frame_list_{self.added_song_info}"] = self.frame_info

            cbx_info = ttk.Combobox(
                self.frame_info, height="6", values=arr_info)
            cbx_info.pack(side="left")
            globals()[f"cbx_list_{self.added_song_info}"] = cbx_info
            globals()[f"cbx_list_{self.added_song_info}"].set(name)

            text_info = Text(self.frame_info, width="30", height="3")
            text_info.pack(fill="both")
            globals()[f"text_list_{self.added_song_info}"] = text_info
            globals()[f"text_list_{self.added_song_info}"].insert(
                END, self.song_info[song_num][5][name])
            self.added_song_info += 1
        print(self.added_song_info, "개의 추가정보 입력됨")
        # 추가정보 입력
        print(f"{song_num}번째 곡 메인화면에 출력.")

    def init_catagory(self):
        # 카테고리분류정보 초기화
        for idx, name in enumerate(self.category_info):
            self.category_seperate_info[name].clear()
            # 재실행 할 경우를 위해서 초기화
        for i in range(0, self.program_info):
            for idx, name in enumerate(self.category_info):
                self.category_seperate_info[name].append(
                    self.song_info[i][1][name])

        # 카테고리 별로 자료 분류
        print("카테고리 정보 갱신됨")

    def init_input_string(self):
        # 기본입력란에 정보 지우기
        for idx, name in enumerate(self.category_info):
            globals()[f"entry_{name}"].delete(0, END)
        # 섹션입력란 정보 지우기
        if self.added_section_info > 0:

            for i in range(0, self.added_section_info):
                # globals()[f"frame_list_{i}"].destroy()
                globals()[f"frame_sect_{i}"].destroy()
                globals()[f"cbx_sect_{i}"].destroy()
                globals()[f"text_sect_{i}"].destroy()
            print(f"섹션정보 {self.added_section_info}개, 초기화됨")
            self.added_section_info = 0
        else:
            print(f"섹션정보 {self.added_section_info}개, 초기화할 섹션정보 없음")

        # 추가입력란 정보 지우기
        if self.added_song_info > 0:
            for i in range(0, self.added_song_info):
                globals()[f"frame_list_{i}"].destroy()
                # globals()[f"frame_sect_{i}"].destroy()
                globals()[f"cbx_list_{i}"].destroy()
                globals()[f"text_list_{i}"].destroy()
            print(f"추가정보 {self.added_song_info}개, 초기화됨")
            self.added_song_info = 0
        else:
            print(f"추가정보 {self.added_song_info}개, 초기화할 추가정보 없음")

        print("================")

    def find_choosed_info(self):
        search_confirmed = self.cbx_searched_result.get()
        # 검색 키워드
        searched_listbox = list(self.listbox_search_result.curselection())[0]
        # 같은 키워드값중에서 몇번째 순서의 정보인지(예 :tom misch의 몇번째 곡인지) 한곡만 지목하기 위해서
        # 리스트 박스의 반환값은 튜플임 그래서 변환해서 첨자지정해서 쓰자
        print(f"사용자가 선택한 정보를 가진 곡 중에서 {searched_listbox}번째 곡")
        print(f"총{self.program_info -1}개의 정보중에서 같은 값의 정보 가져오는중")
        num_elapsed_info = -1  # 같은값 세기
        for i in range(0, self.program_info):

            if search_confirmed == self.song_info[i][1][self.searching_name]:
                # 검색키워드 비교 [곡넘버][곡정보사전][선택한카테고리]
                num_elapsed_info += 1
                # 키워드가 같은 값 갯수 세기
                print(f"{num_elapsed_info}번째곡 비교...")
            if num_elapsed_info == searched_listbox:
                # 같은 키워드를 갖고 리스트 박스에서 사용자가 선택한 값(같은 값중에 몇번째 값인지 비교)
                print(f"{i}번곡정보가 매치됨")
                return i

    def create_folder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("오디오 폴더가 이미존재함")

    def find_audio(self, song_num):
        # 접근할 폴더 경로 선언
        dirname = self.audio_path+"/"+self.song_info[song_num][1]["song name"]
        print(self.song_info[song_num][1]["song name"]+"폴더에 접근중")
        # 해당경로에 있는 파일들을 리스트로 반환
        filenames = os.listdir(dirname)
        print(filenames, " 검색됨")
        # 비교할 정규식 선언
        format_aif = re.compile("aif$")
        format_mp3 = re.compile("mp3$")
        format_wav = re.compile("wav$")
        format_m4a = re.compile("m4a$")

        audio_list = []
        auido_dir_list = []
        # 길이를비교, 새로운 파일이 있으면 실행

        try:
            print(len(self.song_info[song_num][6])+" 개의 저장된 오디오")
        except:
            print("저장된 오디오 없음")

        if len(filenames) > len(self.song_info[song_num][6]):
            # DS_store 파일 때문에 항상 참이 된다
            print("추가된 오디오 검색됨")
            for filename in filenames:
                if filename == ".DS_Store":
                    continue
                orig_name = filename
                filedir = (os.path.join(dirname, filename))
                # join -> 하나의 경로 만들기

                # 파일이 mp3포맷인지 확인
                if format_mp3.search(filename):
                    # 바뀐 이름 저장
                    orig_dir = (os.path.join(dirname, orig_name))
                    if orig_dir != filedir:
                        os.rename(orig_dir, filedir)
                    # 파일명 song_info에 저장
                    audio_list.append(filename)
                    auido_dir_list.append(filedir)

                # aif 파일 이면 mp3 파일로 변환
                else:
                    if format_aif.search(filename):
                        # 경로 스트링에 aif 지우고 mp3 넣기
                        song = AudioSegment.from_file(filedir, "aiff")
                    elif format_wav.search(filename):
                        song = AudioSegment.from_file(filedir, "wav")
                    elif format_m4a.search(filename):
                        song = AudioSegment.from_file(filedir, "m4a")

                    edit_file = filename[:-3] + "mp3"
                    edit_file_dir = (os.path.join(dirname, edit_file))
                    # 파일명에서 모듈이 못 읽어올 정보 바꾸기
                    edit_file = edit_file.replace("#", ".ver")
                    edit_file = edit_file.replace(" ", "_")
                    edit_file_dir = edit_file_dir.replace("#", ".ver")
                    edit_file_dir = edit_file_dir.replace(" ", "_")

                    song.export(edit_file_dir, format="mp3")
                    # 이전 파일 삭제
                    os.remove(filedir)
                    # 포맷된 파일 경로
                    filedir = (os.path.join(dirname, edit_file))

                    # 변환된 파일 경로 저장
                    audio_list.append(edit_file)
                    auido_dir_list.append(filedir)

                    print("mp3로 변환 완료")

        # 오디오파일 경로 song_info에 추가하기
        del self.song_info[song_num][7]
        del self.song_info[song_num][6]
        self.song_info[song_num].append(audio_list)
        self.song_info[song_num].append(auido_dir_list)

        os.remove(self.date_path + "/songinfo.pickle")
        for idx in range(0, self.program_info):
            with open(self.date_path + "/songinfo.pickle", "ab") as file:
                pickle.dump(list(self.song_info[idx]), file)

    def play_audio(self):
        idx = list(self.listbox_audio.curselection())[0]
        playsound(self.song_info[self.song_num][7][idx])

    def open_folder(self):
        song_num = self.find_choosed_info()
        dir = os.path.join(
            self.audio_path, self.song_info[song_num][1]["song name"])
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, dir])

    def search_audio(self):
        audio_root = Tk()

        # 레이아웃 생성
        frame_search = Frame(audio_root)
        frame_search.pack()
        self.entry_search = Entry(frame_search)
        self.entry_search.pack(side="left", fill="both")
        btn_search = Button(frame_search, text="검색",
                            command=self.find_searched_audio).pack(side="right")
        self.listbox_seached_audio = Listbox(audio_root, height="20")
        self.listbox_seached_audio.pack(fill="both")
        btn_play = Button(audio_root, text="재생하기",
                          command=self.play_searched_audio).pack()

        audio_root.mainloop()

    def find_searched_audio(self):
        # 리스트박스에 출력된 오디오의 경로리스트
        self.searched_audio = []
        # 여러번 검색을위해 리박스 초기화
        self.listbox_seached_audio.delete(0, END)
        # 검색어 비교
        searching = self.entry_search.get()
        for songnum in range(0, self.program_info):
            for idx, name in enumerate(self.song_info[songnum][6]):
                # 검색어와 일치하면 리스트에 넣기
                if searching in name:
                    # 아티스트,곡명,파일명,파일경로 저장하기
                    artist = self.song_info[songnum][1]["artist"]
                    song_name = self.song_info[songnum][1]["song name"]
                    file_dir = self.song_info[songnum][7][idx]
                    self.searched_audio.append(file_dir)
                    # 리스트 박스에 검색된 정보 출력
                    info = name+" , "+artist+"/"+song_name
                    self.listbox_seached_audio.insert(END, info)

    def play_searched_audio(self):
        idx = list(self.listbox_seached_audio.curselection())[0]
        playsound(self.searched_audio[idx])


get = jy()

get.root.title("mYdB")
get.root.geometry("550x540")

# 기본정보 프레임
frame_basic_info = LabelFrame(get.root, text="기본정보", relief="solid", bd=1)
frame_basic_info.pack(fill="both")
# 카테고리 추가만 하면 자동으로 다 생성하도록
# 인수의 값만큼 위젯, 각각의 값을 분류하는 사전생성
get.create_fra_ent_dic()

# 섹션정보 프레임
frame_section_info = LabelFrame(get.root, text="section", relief="solid", bd=1)
frame_section_info.pack(fill="both")

section_name = ["intro", "verse1", "verse1'", "verse2", "verse2'",
                "interude", "bridge1", "bridge2", "chorus1", "chorus2", "outro"]


# 추가 정보 프레임
frame_secondary_info = LabelFrame(get.root, text="추가정보", relief="solid", bd=1)
frame_secondary_info.pack(fill="both")

global cbx_info_get
cbx_info_get = []
global text_info_get
text_info_get = []

arr_info = ["Main Ins", "Instruments", "Arrange Tech", "Melody",
            "Rhythm", "Sound"]


# 버튼
button_section = Button(get.root, text="섹션추가", command=get.section_info_plus)
button_section.pack(side="left")

button_plus_info = Button(get.root, text="추가정보", command=get.plus_info)
button_plus_info.pack(side="left")

button_get_info = Button(get.root, text="라이브러리 저장", command=get.get_info)
button_get_info.pack(side="right")

button_search_info = Button(get.root, text="검색하기",
                            command=get.search_info_screen)
button_search_info.pack(side="right")


get.root.mainloop()
