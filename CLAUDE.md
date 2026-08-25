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

> **2026-08-25 — this was violated and it was the cause of the flight stutter.**
> All seventeen scene clips shipped with **exactly one keyframe**, so every seek
> replayed the clip from frame 0. Measured seek latency was 63–65 ms median and
> up to 119 ms on `s04`/`s07` (217 and 241 frames) — 4–7 dropped frames on every
> scroll tick. Only `hero-video.mp4` had ever been re-encoded (16 keyframes),
> which is why the hero scrubbed fine and the scenes did not. Re-encoding all 17
> at `-g 8` took the median to **5–8 ms** (max 13 ms, inside a 60 fps frame
> budget) and cut the payload **112.5 MB → 65.7 MB**. Originals are parked in
> `assets/orig-singlekey/`. **Probe before wiring in any new clip:**
> `ffprobe -v error -select_streams v:0 -skip_frame nokey -show_entries frame=pts_time -of csv=p=0 CLIP.mp4 | wc -l`
> — one keyframe means it is not ready to scrub.

**Video scrubbing requirements (both mandatory or it lags/freezes):**
1. **HTTP Range support** — the browser must be able to `seek` the video. `serve.py`
   returns `206 Partial Content`. The stock `python -m http.server` does NOT → the engine
   falls back to downloading whole clips as blobs → **stutter/freeze** (this was a real bug).
2. **Short GOP** — scene clips must be encoded with a **keyframe every ~8 frames**
   (`-g 8 -keyint_min 8 -sc_threshold 0`). A clip with a single keyframe replays from frame
   0 on every seek → **stutter** (this was the "after scene 11 it lags" bug and the blurry/
   frozen hero). Re‑encode any new scene/hero clip this way before wiring it in.

**Seam behaviour (2026-08-25).** Beats crossfade directly — there are no
connector clips, so a "scene change" is a cross-dissolve between two unrelated
shots and the crossfade does all the work. Three things were making that read as
a flicker, all now fixed in the inlined engine:

- **The incoming clip got only 2vh of lead** (`activeNow = q >= from - 2`).
  `seekClip()` bails while `readyState < 1`, so a clip that had not finished
  opening skipped its only seek and faded in *unpainted*. Lead is now
  `seamVh * 2`; verified the incoming clip sits at `readyState 4`, `t=0` a full
  ~38vh before its crossfade starts.
- **`.wh-scene` had `background:#0b0f0c`.** With `object-fit:cover` that colour
  is only ever visible when the clip has not painted — where it flashed
  near-black through the rising crossfade. Now transparent, so an unpainted clip
  reveals the beat below and a slow decode degrades to "holds the previous frame
  a moment" instead of a black strobe.
- **The keep-window was `cur-1 .. cur+2`.** `release()` blanks an element, so a
  clip torn down two beats back reloaded from scratch — showing nothing — when
  the visitor scrolled back up. Now `cur-2 .. cur+2`.

**Scrubbing back and forth** had two more causes, both of which got *worse* the
more the visitor scrubbed:

- **`release()` blanked the element.** It did `src = …; load()`, and `load()`
  discards the decoded frame immediately, so a released clip was blank until it
  re-opened. Its comment justified that by memory — but that only applies to the
  **blob path**, where the engine holds every byte itself. On a host that answers
  range requests (S3 and serve.py both do) `native` is true, `blobUrl` is null,
  and the teardown frees nothing while guaranteeing a blank frame on the way
  back. Now: blob clips are released, native ones are left for the browser to
  manage. **If you ever move to a host without range support, this matters** —
  the blob path is still fully torn down.
- **`verify()` concluded from a single look.** `nativelySeekable()` wants the
  seekable range to span the whole clip, so a clip that is merely still
  buffering reports short and got misdiagnosed as "host has no range support" →
  `blobFetch()` → `src` swap → blank mid-flight. Every release/ensure cycle
  re-armed that 1.6s timer, so scrubbing made it more likely, not less. It now
  re-checks up to 8 times and **never swaps a clip that is on screen**
  (`onScreen()`, fed by `lastFades`).

Verified by hammering 40 reversals across the same seams: every clip stayed at
`readyState 4` with real painted content (canvas luminance range 1–255),
including the one mid-crossfade — no blanking, no blob swap, no teardown.

**The bloom at seam 1 is deliberate, not a bug.** Measured frame luminance:
hero's last frame `YAVG 216`, s01's first frame `98` — a 118-point cliff. The
0.92 white bloom masks it; every other seam steps ≤32 and gets only the 0.08
whisper. Don't "fix" it without re-measuring — removing it exposes a hard
bright-to-dark cut.

**Flight pacing** (mount weights, tuned for smooth/slow feel):
```js
window.mountScrollWorld(hero, {
  weights: { vhPerSec: 20, minBeat: 130, seam: 24, ease: 0.062 },
  onDarkChange: (dark) => { /* nav goes dark glass while flight is full‑bleed */ },
});
```
Higher `minBeat`/`vhPerSec` = slower per‑scene; lower `ease` = smoother glide.

**Mobile encodes.** Each scene now ships a `sNN-m.mp4` sibling — 1280-wide,
`-g 4`, crf 23, ~29 MB for the set — wired via `data-src-mobile`, which the
engine swaps in on phones (`makeBeat`). A phone decoder's seek cost scales with
both pixel count and GOP length, so the mobile encode tightens both. The boot
loader (§10) prefers the same file, or it would warm the 1080p master the engine
is about to discard. The hero clip deliberately has no `-m` variant.

**The hosted build is a separate upload.** `wisehealth-updated.html` points at
S3, so re-encoding locally fixes `index.html` only — `assets/s3-reupload.tsv`
maps each local file to the S3 key to overwrite in place (same keys, so the HTML
needs no edit). Those objects also send **no `Cache-Control`**, so the browser
only caches them heuristically and the loader re-downloads the flight far more
often than it should; the manifest includes the header to set.

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
**On phones the section re-orders and shows one step at a time.** `.appt-left`
becomes `display:contents` so its two blocks become grid items alongside the
phone, which is then ordered between them: **copy → phone → arrows + step**. The
four steps are stacked into a single grid cell (`grid-area:1/1`) rather than
hidden with `display:none`, so the block keeps the height of the tallest step and
the copy cross-fades in place instead of the section jumping every time the video
advances. The active one is selected with `[data-active="1"]` — matched
positively, because before `mountAppointment()` runs steps 2–4 carry no attribute
at all. Desktop is untouched: four steps spread horizontally with the green
progress line. Note the phone-only view drops the at-a-glance sense of *how many*
steps there are — `.appt-track`/`.appt-fill` stay hidden on mobile because the JS
positions them in pixels measured from the spread-out dots, which collapse to one
point once the steps are stacked.

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

## 10. Boot loader (`#wh-loader`)

Injected in `<head>` of both HTML files as one block: `<style id="wh-loader-css">`
plus `<script id="wh-loader-js">`. It holds a white gate over the page while the
flight footage is pulled into the browser's HTTP cache, showing **real byte
progress**, then fades out and hands over a page whose every seek is a cache hit.
It warms the cache and keeps nothing — the `<video>` elements still stream and
seek natively, so memory is unchanged; only the wait moves to the front.

- **Panel is attached to `<html>`, not `<body>`.** dc re-renders `<body>` into
  its own React tree, so anything parked there is cloned and the script is left
  holding a node that is no longer on screen. This bit is not optional.
- **What it fetches:** the hero clip, `s01..s17`, and the lazy-loaded laptop SVG
  — ~129 MB. Posters, marquee logos and the booking clips are deliberately
  excluded: their own elements request them the moment the page renders, and a
  second request from the loader only races the element's.
- **No `crossorigin` on the media elements.** Chrome fetches a `<video>`'s poster
  as a CORS request but sends no `Origin` header, and S3 only emits
  `Access-Control-Allow-Origin` when one is present — so the attribute silently
  breaks every poster on the page. Don't add it back.
- **`CFG` at the top of the script is the knob.** `gate:'all'` (current) shows
  nothing until every clip is cached; `gate:'lite'` gates on the hero plus
  `liteScenes` scenes and warms the rest behind the revealed page. `maxWait`,
  `stallAfter`, `skipAfter`, `concurrency` are the rest.
- **Automatic degradation:** `prefers-reduced-motion` (the flight engine never
  requests a clip in that mode) and `saveData`/2G both drop to the light gate.
  A **skip** control fades in after 8s; a stall watchdog and a hard `maxWait`
  ceiling lift the gate regardless.
- **Readout is driven by rAF *and* a 200 ms interval** — a tab opened in the
  background parks rAF entirely, and the bar must be current when the visitor
  switches to it. The bar is held off 100% until the gate actually lifts.
- Design: `WISEHEALTH` wordmark, mono eyebrow with pulsing green dot, 2px
  `--line` track with `--accent` fill, mono percentage. Same tokens and easing
  as the rest of the site. **No megabyte counter** — a number most visitors
  cannot judge ("is 129 MB a lot?") is worse than no number, and the bar already
  carries honest progress.
- **The line under the bar advances with the percentage.** `PHASES` maps a
  threshold to a phrase — 0 "Loading the patient journey in high definition",
  30 "Bringing the scenes together", 62 "Almost there", 86 "Just a moment more",
  99 "Ready to launch". `sayPhase()` only fires on a change and swaps the text
  at the bottom of a short fade, so the line changes rather than morphs;
  reduced motion sets it directly. `.whl-note` reserves two lines
  (`min-height:3.2em`) — the phrases differ in length and the panel twitches on
  every swap without it.
- **The real fix is smaller files.** 129 MB of footage is the underlying problem;
  the loader only makes the wait honest. Re-encoding the scenes (and exporting
  the 13 MB laptop SVG as WebP) shortens it directly.

---

## 11. Mobile adaptation

A single block appended to the end of the `<helmet>` stylesheet owns the phone
layout, plus a nav sheet after `</header>` and `mountNav()` in the Component.

- **The bar.** `.wh-navleft` becomes `display:contents` below 760px, so brand,
  nav and the menu button become siblings of the bar and can be re-ordered:
  wordmark left, compact CTA and menu button right. The header's inline
  `gap:24px` and the CTA's inline padding both need `!important` to override —
  this page styles inline almost everywhere, which is why the older media
  queries are full of it too.
- **`.wh-menubtn` is a real button now.** It used to be a `<div>` with no
  handler; below 1100px the inline links are hidden, so it was the only
  navigation on a phone and it did nothing. It toggles `html.wh-navopen`, which
  drives `#whNav` (the sheet) and `[data-menuclose]` (the scrim). The sheet sits
  at `z-index:99` under the bar's `100` on purpose, so it reads as coming out
  from under the bar and leaves the same way.
  **It is `display:none` above 1100px** — that is exactly where the bar already
  shows Booking / Omnichannel / Integrations, so a second way in beside the
  wordmark is clutter. The sheet and scrim are hidden there too.
- **The flight goes edge to edge on phones**, at every point in the run. Two
  separate things were keeping it off the screen edge, and both had to go:
  `#hero` is a `<section>`, so the blanket `section{padding:0 22px !important}`
  rule caught it and shrank `.wh-stage` to 331px — and since the frame's
  full-bleed width is `100%` *of the stage*, the flight could never reach the
  edge no matter how far it opened. Separately, scroll-world already ships
  `.wh-flight{--wh-card-w:100%}` in its own `max-width:860px` block, but that is
  specificity (0,1,0) and this page's
  `html:not([data-wh-reduced]) #hero{--wh-card-w:min(1160px,95vw)}` is (1,1,1),
  so **the engine's mobile rule had never once applied**. Overriding it needs a
  selector of at least that shape — `#hero.wh-flight` alone is (1,1,0) and loses.
  Corner radius goes to 0 there too. Desktop keeps the 1160px card and its 30px
  radius. The `.wh-beats` overlay carries its own 22px padding, so dropping the
  section padding does not strand the captions against the edge.
- **Phone hero chrome differs from desktop.** The caption block is pinned to the
  **bottom-left** (`padding-bottom:22px + safe-area`, plus `align-items:end` —
  `.wh-beats` is a grid and every caption shares one cell, so without it the
  shorter ones stretch and float with dead space beneath). The chapter rail
  becomes **one tag in the top-left** instead of a five-dot column on the right
  edge: siblings are hidden and only `[data-active="1"]` shows, as a dark
  translucent pill with the green dot leading (`row-reverse`). Nothing new
  drives it — `railItems` in `render()` already flips `data-active` on every
  beat change, so the tag re-labels itself through The call → The booking →
  Arrival → Consultation → After. The label needs `display` restored because the
  engine's own mobile block hides it; an id selector outranks that.
- **Beat 0 gets `object-fit:cover` on phones.** The hero clip is the only beat
  set to `contain`: it is shot on white, so on a wide desktop card the letterbox
  is invisible against the page. In a portrait frame it is not — the clip is
  2400x1602, so a 375x812 full-bleed card paints 375x250 of video and 281px of
  white above and below it. Phones get `cover`, which is what all seventeen
  scenes already do, and `--wh-focus` is honoured so the hero clip can be
  re-framed with `data-focus-mobile` exactly like a scene. The rule is written
  as `#hero .wh-video` because the engine injects its own stylesheet *after*
  the helmet, and id specificity is what outranks it. Desktop keeps `contain`.
- **There is no `box-sizing:border-box` reset on this page.** A bare
  `min-height` stacks on top of padding instead of containing it — that is how
  the header CTA reached 62px. Every component sized here declares
  `box-sizing:border-box` itself; do the same rather than adding a global reset,
  which would move every inline-styled box on the site.
- **Touch targets are 44px**, and the `(pointer:coarse)` query keeps that floor
  off the desktop bar, where it would only add 24px of height for nothing.
- **Type is re-led per size, not scaled by one ratio.** `line-height:.98` and
  `letter-spacing:-.035em` are right for a 76px display line and cramped at
  38px wrapped over three lines, so phones get `1.05` / `-.028em`.
- **The request-a-demo popup** (`#whDemo`) runs on **two clocks**, because the
  two kinds of trigger mean different things. The *browsing* trigger (reaching
  the footer) is a "you have been here a while" prompt and waits a full **60s**
  (`mountDemo`, was 3s for everything). **Exit intent is exempt** — it is a last
  chance, and gating it to 60s would mean the visitors who leave at 0:40 are
  never asked at all; it keeps only a 5s floor so an instant bounce does not get
  a popup. `showOnce(leaving)` carries that distinction; only the `mouseout`
  handler passes `true`. Exit intent is desktop-only by design — it is attached
  inside the `(hover:hover) and (pointer:fine)` branch, since touch has no
  hover — so testing it in an emulated-touch viewport will always look broken. It is `840px` wide (was 920)
  and on phones it is a **centred popup, not a bottom sheet**: an equal margin on
  every side, all four corners rounded, inheriting the dialog's own scale-and-lift
  entrance instead of the sheet slide. Two things that bite when resizing it: the
  close button is absolutely positioned in the form panel's top-right, so the
  header needs `padding-right` or the intro line runs under the X; and
  `.wh-demo-aside .lede` is `display:none` on phones, which leaves the headline
  touching the checklist unless `.wh-demo-points` carries its own `margin-top`.
- **On phones the CARD is the scroller, not the form panel.** `.wh-demo-dialog`
  is `overflow:hidden` and `.wh-demo-form`'s `overflow-y:auto` never engages,
  because its grid row is auto-sized — the row grows to fit the fields, so the
  panel is never shorter than its content and has nothing to scroll against.
  That clipped 1120px of form inside a 766px card and left the submit button
  ~230px below the bottom edge, **unreachable**: nobody could submit on a phone.
  Below 720px the dialog takes `overflow-y:auto` (with `overscroll-behavior:
  contain`), `.wh-demo-grid` drops its `max-height` and the form panel goes back
  to `overflow:visible`. Scrolling the whole card also lets the dark intro panel
  move out of the way instead of holding 29% of the screen. The close button
  becomes `position:sticky` + `float:right` so it stays in the card's top-right
  the whole way down, and carries its own translucent background — content
  scrolls under it, and a bare ring over a text field reads as a glitch.
  **If you ever change the fields, re-check this**: it is the kind of break that
  looks fine until the form is one row taller than the screen.
- **Form fields are 16px below 860px.** Anything smaller makes iOS Safari zoom
  the page on focus and strand the visitor scrolled sideways.
- **The loader takes the light gate on phones** — same
  `(max-width:860px),(pointer:coarse)` query the flight engine uses. 130 MB of
  footage is not something to spend on a mobile connection; see §10.
- Verifying on mobile: this preview pane reports `visibilityState: hidden`, so
  rAF and CSS transitions are parked and screenshots paint stale. Measure with
  `getBoundingClientRect`/`getComputedStyle` instead, and inject
  `*{transition:none!important;animation:none!important}` before screenshotting
  an animated state. When forcing `[data-reveal]` visible, also clear
  `[data-reveal] > *` — the `mask` headlines translate an inner span, and
  leaving it set makes headings look missing.

**Known, not fixed** (content decisions, not layout): the footer links point at
`#platform`, `#journey`, `#analytics`, `#usecases` and `#resources`, none of
which exist on the page any more, and the omnichannel headline reads
"Everychannel." with no space. The `@media` rules for those removed sections are
still in the stylesheet.

---

## 12. Lead capture (demo form → Wisemelon trigger)

`#whDemoForm` POSTs to the Wisemelon trigger endpoint on submit. The whole
integration is the `LEAD_API` block plus the `fetch` in the form's submit
handler — one place to edit.

- **Endpoint:** `POST https://api.wisemelon.ai/api/trigger/invoke/6a8de7e8aae0423a74f13a70`
  with `x-api-key` / `x-api-secret` headers.
- **Body:** the whole form (`name`, `email`, `organization`, `role`, `phone`,
  `size`, `message`). Their example only showed `phone`; the rest is sent
  alongside so the lead data is not thrown away — **verify their trigger
  ignores unknown keys**, and trim the body to `{phone}` if it does not.
- **`phone` is normalised to bare digits with a country code** (`normPhone`) —
  `+91 98765 43210`, `09876543210` and `9876543210` all become `919876543210`,
  matching the format in their example. It is now a **required** field, because
  the trigger is a WhatsApp send and there is nothing to fire without it.
- **Failure is never faked.** The handler used to show the success panel after
  an 850ms timer with a `TODO` where the request should be. A non-2xx or a
  network error now re-enables the button, keeps what the visitor typed, and
  shows `.wh-demo-err`; only a real 2xx shows the success panel.

> **The key and secret are public.** They ship inside `index.html`, this repo is
> public, and GitHub Pages serves it — so anyone can read them in view-source
> and invoke the trigger themselves. No amount of client-side work changes that:
> a browser cannot hold a secret. The fix is a proxy that keeps the secret
> server-side (a Cloudflare Worker or Vercel/Netlify function; Pages itself is
> static-only) with the page posting to the proxy instead. **Rotate this pair
> once that is in place.** Until then, treat the endpoint as open to the world
> and make sure it is rate-limited on the server.

---

## 13. Editing rules / preferences

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
