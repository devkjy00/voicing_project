from refactoring import Chord, Voicer, ChromaticScale
import pytest


@pytest.fixture
def chromatic_scale():
    scales = ChromaticScale('C')
    return scales


class TestChromatic:

    def test_get_long_chromatic(self, chromatic_scale):
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
        ), "wrong chromatic_scale._long_chromatic"

    def test_sort_chromatic_by(self, chromatic_scale):
        assert chromatic_scale.sort_chromatic_by('E') == ["E", "F", "Gb", "G",
                                                          "Ab", "A", "Bb", "B",
                                                          "C", "Db", "D", "Eb"
                                                          ], "wrong chromatic_scale.sort_chromatic_by"

    def test_get_sliced_chromatic(self, chromatic_scale):
        assert chromatic_scale.get_sliced_chromatic('B1') == (
            'C1', 'Db1', 'D1', 'Eb1', 'E1', 'F1',
            'Gb1', 'G1', 'Ab1', 'A1', 'Bb1'), "wrong chromatic_scale.get_sliced_chromatic"


@pytest.fixture
def chord():
    return Chord('C')


class TestChord:
    def test_chord_attribute(self, chord):
        assert chord.diatonic == [['C', 'M7'], ['D', 'm7'], ['E', 'm7'],
                                  ['F', 'M7'], ['G', '7'], ['A', 'm7'], ['B', 'm7b5']], "wrong chord.diatonic"
        assert chord._diatonic_note_idx == [0, 2, 4, 5, 7, 9, 11], "wrong chord._diatonic_note_idx"


@pytest.fixture
def voicer():
    voicer = Voicer()
    return voicer


class TestVoicer:
    def test_four_part_voicing(self, voicer):
        assert voicer('2b7') == ['Db4', 'F4', 'Ab4', 'B3'], "wrong four_part"
