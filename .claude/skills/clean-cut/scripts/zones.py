"""Inspect splice zones: speech bursts (energy > -40 dB) plus a fresh transcription of just that window.
Long whisper words (e.g. "that[13.76-18.26]") usually hide a pause or a retake; this shows where the speech really is.
usage: python zones.py AUDIO.wav 12.0:18.8 59.4:65.4 ...   (48 kHz mono wav, times in audio seconds)"""
import sys, wave
import numpy as np
from faster_whisper import WhisperModel

w = wave.open(sys.argv[1]); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
m = WhisperModel('medium.en', compute_type='int8')
for spec in sys.argv[2:]:
    a, b = map(float, spec.split(':')); seg = x[int(a * sr):int(b * sr)]
    hop = sr // 100; n = len(seg) // hop
    db = 20 * np.log10(np.sqrt((seg[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    bursts, on = [], None
    for i, v in enumerate(db):
        if v > -40 and on is None: on = i
        if v <= -40 and on is not None:
            if i - on > 3: bursts.append((round(a + on / 100, 2), round(a + i / 100, 2)))
            on = None
    if on is not None: bursts.append((round(a + on / 100, 2), round(b, 2)))
    a16 = seg[::sr // 16000] if sr % 16000 == 0 else seg
    segs, _ = m.transcribe(a16, word_timestamps=True, condition_on_previous_text=False, beam_size=5)
    words = ' '.join(f'{wd.word.strip()}[{a + wd.start:.2f}-{a + wd.end:.2f}]' for s in segs for wd in s.words)
    print(f'=== {a}-{b}\n bursts: {bursts}\n words: {words}')
