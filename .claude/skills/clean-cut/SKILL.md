---
name: clean-cut
description: First editing round on Elena's raw talking-head footage. Keeps the last clean take of every line, removes restarts, laughs and false starts, tightens pauses to ~0.06-0.1 s, never clips a word, then proves it by re-transcribing the cut. Use when she sends raw footage/a Drive folder and says "cut the repeats", "take out retakes", "run an editing round", "rough cut", or "tighten the gaps". Graphics come after, with the edit-video skill.
---

# Clean cut (retakes out, gaps tight, nothing clipped)

Her standing notes for this step (from `context/video-rules.md` and past rounds):
- Keep the **last full take** of every line. If the last one stumbles ("and And"), use the cleanest complete take.
- **Never cut off a sentence or a syllable.** Every kept sentence must read whole.
- Pauses between words: **about 0.06-0.1 s** ("a little tighter" than 0.1).
- Cut laughs and asides she flags; cut half-sentences she abandoned.
- Don't cut her words otherwise. Flag (don't silently drop) unverified claims she ad-libbed.
- Pickups/re-recorded lines in a second clip replace the matching section.

## Steps
```
- [ ] 1. Download (Drive: drive.usercontent.google.com/download?id=ID&export=download&confirm=t), ffprobe offsets
- [ ] 2. Extract 48 kHz mono wav per clip
- [ ] 3. takes.py on each clip -> every retake visible (default whisper hides repeats!)
- [ ] 4. Pick the last full take of each line -> write the EDL
- [ ] 5. zones.py on every splice and on every suspiciously long word -> fix edges to burst boundaries
- [ ] 6. cut.py EDL audio -> takes.py cut.wav -> READ THE WHOLE TRANSCRIPT
- [ ] 7. Fix: missing words, doubled words, clipped endings -> repeat 6 until clean
- [ ] 8. cut.py EDL render -> 540x960 preview -> send, list what was cut and what's flagged
```

```bash
K=.claude/skills/clean-cut/scripts; ASR=~/.venvs/asr/bin/python
ffprobe -v error -show_entries stream=codec_type,start_time -of compact a.mov   # audio start_time = offset
ffmpeg -v error -y -i a.mov -vn -ac 1 -ar 48000 a.wav
$ASR $K/takes.py a.wav wa.json "Anthropic, Mythos, OpenAI, Linux"
$ASR $K/zones.py a.wav 12.0:18.8 59.4:65.4
python3 $K/cut.py edl.json audio && $ASR $K/takes.py cut.wav wcut.json
python3 $K/cut.py edl.json render
ffmpeg -v error -y -i cut.mov -vf scale=540:960 -c:v libx264 -crf 28 -preset veryfast -c:a aac -b:a 128k preview.mp4
```

## What went wrong before (and the fix built into the scripts)
- **Whisper silently dropped repeated takes** ("and that, and that conversation…"), so cuts left restarts in. Fix: `takes.py` uses `condition_on_previous_text=False`, and step 6 re-transcribes the cut.
- **Long word stamps hide pauses and retakes** (`that[13.76-18.26]`). Fix: `zones.py` shows the speech bursts; set edges there.
- **Gap tightening clipped quiet consonants and soft words** ("firs-", "for security" lost). Fix: silence = below -47 dB, only pauses > maxgap+0.06 s get shortened, with padding.
- **Cutting at the quietest point between glued words can still clip a tail** ("suck-" for "sucker"). Fix: re-transcribe and read; when a word looks short, move the edge to the end of its burst.
- **A broken pipe (`| head`) once stopped the audio write**, so the check ran on the old file. Don't pipe cut.py into head.

## Then
Graphics, captions, title: `edit-video` skill + house style in `context/video-rules.md`. Run `check_render.py` on the final.
