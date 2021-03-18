# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:29:01 2017

@author: greert
"""
import re
import caster
import base64
import _pickle as cPickle

def makeFlatsSharps(text):
    text = text.replace('Db','C#')
    text = text.replace('Eb','D#')
    text = text.replace('Gb','F#')
    text = text.replace('Ab','G#')
    text = text.replace('Bb','A#')
    return text

def letterChordToNumChord(letterChord,noteNums):
    numChord = letterChord
    for note in noteNums:  # for each note C, C#, D, ...
        for i in range(0, len(numChord)):  # for each letter in the numChord
            if len(note[0]) == 2:  # If it's a sharp note
                if i < len(numChord) - 1 and note[0] == numChord[i:i + 2]:  # If there's a substring match
                    numChord = numChord[0:i] + 'w' + str(note[1]) + numChord[i + 2:len(numChord)]
            else:  # for all the naturals
                if note[0] == numChord[i]:  # If there's a substring match
                    numChord = numChord[0:i] + 'w' + str(note[1]) + numChord[i + 1:len(numChord)]
    return numChord

def shiftNumChord(origChord, shift):
    newChord = origChord
    i = 0  # have to use a while loop bc len(newChord) is changing
    while i < len(newChord):  # for each letter in the newChord
        selectionSize = 0
        if newChord[i] == 'w':
            # if the next digit is a 1 look for the next digit being 0 or 1 (i.e., 10 or 12)
            if newChord[i + 1] == '1' and i < len(newChord) - 2 and \
                    (newChord[i + 2] == '0' or newChord[i + 2] == '1'):
                selectionSize = 3;
            else:
                selectionSize = 2;
            wdigit = int(newChord[i + 1:i + selectionSize])
            newdigit = shiftNumber(wdigit,shift)
            newChord = newChord[0:i] + 'w' + str(newdigit) + newChord[i + selectionSize:len(newChord)]
        i += 1
    return newChord

def shiftNumber(num, shift):
    num+=shift
    if num<0:
        num+=12
    else:
        num = num%12
    return num

def numChordToLetterChord(numChord):
    letterChord = numChord
    i=0 #have to use a while loop bc len(letterChord) is changing
    while i < len(letterChord):  # for each letter in the letterChord
        selectionSize=0
        if letterChord[i]=='w':
            #if the next digit is a 1 look for the next digit being 0 or 1 (i.e., 10 or 12)
            if letterChord[i+1]=='1' and i<len(letterChord)-2 and \
                (letterChord[i+2]=='0' or letterChord[i+2]=='1'):
                selectionSize=3;
            else:
                selectionSize=2;
            wdigit = int(letterChord[i+1:i+selectionSize])
            for note in noteNums:
                if note[1]==wdigit:
                    # replace the entire 'w'+digit with the corresponding note
                    letterChord = letterChord[0:i] + str(note[0]) + letterChord[i+selectionSize:len(letterChord)]
                    break
        i+=1
    return letterChord

with open('chords_and_lyrics_full.txt', 'r') as myFile:
    temp_text = myFile.readlines()
print(type(temp_text[4]))
print(temp_text[4])

#read in chord casting table
with open('chord_casting_UTF-8.txt', 'r') as f:
    inputs=[]
    outputs=[]
    exploLine=[]
    for line in f:
        exploLine = line.split("\t")
        inputs.append(exploLine[0].replace('\ufeff','').strip()) #clean up the special chars
        outputs.append(exploLine[1].replace('\n', '').strip()) #clean up special chars
    castingTable = list(zip(inputs, outputs))
    castingTable = castingTable[1:]
    print("Opened Chord Casting Table")
print(castingTable) #test

def nm(name, x):  # named capture group
    return r'(?P<' + name + '>' + x + r')'
#define re rules
re_natural = r'[A-G]'
re_modifier = r'#*b*'
re_note = (re_natural + re_modifier)
re_chord = (r'(maj|min|dim|aug|add|sus|m)')
re_interval = (r'([1-9]|1[0-3])')
re_slash = '/'
re_optional = r'('+re_chord+'|'+re_interval+'|'+re_slash+'|'+re_note+')'
returnablePattern = re_note + re_optional + r'*'
chordPattern = (r'\s' + nm('chordRet', returnablePattern) + r'\s')
#find matches
big_list_of_chords = []
big_list_of_lyrics = []
chordflag = False
lyricflag = False
for u in range(len(temp_text)):
    fullText = temp_text[u]
#    fullText = fullText.decode('utf-8')
    matchIter = re.finditer(chordPattern, fullText)
    origChords = []
    for elem in matchIter:
        s = elem.start()
        e = elem.end()
        #print('Found "%s" in the text from %d to %d ("%s")' % \
        #      (elem.re.pattern, s, e, elem.group('chordRet') ))
        #check for special case "Am I"
        #Removed because it would just recast Am as Am
        if elem.group('chordRet') != 'Am' or e >= len(fullText) or fullText[e] != 'I':
            origChords.append(elem.group('chordRet'))
        #We should append A minor still?        

        
    
    #make a new list with the cast of each chord, using the table, and count the amount of each chord
    castedChords = []
    #have to check the sharps first so it doesn't switch 'C#' into 'w0#'
    noteNums = [('C#',1),('D#',3),('F#',6),('G#',8),('A#',10),('C',0),('D',2),('E',4),('F',5),('G',7),('A',9),('B',11)]
    
    for origChord in origChords:
        #example of process: E/C# -> w4/w1 -> w0/w9 (store shift as 4) -> C/A -> Am -> w9m -> w1m -> C#m
        #convert origChord to numeral version
        origChord = makeFlatsSharps(origChord)
        tempChord = letterChordToNumChord(origChord,noteNums)
        #shift numeral chord to C numeral version
        if tempChord[1]=='1' and len(tempChord)>2 and \
            (tempChord[2]=='0' or tempChord[2]=='1'):
            rootNum = int(tempChord[1:3])
        else:
            rootNum = int(tempChord[1])
        shift = rootNum
        tempChord = shiftNumChord(tempChord, -shift)
        #convert C numeral version to C letter version
        tempChord = numChordToLetterChord(tempChord)
        #cast C letter version using table
        for chord in castingTable:
            if tempChord == chord[0]:
                tempChord = chord[1]
                break
        #convert casted letter chord to casted numeral chord
        tempChord = letterChordToNumChord(tempChord,noteNums)
        #shift casted numeral chord back
        tempChord = shiftNumChord(tempChord, shift)
        #convert casted numeral chord to casted letter chord
        tempChord = numChordToLetterChord(tempChord)
        #print('Converted '+origChord+' to '+tempChord)
        castedChords.append(tempChord)
    if castedChords:
        if chordflag == True:
            lyricflag = False
            big_list_of_chords[-1].extend(castedChords)
            chordflag = True
        else:
            lyricflag = False
            chordflag = True
            big_list_of_chords.append(castedChords)
    else:
        if chordflag == True and lyricflag == False:
            chordflag = False
            lyricflag = True
            fullText = fullText.encode('utf-8').decode('utf-8')
#            fullText = fullText.decode('utf-8')
            print(fullText)
            big_list_of_lyrics.append(fullText)
        if chordflag == False and lyricflag == True:
#            print(big_list_of_lyrics[-1])
            fullText = fullText.encode('utf-8').decode('utf-8')
            big_list_of_lyrics[-1] = big_list_of_lyrics[-1]+fullText
#print big_list_of_lyrics
#print big_list_of_chords
print(len(big_list_of_chords))
print(len(big_list_of_lyrics))
print(len(temp_text))
cPickle.dump( big_list_of_lyrics, open( "lyrics.p", "wb" ) )
cPickle.dump( big_list_of_chords, open( "chords.p", "wb" ) )