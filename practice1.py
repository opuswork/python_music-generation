from music21 import *
import numpy as np
from scipy.io import wavfile
from synthesizer import Player, Synthesizer, Waveform

# Create a C major chord (C-E-G)
chord = stream.Stream()
c_note = note.Note("C4", quarterLength=2)  # C4
e_note = note.Note("E4", quarterLength=2)  # E4
g_note = note.Note("G4", quarterLength=2)  # G4

# Add all notes to create a chord
chord.append(c_note)
chord.append(e_note)
chord.append(g_note)

# Initialize synthesizer
player = Player()
synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)

# Create audio data
sample_rate = 44100
duration = 2  # seconds
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Piano-like envelope parameters
attack_time = 0.1  # seconds
decay_time = 0.2   # seconds
sustain_level = 0.7
release_time = 1.5  # seconds

# Create envelope
envelope = np.zeros_like(t)
attack_samples = int(attack_time * sample_rate)
decay_samples = int(decay_time * sample_rate)
release_samples = int(release_time * sample_rate)

# Attack phase
envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
# Decay phase
envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)
# Sustain phase
envelope[attack_samples + decay_samples:-release_samples] = sustain_level
# Release phase
envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

# Generate chord
chord_samples = int(sample_rate * duration)
chord_t = np.linspace(0, duration, chord_samples, False)
chord_wave = np.zeros(chord_samples)

# Piano harmonics (relative amplitudes)
harmonics = [1.0, 0.5, 0.25, 0.125, 0.0625]  # Fundamental and 4 harmonics

# Add each note to the chord
for n in chord.notes:
    freq = n.pitch.frequency
    note_wave = np.zeros(chord_samples)
    
    # Add harmonics for each note
    for i, amplitude in enumerate(harmonics):
        harmonic_freq = freq * (i + 1)  # Multiply frequency for each harmonic
        harmonic_wave = amplitude * np.sin(2 * np.pi * harmonic_freq * chord_t)
        note_wave += harmonic_wave
    
    # Apply envelope to the note
    note_wave *= envelope
    # Add to chord
    chord_wave += note_wave

# Normalize audio data
max_amplitude = np.max(np.abs(chord_wave))
if max_amplitude > 0:
    chord_wave = chord_wave / max_amplitude
chord_wave = np.int16(chord_wave * 32767)

# Save as WAV file
wav_path = 'piano_c_major_chord.wav'
wavfile.write(wav_path, sample_rate, chord_wave)

print(f"Piano-like C major chord has been saved as '{wav_path}'")
