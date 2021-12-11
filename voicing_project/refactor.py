# TDD로 다시 짜기

import unittest, pytest

class SongKey:
    def __get__(self, instance, owner):
        # try:
            print(f'{instance}의 키는 {instance.__dict__[self.key]}입니다')
        # except AttributeError:
        #     print( '키가 생성되지 않았습니다')

    def __set__(self, instance, value):
        pass

class Voicer:
    key = SongKey()

    def __init__(self) -> None:
        pass

    


class TestVoicer(unittest.TestCase):
    def test_song_key(self):
        with self.assertRaises(AttributeError):
            tester = Voicer()   
            tester.key

unittest.main()
