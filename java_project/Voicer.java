
public class Voicer {
	public static void main(String[] args) {
	ChromaticScale s = new ChromaticScale();

	}
}

class ChromaticScale {
    protected static String[] chromaticScale = new String[]{"C", "Db", "D", "Eb","E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
    protected static String[] octave = new String[]{"1", "2", "3", "4"};
    protected static int[] majorDiaScaleIdx = new int[]{0, 2, 4, 5, 7, 9, 11};
    protected static int[] minorDiaScaleIdx = new int[]{0, 2, 3, 5, 7, 8, 10};
	protected static String[] chromaticOctave = new String[chromaticScale.length * octave.length];
	{
	int i = 0;
	for(String s : chromaticScale){
		for(Stirng o : octave) {
		chromaticOctave[i++] = 
			
		}

	}
	}
    def _get_long_chromatic(self) -> tuple:
        return tuple(i + j for j in self._octave
                     for i in self._chromatic_scale)

	

		
} // class ChromaticScale
