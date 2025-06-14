##--------------------------------------------------------------------------
##
## Simple Canon Variation Style
##
##--------------------------------------------------------------------------

from music21 import stream, note, chord, meter, key, tempo

# Create a score
score = stream.Score()

# Set time signature, key, and tempo
part = stream.Part()
part.append(tempo.MetronomeMark(number=90))
part.append(key.Key('D'))
part.append(meter.TimeSignature('4/4'))

# Canon-like bass line (typical to Pachelbel)
bass_line = ['D2', 'A2', 'B2', 'F#2', 'G2', 'D2', 'G2', 'A2']

# Add bass notes as whole notes
for pitch in bass_line:
    n = note.Note(pitch)
    n.duration.quarterLength = 4
    part.append(n)

# Add right-hand broken chords (a very simplified version)
right_hand = stream.Part()
right_hand.id = 'Piano_RH'
right_hand.append(tempo.MetronomeMark(number=90))
right_hand.append(key.Key('D'))
right_hand.append(meter.TimeSignature('4/4'))

chord_progression = [
    ['D4', 'F#4', 'A4'],
    ['A3', 'C#4', 'E4'],
    ['B3', 'D4', 'G4'],
    ['F#3', 'A3', 'D4'],
    ['G3', 'B3', 'D4'],
    ['D3', 'F#3', 'A3'],
    ['G3', 'B3', 'D4'],
    ['A3', 'C#4', 'E4']
]

for c in chord_progression:
    arpeggio = stream.Voice()
    for pitch in c:
        n = note.Note(pitch)
        n.duration.quarterLength = 1
        arpeggio.append(n)
    right_hand.append(arpeggio)

# Combine both parts into a score
score.insert(0, part)
score.insert(0, right_hand)

# Show the score (requires MuseScore or musicXML viewer)
score.show()
