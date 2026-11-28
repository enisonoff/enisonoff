---
name: house-style
description: Elena's DEFAULT look for talking-head news reels, approved on the outage video ("The fixes are breaking everything", Nov 2026). Film-graded footage, big lowercase Anton words tucked behind her head, soft rounded secondary lines, sourced headline clippings, B&W B-roll stills with a slow push-in, split screens for explanations, clean shadowed phrase captions, everything snapping on with her voice. Use for every new reel edit unless she names another style (bloomberg-style, zauey title cards), and whenever she says "my style", "default style", "like the outage video" or "like the last reel".
---

# House style (default reel look)

Reproduces the approved outage reel v6 exactly. `reference/outage_beats.py` is that video's beat list, and rendering it through `scripts/reel_style.py` matches the v6 frames pixel for pixel.

Her process still applies: **plan → storyboard → wait for her OK → render.** Fact-check everything on screen, and use `context/video-rules.md` for any rule not covered here.

## Pipeline
```
- [ ] 1. clean-cut skill: last takes, nothing clipped. EDL: "maxgap": 0.08, "trim_edges": true, "lead": 0.032, "tail": 0.056
         Re-transcribe cut.wav and read it all. Watch for merged retakes ("one former NSA, one former NSA hacker").
- [ ] 2. make_roughcut.py cut.mov plan.json roughcut.mp4 "A-B@1.15" "B-C@1.3"   (push-ins on emphasis lines only; ends snap to cuts)
- [ ] 3. Masks for every frame: edit-video/scripts/masks.py roughcut.mp4 WORKDIR/m 0 END   (2 jobs in parallel, ~35 min for 3 min)
- [ ] 4. Transcribe roughcut audio -> words.json (clean-cut takes.py). This drives the captions.
- [ ] 5. Copy reference/outage_beats.py -> WORKDIR/beats.py and write this video's beats (vocabulary below)
- [ ] 6. Storyboard: import reel_style, call compose(frame, fi, t, t) for one moment per beat, tile the frames, send, wait
- [ ] 7. Render ONE process (pgrep -af reel_style first). New filename per version. Then:
         ffmpeg -v error -xerror -i out.mp4 -f null -  ->  loudnorm -14 copy  ->  phone copy (3.5 Mbps)
```
```bash
K=.claude/skills/house-style/scripts
export REEL_DIR=$WORK REEL_SRC=$WORK/roughcut.mp4 REEL_WORDS=$WORK/words.json REEL_BEATS=$WORK/beats.py
# fonts: fontsource packages in $(dirname $WORK)/fonts or REEL_FONTS: anton dosis inter inter-tight libre-baskerville archivo-black
python3 $K/reel_style.py 0 END $WORK/reel-v1.mp4
```
Notes changes that alter the cut (removed words, tighter pacing) after beats are written: keep the beats on the old cut and set `REEL_TMAP=$K/tmap.py TMAP_OLD=old_plan.json TMAP_NEW=new_plan.json`. Graphics and masks map through source frames; captions follow the new transcript.

## The look
- **Grade**, every frame (`grade()`):
  - background desaturated 35%, but only 12% darker; she flagged it when it was darker;
  - a wide soft mask edge, so no light ring shows behind her head;
  - contrast 1.15, teal shadows, warm mids, matte blacks, highlight glow, vignette, grain.
- **Palette:** red (232,40,44), warm white (250,247,240) and near-black. No other colors except headline paper and flags.
- **Big words:** Anton, lowercase.
  - Behind her head via the cutout, auto-placed just above the top of her head (`auto=True`), never over her face.
  - 25% bigger on cards and splits. Words behind her stay frame-width, because bigger just hides more of the word.
- **Secondary lines:** Dosis 500 as a stand-in for Softedge (her Edits font). Tucked above-left of the big word, white on footage.
- **Snap-on:** every element lands in 4 frames: 0.8 → 1.06 → 1.0, a 24 px rise, starting 1.5 frames early so it hits the word. Every element has a soft drop shadow.
- **Captions** (`subtitle()`):
  - Inter Tight 700, 74 px, tight tracking, sentence case, white, no outline, soft shadow.
  - Phrases up to ~6 words on 1-2 balanced lines, with no one-word leftovers. The whole phrase pops in on her voice.
  - Chest height on her footage; straddling the divider on split screens.
- **Pacing:** pauses at cuts 0.08 s. Push-ins of 1.15x / 1.3x on emphasis lines only, ending exactly on a cut.

## Beat vocabulary (in beats.py; times are cut seconds)
| Call | What it makes | Used for |
|---|---|---|
| `behind(a, b, t_small, 'small line', t_big, 'big word', RED, 0, auto=True)` | big Anton word behind her head, small Dosis line above it | the hook, key nouns ("software update", "dark ages") |
| `..., brk=T` on the hook | holds through the word, then each word cracks in half and falls away | the opening line |
| `card(a, b, [Item(...)])` | black grain card | thesis line only ("the fixes are / breaking / everything") |
| `card` + `Clip(t, clipping(outlet, date, headline, 'key words'))` | sourced headline clippings landing one per item, key words on a red bar | any list of news events |
| `over(a, b, [Clip(...)])` | clippings over her chest, face stays on | official quotes and headlines mid-explanation |
| `broll(a, b, '04', [Item(...)])` | B&W still from broll/04.png, slow 8% push-in, words on the picture | a line with a picture: put its words on the picture |
| `broll(a, b, fn)` | a drawn scene, `fn(t, a, b, h)` returns the frame (e.g. `sign.fence_scene`) | gags like the WARNING / BEWARE OF AI MODEL sign |
| `split(a, b, items, bg='11', panel=fn)` | graphic on top, her below, red divider | explanations; the top shows the analogy literally (the broken-locks list + PUBLIC stamp) |
| `Counter(t0, 948, t1, 61, ANTON(400), y)` | number snaps on, then rolls down and turns red | any number that changes |
| `Flag(t, 'us'/'cn', x, y)` in a behind scene | waving flags on either side of her head, tucked behind her hair | countries |

## What she rejected (don't bring back)
- The first style pass: uppercase, plain, not stylish. Emphasis words are always lowercase.
- A wall darkened so much that a light ring showed behind her head.
- Per-word "Classic" bounce captions with a black outline: uneven mid-bounce, template look.
- Quick text, then a picture. Put the text on the picture.
- Split screens whose top half doesn't literally show the line (the dark hallway for "every broken lock").
- Static "948 holes found / 61 fixed" labels. Make the number move.
- Ending on a black card. End on her face.
- Any CTA ("comment TOWN").
- Unsourced quotes. If there is no published quote with her word ("flicker"), use the closest sourced headline and say so.

## Gotchas
- Two renders writing one file corrupted a whole render. Kill queued jobs by ID and check `pgrep` first.
- Whisper merges retakes, and gives different words on identical audio between runs. Check suspicious spots with `zones.py`. Sibilants (the "s" in "attacks") sit below -42 dB, so look at high-frequency energy before trimming.
- Higgsfield generations spend her credits and this session's permission check blocks them without her explicit OK. Ask first: ~1 credit per still, 10-12 per 4 s video. Wikimedia / DVIDS downloads are rate-limited or blocked from the container, so draw the graphic or ask her for the file.
