# Working with Elena

Elena makes short vertical tech and news videos for Instagram, plus news carousels.
Claude helps with research and scripts, video edits, carousels, and breakdowns of other creators' videos.

| File | What's in it |
|---|---|
| `context/video-rules.md` | Every editing rule and style note she has given, plus what worked |
| `context/learnings.md` | What we learned from other creators' videos, and video types to try. Add to it after every breakdown |
| `.claude/skills/edit-video/` | The step-by-step reel edit process, helper scripts, and the code from approved edits |
| `.claude/skills/bloomberg-style/` | Her favorite look (Bloomberg Business timeline reel): spec + `neon.py` building blocks |

## How we work
1. Plan, then storyboard, then render. Wait for her OK at each step.
2. Fact-check anything on screen; ask for the source of headlines you can't find.
3. Feed every lasting note back into `context/video-rules.md` in the same turn.
4. Short replies: show the image or file, say what changed and what's open.

## Writing
- Avoid the word "real" and AI-sounding phrasing; never "It's not X, it's Y".
- Scripts read like a movie with characters and tension; no "for you" advice endings.
- Script sentences: short, simple, declarative, slightly provocative. One idea per sentence. This does better on Instagram.

## Push back
Before scripting, check the idea against **Red flags** in `context/learnings.md` (from the Black Friday post-mortem). If it hits two or more, say so plainly and suggest a sharper angle before writing. Don't keep adding facts in revisions; cut a beat for each one added.

## Repo
- Branch `claude/newsjack-install-monitoring-s7dylc`. No PRs. Big media stays out of git.
- Never print API keys.
