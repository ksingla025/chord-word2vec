---New Key Detector:
The new key detection function can be found in 'findTonicNumNo7.py'.
In terms of *using* this key detection function, I looked back at my old files
and found that we mainly used it for two purposes:
	a) Counting up all the cadences in the entire corpus to find out which
	cadences were the most common (it was the IV-I cadence)
	b) Casting all of our songs from the absolute (key) notation to their
	relative (roman numeral) notation
I was able to reuse some old scripts with my new findTonicNumNo7 function in order
to redo both a) and b) with the updates key detection algorithm.
	a) The counting script is 'count_cadences_multisong_blues.py' and the
	results from it are found in 'cadence_counting_blues_results.txt'
	b) The absolute-to-relative casting script is 'cadence_converter.py'
	and the resulting dataset is 'cadences_uku_english_only_songmarkers_empty_lines_removed.txt'

IMPORTANT: for training our model, the most important file out of all of these is
'cadences_uku_english_only_songmarkers_empty_lines_removed.txt'.  I don't think you'll *need*
to use the rest unless you get curious or something.


---Total songs / lines in corpus:
Songs: 4477
Lines of chords/lyrics: 159427


---Line Numbers for Annotations:
Found in "compiled_annotations_indices.txt"
NOTE: The line numbers in this txt file are ZERO-BASED--so the first line overall,
"i 'm always screaming my lungs out , till my head starts spinning ." would be line 0.
Just be careful if you're looking for lines in a text editor which starts at line 1--then
you'll have to add 1 to each line number in the TXT file to find the correct line number
in a text editor (like Notepad++) where the line numbers start at 1.

Also note: I've included the text files "chords_uku_english_only_songmarkers_empty_lines_removed.txt"
and "lyrics_uku_english_only_songmarkers.txt".  These two files have been formatted so they have
exact line-to-line correspondence between the correct chord and lyric lines. (e.g. line 1 in the
chords file goes with line 1 in the lyrics file and so on.)