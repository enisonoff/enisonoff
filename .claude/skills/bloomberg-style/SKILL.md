---
name: bloomberg-style
description: Edit or design Elena's videos, cutaways and carousels in the Bloomberg Business explainer look she loves — a glowing timeline spine the camera travels down, huge date numbers, duotone photos in neon frames, glowing line charts, dark navy background, plain white captions. Use when she says "Bloomberg style", "like the Bloomberg reel", "timeline style", "neon", or asks for a recap/timeline of a story, and as the default look for cutaways in new edits unless she asks for another style.
---

# Bloomberg style

Reference: @bloombergbusiness "Jensen recap" reel, https://www.instagram.com/reel/DgLYL2By15M/ (43 s, faceless narration). Full breakdown in `context/learnings.md`. Follow `context/video-rules.md` and the `edit-video` skill for process (plan → storyboard → wait → preview → render + checks); this skill is the look.

## The look
| Element | Spec |
|---|---|
| Background | Near-black navy (#02060E → #0A182C), radial vignette, faint diagonal falling streaks that drift with the camera |
| Spine | One vertical glowing line at x≈300 (of 1080), runs top to bottom through every timeline frame. Glow: wide soft blue (#14A0FF) + bright core (#AAEBFF) |
| Timeline stop | White dot on the spine, dotted rule to the right. Huge day number left of the spine (Inter 800, ~210 px, white). Month right of it (Inter 800, 56 px). 1-3 short summary lines (Inter 600, 42 px, gray #A5AFBE) |
| Media | Photo or clip in a thin glowing frame, converted to a blue-gray duotone, slides up + fades in (~0.4 s). "Credit: ___" in small dim gray under it |
| Camera | Pans down the spine to the next stop (~0.6 s ease-out), one stop every ~4-6 s, matched to when she says the date |
| Charts | One glowing mint line (#3CF0D2) drawing left to right on the dark background, faint gridlines with $ labels on the right, white dot + big white value at the end. No boxes, no legend |
| Captions | White, Inter 700 ~54 px, sentence case, full phrase on 1-2 lines, lower third (y≈1420), no highlight box, no outline |
| Numbers / headlines | Big white Inter 800. Losses in soft red (#FF5A50) only when the number is the point |
| Palette | Navy, glow blue, white, gray. One accent at most (mint for charts, red for a loss). Elena's brand blue (#1803BB) can replace the glow color if she asks |

## How to use it on Elena's talking videos
- Her shots stay as they are; the cutaways switch to this look.
- Any run of dates/events in the script ("last week… Monday… Tuesday…") becomes one timeline sequence: one stop per date, camera panning between them, instead of separate graphics.
- Stats become a glowing chart or one big white number; analogies (IOU, receipts) go inside a neon frame.
- Keep it sparse: a stop needs a date, ≤3 lines and at most one photo.
- Every date, number and quote on a stop is fact-checked like any other on-screen claim; the credit line names the photo source.

## Code
`scripts/neon.py` (PIL + numpy, 1080x1920) has every piece: `bg`, `glow_line`, `glow_rect`, `duotone`, `framed_media`, `stop`, `timeline_scene` (camera pan between stops), `chart_scene` (line draws in), `caption`.
```python
import sys; sys.path.insert(0, '.claude/skills/bloomberg-style/scripts'); import neon as N
N.FONT_DIR = '<scratchpad>/fonts/inter/package/files'      # npm pack @fontsource/inter
stops = [dict(day='12', month='November', lines=['Huang quits.', 'Nvidia falls 23%.'], media=Image.open(p), credit='Nvidia'), ...]
frame = N.timeline_scene(t_since_this_stop, stops, active=i)
```
Demo sheet: `python3 scripts/neon.py FONT_DIR PHOTO.jpg out.png`.
Drop frames into the edit-video render loop the same way as any other cutaway (a function of seconds-since-start).

## Don't
- Don't copy Bloomberg's logo, name, or lower-third branding; this is the style, not their identity.
- No white cards, no lime highlight boxes, no serif/script fonts in this look.
- Don't put her face inside a neon frame or cover it.
