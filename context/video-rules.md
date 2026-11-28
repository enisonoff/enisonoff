# Video rules (everything Elena has asked for, in one place)

Add to this file whenever she gives a note that applies beyond one video.

## Process
- Plan, then storyboard, then render. Never render before she says go; if she says "wait" or "storyboard first", stop.
- Re-storyboard after notes. A low-quality preview before the full render is welcome.
- Check every render for flashes and sync before sending (edit-video skill, `check_render.py`).
- Don't cut her words unless she asks.
- Joins should be snappy: trim dead air and breaths at every cut to ~0.04 s lead / 0.07 s tail (clean-cut `trim_edges`). Cut redundant lines that restate the previous one.
- Cold open: if her best line moves to the top as the hook, don't play it again at the end. End on the line before it.

## Frame and placement
- Safe zone: nothing important above y≈250 or below y≈1560 (of 1920).
- Never cover her face. Graphics go in the wall space above her head or to the side with more room; check which side has more wall in that shot.
- Photos can tuck *just* behind her head for dimension (her hair over the photo edge), not deep behind it.
- Center text on everything (posters, Venn names, chart titles).
- Photos straight, no frames or white outlines. No white cards behind text on her shot.

## Style that worked (Jensen winners & losers, Nov 2026)
- On-camera posters: Instrument Serif italic lead-in + tall Anton caps in blue (#1646FF), tight line spacing, centered, words revealing one at a time with a blur-in (like @nextbysophie and @romina.aminian reels).
- Full-screen cutaways on a light dot-grid "whiteboard" (like @poojaduttttt) for the Venn, charts, headline clippings and timelines. Captions there are black with a lime (#D4F542) highlight; on her shot they're white with one yellow word.
- People as centered face bubbles (whole face, hair to chin), companies as logos, groups as icons (lawyers = scales of justice).
- Charts: one simple XY chart with labeled lines beats bars for comparisons; label dates on records.
- Headline clippings: outlet + date, lime highlight on 1-3 key words, always a sourced headline.
- Humor beats she liked: the clone pile-up, Jensen on a billion-dollar bill, "this is fine" next to Kress, the Truth Social post full screen.

## Style that worked (SpaceX chip loan)
- Full-frame cutaways inspired by Cleo Abrams: a space render the camera races across following a beam of light; a chatbot question that becomes a ball of energy flying to a space data center; a GPU rack that builds until "$44B" pops on top.
- No white cards, no logos-on-cards, no push-in/zoom transitions, no Starship drawing.

## House style (from Dec 2026): Interval news look
- Title: left-aligned white Inter Tight 500, tight tracking, 2 lines + smaller 2-line subtitle. No box, no shadow, no color.
- Captions (outage video on): bottom subtitles in Edits' "Classic" look with kerning -1 and the bounce effect. Stand-in: Inter Tight 700, 64 px, tracking -3%, white with a black stroke, lowercase, up to 3 words per line, each word bounces on as she says it (0.5 -> 1.1 -> 1.0 with a small hop, 0.22 s).
- Graphics = evidence: full-width screenshots of the real source article, phone screen recordings of the real list/page. Ask Elena for screenshots or record them; never mock up an article.
- Filming: darker room, one warm lamp, mic in frame if possible, centered, eye level. Avoid late-night bed shots.
- Her addition: one dry line per beat, max.

- Push-ins: quick 10-15% punch-in cuts on her face for emphasis lines only (thesis, dry beat, proof, button). Never as zoom transitions into graphics.

- Emphasis words are lowercase (never all caps). Approved combo (outage video, Nov 2026): **Anton lowercase** for the big word + a soft rounded secondary line (she likes **Softedge** from Edits; no public file, so we use **Dosis 500** as the stand-in; Great Vibes script was the earlier pick) tucked above-left (white) and optionally below-right (red). Palette red (232,40,44) / white only. Big words sit BEHIND her (rembg mask, MinFilter(7)+blur(3) to kill halos), never over her face. Every line fits 960 px wide; script on footage gets a soft dark shadow.
- Film grade on all her footage: background desaturated 35% and only slightly darkened (12%) via the mask; the grade mask is eroded (MinFilter 15) and blurred wide (30) so no light ring shows on the wall behind her head (she noticed it at 35%), contrast 1.15, teal shadows + warm mids, matte blacks (0.045 + 0.93a), soft highlight glow, vignette, light grain. Code: `film_grade()` in the outage style script.
- Cards: near-black grain background, same Anton + script combo. Split screens: panel on top, her (graded) on the bottom, thin red divider, subtitles just above the divider.
- Text snaps on, each line landing on the word as she says it: 4 frames (0.13 s), scale 0.8 -> 1.06 -> 1.0, 24 px rise, starts ~1.5 frames early. Every line has a soft drop shadow (3,7 px offset, blur 9, 60% black). Kinetic text is 25% bigger than the Nov 27 storyboard, except words behind her head, which stay frame-width (bigger just hid more of the word). Secondary lines on her footage are white, not red (red got lost on her hair).
- Pacing: pauses at cuts 0.08 s (maxgap) and joins trimmed to 0.032 s lead / 0.056 s tail (her note: 20% tighter than 0.10 / 0.04 / 0.07).
- Lists of news events: show the actual headlines as clippings (off-white paper, Libre Baskerville bold, outlet + date in small caps, 1-3 key words on a red bar), one jumping on per item. Every headline must be sourced.
- Grade her footage: darken/desaturate the wall, warm skin, contrast, vignette, grain. Black grain cards for thesis lines and lists.

## Title cards (older)
- Default: zauey style. Big lowercase white sans (Inter 800), 2 lines, small "(in 3 minutes)" under it, low on her chest, no box. She didn't like the neon panel or the copper torn-paper version.

## Brand
- Her logo blue is #1803BB (deep royal blue, white "on/offline" type). Use it for title cards and headline accents so videos read as hers in the grid.

## Sound
- Subtle clicks only, varied, well under her voice. No whooshes. Nothing on cuts back to her.

## Things she didn't like
- Busy edits (too many graphics); graphics that just restate her words, including a full-screen text card of her key line (cut from the AI lenders video).
- Plain sans lead-ins ("not stylish"); outlines on text; serif headlines on the carousel.
- Flashes of her face between two graphics; audio drifting out of sync.
- Moodboard-style extras piled together (torn copper paper, retro TV bezels, fluted glass, stat-row meters): too busy. Keep cutaways to one idea, a soft background, white type.
- "For you" advice endings in scripts.

## Fonts for the next video
Try the CapCut-style trio: Gloock caps + Great Vibes script + DM Mono small line (Google Fonts). Show 2 frames on her footage before using it.

- Words behind her head sit just above the highest point of her head in that beat (auto-placed from the cutout, tucked ~25 px into her hair); she couldn't read "all sides" / "dark ages" when her head covered the middle.
- A push-in must end exactly on a cut. Ending it a few frames after the cut flashes the new shot zoomed in ("weird frame" at "if a hacker is saying that").
- When a line has a B-roll picture, put its words on the picture, not on her and then the picture (pennywise on the sewer drain).
- Numbers that change should move: 948 rolls down to 61 and turns red, rather than two static labels.
- Explanations need a literal visual of the analogy (a list of broken locks with a PUBLIC stamp beat a dark hallway, which she found confusing).
- End beat stays on her face with the final words behind her, not on a black card.
