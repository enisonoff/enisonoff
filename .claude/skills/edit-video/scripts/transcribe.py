"""Word-level transcript.
usage: ~/.venvs/asr/bin/python transcribe.py VIDEO OUT.json [--model small.en|medium.en] [--prompt "Nvidia, Jensen Huang"] [--start S --dur D]
Writes [{"w","s","e"}] (seconds in the source video) and prints the transcript.
Use medium.en on any stretch you plan to cut: small.en timings can be off by ~0.2 s at word edges.
"""
import argparse, json, subprocess, numpy as np
from faster_whisper import WhisperModel
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('out')
ap.add_argument('--model', default='small.en'); ap.add_argument('--prompt', default=''); ap.add_argument('--start', type=float, default=0); ap.add_argument('--dur', type=float, default=0)
a = ap.parse_args()
cmd = ['ffmpeg', '-v', 'error', '-ss', str(a.start), '-i', a.video] + (['-t', str(a.dur)] if a.dur else []) + ['-ac', '1', '-ar', '16000', '-f', 's16le', '-']
audio = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.int16).astype('float32') / 32768
segs, _ = WhisperModel(a.model, compute_type='int8').transcribe(audio, word_timestamps=True, initial_prompt=a.prompt or None)
ws = [dict(w=x.word.strip(), s=round(a.start + x.start, 3), e=round(a.start + x.end, 3)) for s in segs for x in s.words]
json.dump(ws, open(a.out, 'w')); print(len(ws), 'words'); print(' '.join(f"{w['w']}@{w['s']}" for w in ws))
