"""Repeat-safe transcription: keeps every retake (default whisper settings silently drop repeated phrases).
usage: python takes.py AUDIO_OR_VIDEO OUT.json ["Proper, Nouns, To, Prime"]
Prints phrases split on pauses > 0.45 s with their times. Needs faster-whisper + numpy + ffmpeg."""
import json, sys, subprocess
import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
prompt = (sys.argv[3] + '. ') if len(sys.argv) > 3 else ''
audio = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                                     capture_output=True, check=True).stdout, dtype=np.int16).astype('float32') / 32768
m = WhisperModel('medium.en', compute_type='int8')
segs, _ = m.transcribe(audio, word_timestamps=True, condition_on_previous_text=False, vad_filter=False, beam_size=5,
                       initial_prompt=prompt + 'Um, uh, so, so this would be,')
words = [dict(w=w.word, s=round(w.start, 2), e=round(w.end, 2)) for s in segs for w in s.words]
json.dump(words, open(out, 'w'))
line, t0, last = [], None, None
for x in words:
    if last is not None and x['s'] - last > 0.45 and line:
        print(f'{t0:7.2f}-{last:7.2f} | ' + ' '.join(line)); line, t0 = [], None
    if t0 is None: t0 = x['s']
    line.append(x['w'].strip()); last = x['e']
if line: print(f'{t0:7.2f}-{last:7.2f} | ' + ' '.join(line))
