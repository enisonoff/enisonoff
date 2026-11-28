"""Beat list of the approved outage reel (v6). Times are on its v2 cut; REEL_TMAP mapped them to the final cut.
Copy this file per video and rewrite the beats. Every helper used here lives in scripts/reel_style.py."""
H1 = [  # (cut time it lands, outlet, date, headline, highlighted words)  -- all checked against the published stories
    (12.52, 'BleepingComputer', 'Nov 12', 'Massive Microsoft 365 outage disrupts Outlook, Teams, Copilot worldwide', 'outage disrupts'),
    (13.38, 'PBS News', 'Nov 13', 'FAA grounds all flights at U.S. airports due to air traffic control communications problems', 'grounds all flights'),
    (14.08, 'AP', 'Nov 16', 'A technical issue at JPMorgan Chase triggers online banking delays across major US banks', 'technical issue'),
    (14.28, 'CBS News', 'Nov 17', "NSA's classified internal network goes down, sources say", 'goes down'),
]

def lock_list(t, t_fill, t_stamp):
    im = Image.new('RGBA', (W, 960), (0, 0, 0, 0)); paper = Image.new('RGBA', (760, 780), (246, 243, 236, 255)); d = ImageDraw.Draw(paper)
    d.text((40, 34), 'BROKEN LOCKS', font=ANTON(56), fill=(15, 15, 15)); d.text((44, 120), 'united states · found overnight', font=SUB(26), fill=(110, 110, 110))
    rows = ['front door, 14 elm st', 'back gate, 220 oak ave', 'garage, 9 harbor rd', 'side door, 31 pine st', 'window, 77 lake dr', 'basement, 5 mill ln', 'front door, 402 main st', 'shed, 18 birch ct']
    n = int(min(max((t - t_fill) / 1.4, 0), 1) * len(rows) + (1 if t >= t_fill else 0))
    for i, r in enumerate(rows[:n]):
        yy = 180 + i * 62; d.text((44, yy), r, font=HEAD(34), fill=(20, 20, 20)); d.text((640, yy), 'open', font=SUB(28), fill=RED)
    p = paper.rotate(-1.5, resample=Image.BICUBIC, expand=True); im.alpha_composite(p, ((W - p.width) // 2, 70))
    if t >= t_stamp:
        k = min((t - t_stamp) / 0.13, 1); st = Image.new('RGBA', (560, 170), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rectangle([6, 6, 554, 164], outline=RED + (255,), width=10); sf_ = ANTON(108); bb_ = sd.textbbox((0, 0), 'PUBLIC', font=sf_); sd.text((280 - (bb_[0] + bb_[2]) / 2, 85 - (bb_[1] + bb_[3]) / 2), 'PUBLIC', font=sf_, fill=RED + (255,))
        st = st.rotate(12, resample=Image.BICUBIC, expand=True); sc = 1.4 - 0.4 * k; st = st.resize((int(st.width * sc), int(st.height * sc)))
        im.alpha_composite(st, ((W - st.width) // 2, 480 - st.height // 2))
    return im

behind(1.80, 4.90, 1.88, 'taken down by its own', 3.44, 'software update', RED, 200, brk=4.38)
card(6.00, 8.00, [Item(6.04, 'the fixes are', SF(80), WHITE, 640), Item(6.84, 'breaking', fit(ANTON, 'breaking', 960, 300), RED, 720), Item(7.34, 'everything', fit(ANTON, 'everything', 960, 300), WHITE, 1020)])
card(12.45, 14.88, [Item(12.45, 'this month', SF(72), WHITE, 120, 90)] + [Clip(t, clipping(o, d_, h, k, 860, 44), 540 + (-30, 25, -20, 20)[i], 420 + i * 300, (-2.5, 1.8, -1.2, 2.2)[i]) for i, (t, o, d_, h, k) in enumerate(H1)])
card(14.88, 18.40, [Item(14.95, 'just today', SF(80), WHITE, 520), Clip(15.50, clipping('Reuters', 'Nov 27', 'Hackers breach US Air Force flagship Cloud One computing platform', 'hackers breach', 960, 62), 540, 900, -1.5)])
broll(43.40, 45.75, '03')
broll(143.80, 148.60, '12')

behind(24.42, 26.95, 24.46, 'experts from', 24.98, 'all sides', WHITE, 0, auto=True)
broll(50.50, 52.25, '04', [Item(50.54, 'basically', SF(80), WHITE, 560), Item(50.84, 'pennywise', fit(ANTON, 'pennywise', 960, 300), RED, 640), Item(51.36, 'in the sewers', SF(80), WHITE, 1010)])
behind(60.80, 66.20, 61.66, 'not attacks.', 64.66, 'upgrades', WHITE, 0, auto=True)
import sign as _sign
_FENCE = _sign.fence_scene()
def _fence(t, a, b, h):
    k = (t - a) / max(b - a, 0.1); s_ = 1 + 0.06 * k; z = _FENCE.resize((int(W * s_), int(H * s_)), Image.BILINEAR); x0 = (z.width - W) // 2; y0 = (z.height - h) // 2
    return z.crop((x0, y0, x0 + W, y0 + h))
broll(75.15, 79.05, _fence)
over(89.80, 94.70, [Clip(89.94, clipping('OpenAI', 'Sep 1', '"We now believe Astra meets the Critical cybersecurity capability threshold."', 'critical cybersecurity capability threshold', 900, 46), 540, 1020, -1.5), Clip(91.40, clipping('Axios', 'Sep 1', "OpenAI to limit access to Astra's most powerful cyber tools", 'limit access', 860, 40), 560, 1210, 1.8)])
SCENES.append((110.40, 112.20, 'behind', [Flag(110.70, 'us', 215, 600), Flag(111.32, 'cn', 880, 600)], []))
split(116.40, 122.90, [], panel=lambda t: lock_list(t, 118.18, 121.08))
_hf = None
split(132.60, 140.70, bg='11', items=[Counter(134.42, 948, 139.28, 61, ANTON(400), 40), Item(134.96, 'holes found', SF(72), WHITE, 720, 110, brk=139.70), Item(139.78, 'fixed', SF(72), RED, 720)])
broll(157.70, 161.70, '13', [Clip(158.70, clipping('Axios', 'Nov 17', 'Why the internet suddenly broke all at once', 'broke all at once', 900, 54), 540, 760, -1.5)])
behind(153.40, 155.65, 153.46, 'we have entered the', 154.46, 'dark ages', WHITE, 0, auto=True, t_below=154.94, below='of sorts')
behind(174.20, 177.20, 174.38, 'the preparation', 176.40, '= the problem', RED, 0, auto=True)
