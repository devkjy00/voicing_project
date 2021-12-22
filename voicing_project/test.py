import pytest
from unittest import TestCase, main
from refactor import SongKey, Voicer, ChromaticScale



@pytest.fixture
def chromatic_scale():
    scales = ChromaticScale()
    return scales

def test_get_long_chromatic(chromatic_scale):
    assert chromatic_scale._long_chromatic == (
            "C1",
            "Db1",
            "D1",
            "Eb1",
            "E1",
            "F1",
            "Gb1",
            "G1",
            "Ab1",
            "A1",
            "Bb1",
            "B1",
            "C2",
            "Db2",
            "D2",
            "Eb2",
            "E2",
            "F2",
            "Gb2",
            "G2",
            "Ab2",
            "A2",
            "Bb2",
            "B2",
            "C3",
            "Db3",
            "D3",
            "Eb3",
            "E3",
            "F3",
            "Gb3",
            "G3",
            "Ab3",
            "A3",
            "Bb3",
            "B3",
            "C4",
            "Db4",
            "D4",
            "Eb4",
            "E4",
            "F4",
            "Gb4",
            "G4",
            "Ab4",
            "A4",
            "Bb4",
            "B4",
        )

def test_sort_chromatic_by(chromatic_scale):
    chromatic_scale.sort_chromatic_by("E")
    assert chromatic_scale._chromatic_scale == ("E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb")
        
@pytest.fixture
def voicer():
    voicer = Voicer()
    return voicer


@pytest.fixture
def song_key():
    song_key = SongKey()
    return song_key

def 