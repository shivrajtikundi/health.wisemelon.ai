# WiseHealth Landing Page — Project Guide (CLAUDE.md)

A single self‑contained marketing site for **WiseHealth** — an AI operating system
for modern hospitals (parent company **Wisemelon**, `wisemelon.ai`). Built on the
**Claude Design ("dc")** framework and served locally with a small Python dev server.

> When editing this project, **match the existing design language exactly** (below).
> Do not redesign sections that weren't asked for. Do not introduce new colours,
> fonts, or generic SaaS components. Use only supplied assets; never fake logos.

---

## 1. Files & structure

```
WiseHealth.dc.html      ← THE site (all markup, CSS, and the dc Component script)
support.js              ← dc framework runtime      (referenced as ./support.js)
scroll-world.js         ← hero scroll‑flight engine  (referenced as ./scroll-world.js)
serve.py                ← range‑capable dev server   (run via .claude/launch.json)
.claude/launch.json     ← dev server config (autoPort, port 4599)
CLAUDE.md               ← this file

assets/
├── scenes/
│   ├── appointment/     ← flight scene videos s01–s17.mp4 + hero-video(.mp4/-m dropped) + poster/
│   │   └── booking/     ← step-1..4.mp4  (portrait 9:16 booking clips for the phone)
│   └── ipd/             ← intentionally EMPTY (IPD scenes go here later)
├── uploads/             ← raw source uploads
│   ├── hero-source.mp4          (raw hero, ~high‑res source)
│   ├── videos/                  (raw booking recordings)
│   ├── hopitals logos/          (8 real hospital logo SVGs — used in the marquee)
│   └── images/Group 1321317620.svg  (laptop mockup used in the omnichannel section, ~13MB)
└── references/          ← design references + the original brief + new‑design reference
```

---

## 2. Brand & design system (SINGLE SOURCE OF TRUTH)

Design tokens live in `:root` inside `WiseHealth.dc.html` and are applied by the dc
Component (`applyAccent`). The current accent is **green**.

| Token | Value | Use |
|-------|-------|-----|
| `--accent` | **`#12A594`** (teal‑green) | brand accent: logo "HEALTH", eyebrow dots/dashes, headline last word, ticks, links, buttons hover |
| `--ink` | `#0B0B0C` | primary text / near‑black |
| `--mut` | `#6E6E76` | muted body / secondary text |
| `--line` | `#E6E6E9` | hairlines, borders, dividers |
| `--paper` | `#FBFBFC` | section background variant |
| `--card` | `#F3F3F5` | cards, quote blocks, hover‑row fill |

- `data-props` accent options include `#12A594` (green, current), `#0B0B0C`, `#2F6BFF`,
  and previously `#7C6BF2` (purple — **replaced by green**, don't reintroduce).
- Light theme only. Dark chrome is used deliberately inside the phone mockup
  (WhatsApp dark header `#1F2C34`).

### Fonts
- **Display + body:** `"Helvetica Neue", Helvetica, Arial, sans-serif`. Headlines are
  **weight 500** (medium, NOT bold), tight tracking.
- **Labels / eyebrows / meta / status:** `ui-monospace, SFMono-Regular, Menlo, monospace`.
- `Gloock` (serif) and `Plus Jakarta Sans` were used in earlier iterations but the
  **current design is Helvetica** — don't mix them back in.

### Typography rules
- **Display headings:** `font-size:clamp(38px,4.6vw,76px)`, `line-height:~1.0`,
  `letter-spacing:-.035em`, `font-weight:500`, sentence case. The **last word/phrase
  is coloured `var(--accent)`** (e.g. "One patient **conversation.**").
- **Eyebrows:** mono, `font-size:11.5px`, `letter-spacing:.22em`, `text-transform:uppercase`,
  `color:var(--accent)`, with a leading green dash (`::before` 26px×2px bar).
- **Body:** `16px`, `line-height:1.65`, `color:#6E6E76`, `text-wrap:pretty`.
- **Pills / tags / badges:** `border-radius:999px`, 1px `--line` border, often mono text,
  with a pulsing green dot (`wh-pulse`).
- **Quote/callout cards:** `background:var(--card)`, `border-radius:20px`, italic.
- Numbers/stats: large light numerals; count‑up on reveal (`data-count`).

---

## 3. Skills in use

- **`impeccable`** — the frontend craft floor: real contrast (no failing greys), genuine
  hover/press/focus feedback, deliberate spacing rhythm, no icon/arrow monotony,
  accessible focus rings, cohesive tokens. Apply this bar to every UI change.
- **`apple-design`** — motion & materials: respond on press (spring scale), interruptible/
  smooth transitions, optical typography (tracking/leading by size), translucency/depth,
  and **always honour `prefers-reduced-motion`**.
- **`scroll-world`** — the hero scroll‑flight engine (`scroll-world.js`, see §5). Scroll
  scrubs a cinematic camera‑flight through video scenes.

Load these skills when doing related work; keep new work consistent with the language
they established here.

---

## 4. Animation language (reuse this — don't invent new patterns)

Driven by the dc Component (`class Component extends DCLogic`) inside the HTML.

- **Reveal on scroll:** `data-reveal="up|mask|scale"` + `data-delay="<ms>"` on elements,
  with inline `opacity:0; transform:…; transition:… cubic-bezier(.22,1,.36,1)` init.
  An IntersectionObserver toggles them (reversible). `mask` = headline lines slide up from
  `overflow:hidden`. Easing everywhere: **`cubic-bezier(.22,1,.36,1)`**.
- **Scroll progress bar** (`[data-progress]`), **sticky nav** that condenses on scroll.
- **Marquee** (`[data-marquee]`, keyframe `wh-marquee`, translate −50%, seamless loop).
- **Count‑up** numbers (`[data-count]` + `data-suffix`), **magnetic buttons** (`[data-magnet]`),
  **tilt/hover‑row** interactions (`[data-hoverrow]`, `[data-arrow]`), **orbit/float/spin/pulse**
  keyframes (`wh-float`, `wh-spin`, `wh-pulse`).
- Reduced motion: global `*{animation:none!important;transition-duration:.01ms!important}`
  plus explicit fallbacks (reveals + custom sections force visible/static).

---

## 5. Hero scroll‑flight (`scroll-world.js`) — CRITICAL RULES

The hero (`#hero.wh-flight`) is a pinned scroll‑scrubbed video flight (~23 viewport
screens). The engine reads DOM nodes by class and writes CSS custom properties on
`<html>` (`--wh-open`, `--wh-intro-o`, `--wh-intro-y`, `--wh-dark`, per‑beat vars) so a
dc re‑render can't clobber the animation. Mounted from the Component via
`window.mountScrollWorld(hero, {...})`.

**Video scrubbing requirements (both mandatory or it lags/freezes):**
1. **HTTP Range support** — the browser must be able to `seek` the video. `serve.py`
   returns `206 Partial Content`. The stock `python -m http.server` does NOT → the engine
   falls back to downloading whole clips as blobs → **stutter/freeze** (this was a real bug).
2. **Short GOP** — scene clips must be encoded with a **keyframe every ~8 frames**
   (`-g 8 -keyint_min 8 -sc_threshold 0`). A clip with a single keyframe replays from frame
   0 on every seek → **stutter** (this was the "after scene 11 it lags" bug and the blurry/
   frozen hero). Re‑encode any new scene/hero clip this way before wiring it in.

**Flight pacing** (mount weights, tuned for smooth/slow feel):
```js
window.mountScrollWorld(hero, {
  weights: { vhPerSec: 20, minBeat: 130, seam: 24, ease: 0.062 },
  onDarkChange: (dark) => { /* nav goes dark glass while flight is full‑bleed */ },
});
```
Higher `minBeat`/`vhPerSec` = slower per‑scene; lower `ease` = smoother glide.

**Hero framing:** the video card sits pushed down (`translateY((1 - var(--wh-open))*23vh)`)
with a **white inner‑glow** (`.wh-innerglow`, `opacity: calc(1 - var(--wh-open))`) that
clears as you scroll; both ease back to full‑bleed centre. Hero uses ONE high‑res clip
(no `-m` mobile variant) so it stays sharp; keep the hero clip **native/2400px‑wide**,
`crf 18`, short GOP.

---

## 6. Page section order

1. **Hero** — scroll‑flight (`#hero.wh-flight`, the cinematic patient journey, ~23 screens)
2. **Marquee** — hospital logo strip (real SVGs from `assets/uploads/hopitals logos/`,
   grayscale, `⊕` green separators, height ~57px, keyframe `wh-marquee`)
3. **Appointment** (`#appointment`) — booking demo (see §7)
4. **Omnichannel** (`#omnichannel`) — animated wheel + laptop (see §8)
5. **Problem** (`#problem`) — sticky headline + numbered hover‑rows
6. **Platform** (`#platform`) — "One system. Every workflow." 3 tilt cards
7. **Analytics** (`#analytics`) — count‑up stats + orbit visual
8. **Use cases** (`#usecases`) — 4 role cards
9. **Resources** (`#resources`) — article hover‑rows
10. **Book / footer** (`#book`) — dark CTA + footer columns

Marquee sits **before** the appointment section. Sections after the flight are normal flow.

---

## 7. Appointment section (booking demo)

Left: eyebrow → "A simpler way to book **care.**" → body → "Built with Wisemelon Webfronts"
pill → prev/next `«  »` arrows → **4‑step stepper** (`STEP 0N` + description, green progress
line that fills continuously with the current video's playback).
Right: **portrait iPhone** mockup (metallic bezel, dynamic island + camera, glass sheen)
with a **dark WhatsApp header** (avatar, "Wise Health" + blue tick, "online", call icons)
and a **dark iPhone bottom bar**. The **video sits between the bars** in a 9:16 `.appt-videoarea`.

- Videos: `assets/scenes/appointment/booking/step-1..4.mp4` — **portrait 1080×1920 (9:16)**.
  Auto‑cycle 1→4 and **loop back to 1**; step‑click and arrows jump; play/pause on scroll
  in/out. Logic is `mountAppointment()` in the Component.
- **To replace the clips:** drop new files with the **same names** (order = step order).
  Keep them 9:16 or they'll cover‑crop. Web‑optimize: `-an -r 30 -crf 22 -pix_fmt yuv420p
  -movflags +faststart` (short GOP not needed here — these play, they aren't scrubbed).

---

## 8. Omnichannel section (animated wheel)

Left: eyebrow → "Everychannel. One patient **conversation.**" → body → channels pill
("WhatsApp · Instagram · Facebook · Website · Google") → quote card.
Right: an **animated radar wheel** behind the laptop mockup.

- Wheel = **5 concentric filled circles** (`.omni-c.c1..c5`), recoloured to brand green
  (greenest in the middle band, outer rings green‑stroked, light centre hub). Big (~82% of
  the visual). It **rotates circularly** via two masked conic‑gradient sweeps (`.omni-spin`,
  `wh-spin`, opposite directions). "WISE**HEALTH**" text hub at centre.
- **Channel logos** (`.omni-logo` WhatsApp/Facebook/Instagram/Chrome, inline SVG in white
  badges) are placed around the **top arc at different radii** (IG far‑left, WA upper‑left,
  FB top, Chrome upper‑right), centred with `translate(-50%,-50%)`. They **scale‑in** when
  the section enters view (`mountOmni()` adds `.is-in` → `omni-pop`) then **float** gently.
- Laptop image: `assets/uploads/images/Group 1321317620.svg` (in front). ⚠️ It's **~13 MB**
  — consider exporting a PNG/WebP for a faster load.

---

## 9. Dev server & workflow

- **Run:** the preview uses `.claude/launch.json` → `sh -c "exec python3 serve.py"`,
  `autoPort:true`, port **4599**. `serve.py` = threaded, **Range‑capable** static server
  with `Cache-Control: no-cache`. Never use `python -m http.server` (no ranges → flight lags).
- **If port 4599 is stuck** (orphaned process): `lsof -tiTCP:4599 -sTCP:LISTEN | xargs kill -9`,
  then start the preview again. `exec` in the launch cmd prevents future orphans.
- **dc framework caches via the browser** — after editing, **hard‑refresh** or append `?v=N`
  to the URL, or the old compiled version renders.
- **ffmpeg** is available; **`drawtext` is NOT** (no freetype) — can't burn text into videos.
- **Screenshotting lower sections is hard:** the pinned ~23‑screen flight desyncs the
  preview's screenshot vs scroll. To verify below‑hero sections: in the page, set the flight
  track `display:none`, force `[data-reveal]` visible, add `.is-in`, then use a tall viewport
  and capture from the top. (Verification trick only — never leave it in the file.)

---

## 10. Editing rules / preferences

- Preserve all dc mechanics exactly: `<x-dc>`, `<helmet>`, `{{ bindings }}`, `<sc-for>`,
  `data-props`, `style-hover`, the inline `data-dc-script` Component.
- Match tokens/typography above. Green accent, Helvetica display (weight 500), mono eyebrows,
  sentence case, rounded pills/cards, `cubic-bezier(.22,1,.36,1)` motion, reduced‑motion safe.
- Only supplied assets; **no fake hospital/brand logos**. Channel icons (WA/FB/IG/Chrome) are
  simplified brand marks used nominatively to show integrations.
- Keep media systems **easy to swap** (stable filenames, documented folders).
- New flight/IPD scene videos → `assets/scenes/ipd/`, encoded **short‑GOP** (see §5) or they
  won't scrub smoothly.
- Don't reintroduce the old purple accent, Gloock/Plus Jakarta fonts, or the pre‑redesign
  green layout — the current design is the source of truth.
