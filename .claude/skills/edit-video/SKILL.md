---
name: edit-video
description: Edit one of Elena's vertical talking-head news videos for Instagram, the way her approved edits were built (SpaceX chip loan, Jensen winners & losers). Plan from the transcript, design-check, storyboard and wait for her OK, send a low-quality preview, then a full-quality render that passes the flash and sync checks. Use when she shares a raw video or Drive link and says "edit this", "plan this edit", "storyboard", "add graphics", or gives notes on a storyboard, preview or render.
---

# Edit video

Read `context/video-rules.md` first. It holds every rule she has given. This file is the order of work.

## Checklist
```
- [ ] 1. Get the file, check frame rate, transcribe
- [ ] 2. Fact-check every number/quote that will be on screen
- [ ] 3. Beat plan (what she says -> what's on screen), using reference-video learnings
- [ ] 4. Design check: 2-4 options of anything new (fonts, layouts), side by side
- [ ] 5. Storyboard every beat -> STOP and wait
- [ ] 6. Apply notes -> re-storyboard only what changed -> wait
- [ ] 7. Low-quality preview (540x960) -> wait
- [ ] 8. Full-quality render -> run check_render.py -> send
- [ ] 9. Save any new rule into context/video-rules.md
```

### 1. File and transcript
- Drive: `curl -sL -o raw.mp4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`. An HTML page back means it's private: ask her to share it.
- `ffprobe` the frame rate. Phone footage is **variable frame rate**; never use `select=` + `setpts=N/...` on it (that drifted audio ~1 s by the end). Decode with `trim=a:b,setpts=PTS-STARTPTS,fps=30` per segment and concat.
- `scripts/transcribe.py` with every proper noun in `--prompt`. Fix misheard names in captions (Nebius, IREN, Bessent, Huang).
- `scripts/jumpcuts.py raw.mp4 > jumpcuts.txt`. Her footage already has jump cuts; graphics must snap to them.

### 2. Fact-check
Every number, quote and headline on screen needs a source found this session. Search, don't recall. Use exact figures (Forbes $33.7B, not "$34B"). If a headline she sends can't be found, ask which outlet before using it. Show "approx." or the intraday caveat when a number isn't a close.

### 3. Beat plan
- **Don't cut her words** unless she asks. If she asks to cut a repeat, re-time that stretch with `--model medium.en` and cut in the silence between words (small.en edges were 0.2 s off and left half a word in).
- Pick graphics only where they add something. Aim for long stretches of just her; she called 30 graphics in 2:45 "busy." Flag anything that restates what she says and offer to cut it.
- Pull reference reels she sends with Scrape Creators (`api.scrapecreators.com/v2/instagram/post`, header `x-api-key`; the key is in the environment, never print it). If `/reel/` 404s, retry `/p/`.

### 4-6. Design and storyboard
- Build storyboard frames with the real compositor at 1080x1920, then shrink. Draw the safe-zone lines (y=250, y=1560). Label each tile with the timestamp and a one-line note.
- After notes, re-storyboard; never render straight from notes. She says "storyboard first" often; assume it.

### 7-8. Preview, render, checks
- Low-quality preview first (`-vf scale=540:960 -crf 30 -preset veryfast`) when she asks or when timing changed a lot.
- Full quality: libx264 crf 16 preset slow, AAC 192k, loudnorm I=-14.
- Before sending ANY render: `scripts/check_render.py render.mp4 raw.mp4 <out:src pairs>` -> short flashes must be `[]`, sync offsets 0 or ±0.033. Also pull a frame sheet and look at it.

## Building blocks (see `reference/`)
Default cutaway look: the `bloomberg-style` skill (neon timeline, glowing charts). The pieces below are the earlier whiteboard look.

`reference/renderE.py` is the final Jensen edit (it execs `sbE.py` -> `renderD.py` -> `sbD.py` -> ... for helpers; fix the hardcoded scratchpad paths at the top of each before reuse). Pieces worth reusing:
- `poster_at` / `word_plan`: centered two-font posters above her head (Instrument Serif italic lead-in + tall Anton caps in blue), words landing one at a time with a blur-in.
- `venn_faces` + `circle_face`: the winners/losers Venn with centered face bubbles (head found via the narrowest "neck" row of the cutout), logo chips for companies, icon/word chips for groups.
- `timeline_quotes`: two quote cards with a dotted connector and a lime "N days later" pill; optional face cutout.
- `clip_card`: headline clipping with lime highlights on key words, outlet + date on top.
- `chart_anim`: one simple XY chart, lines drawing in from the origin, each line labeled at its end.
- `make_bill`: her billion-dollar-bill template with a portrait in the center oval.
- `frame_at` (clones_anim.py): the clone gag, pops accelerating, a giant one last, title on a white tag.
- `card_layer` + `mask_src`: a photo tucked just behind her head using per-frame masks (`scripts/masks.py`).
- snapping + `audit()`: closes gaps < 0.5 s between graphics and snaps every boundary to her jump cuts.
- `spacex_render.py`: full-screen cutaways with motion (space render with a beam of light the camera follows, a chatbot message turning into an energy ball, the $44B rack building, the guarantee umbrella); `spacex_sfx.py`: synthesized subtle clicks.

## Setup in a fresh session
```bash
python3 -m venv ~/.venvs/asr && ~/.venvs/asr/bin/pip install -q faster-whisper numpy
python3 -m venv ~/.venvs/seg && ~/.venvs/seg/bin/pip install -q "rembg[cpu]" pillow scipy
cd $S/fonts && for p in montserrat anton instrument-serif inter jetbrains-mono; do npm pack @fontsource/$p && mkdir -p $p && tar xzf fontsource-$p-*.tgz -C $p; done
npm pack simple-icons   # logos (older versions, e.g. 9.21.0, still have openai)
```
Wikimedia rate-limits hard here (429s): ask Elena for photos rather than waiting on downloads.
