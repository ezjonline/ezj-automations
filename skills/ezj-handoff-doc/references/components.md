# Components

Every class below is already styled in `template/handoff.html`. Copy the snippet, change the words. Do not add CSS.

Motion is automatic: sections fade up on scroll, `data-count` numbers count up, bars grow. It all switches off for people who turn off motion, and the page reads fine with no JavaScript.

## Page skeleton

```html
<section class="sys" id="how"><div class="wrap">
  <div class="syshead">
    <div class="row"><span class="eyebrow">How it works</span><span class="pill ok">Working now</span></div>
    <h2>The outcome in plain words</h2>
    <p>One or two sentences.</p>
  </div>
  <!-- components -->
</div></section>
```

## Hero

The byline holds the logo line (never edit it), who it is for, the date, and who built it. Link buttons: Loom first with `btn main`, then PR, then the live link. Three tiles, one per main part, each with a status pill.

```html
<div class="links">
  <a class="btn main" href="https://www.loom.com/share/...">🎥 Watch the Loom <small>4:12</small></a>
  <a class="btn" href="https://github.com/.../pull/7">🔀 Pull request #7</a>
  <a class="btn" href="https://...">🌐 Try it live</a>
</div>
<div class="tiles">
  <a class="tile" href="#how"><span class="n">01</span><h3>Part name</h3><p>What it does in one line.</p><span class="pill ok">Working now</span></a>
</div>
<p class="together"><b>01 and 02 are one flow.</b> 03 runs on its own.</p>
```

Only two parts? Use two tiles. Only one? Drop the tiles and keep the buttons. No live link? Drop that button. Do not know the Loom length? Leave out the `<small>`.

`p.together` is a small grey caption. Use it under any component that needs one line of explanation, not only the hero.

## Diagrams (How it works needs at least one)

**rail**: the whole thing in one line, 3 to 6 steps. The last or most important step gets `hot`.

```html
<div class="rail"><span class="s">Form submitted</span><i>→</i><span class="s">Checked</span><i>→</i><span class="s hot">Card posted in Slack</span></div>
```

**routes**: where it branches, 2 or 3 outcomes. The main path gets `route main`.

```html
<div class="routes">
  <div class="route main">
    <div class="chips"><span>Matched client</span></div>
    <div class="to">Two buttons</div>
    <div class="where">Build the brief, or read the answers</div>
    <div class="foot">Most common: <b>9 in 10</b></div>
  </div>
</div>
```

**lanes**: timed sequences (follow ups, reminders, retries). The real messages hide behind the toggle.

```html
<div class="lanes">
  <div class="lane">
    <div class="who"><span class="t">Booked a call</span><span class="d">Needs to show up</span></div>
    <div class="track"><span class="touch"><span class="ic">💬</span>right away</span><span class="arrow">→</span><span class="touch"><span class="ic alt">✉</span>day before</span></div>
    <div class="ends">Stops when they cancel</div>
    <details><summary>See the messages</summary><div class="msgs">
      <div class="msg"><span class="when">Right away</span><div class="bubble">you're booked for thursday 3pm.</div></div>
    </div></details>
  </div>
</div>
```

**pipe**: stages something moves through, with what moves by itself versus by hand.

```html
<div class="pipe">
  <span class="lbl">The pipeline moves itself</span>
  <span class="stage auto">Applied</span><span class="arrow">→</span><span class="stage auto">Booked</span><span class="arrow">→</span><span class="stage manual">Won or Lost</span>
  <div class="key"><span>Moves automatically</span><span class="m">One click from a person</span></div>
</div>
```

**feature + phone**: a highlighted explainer beside what a person actually sees. Bubbles: `them` (the person, blue), `bot` (the system), `alert` (a notification to the team, with a bold label).

One way flows are fine: use only `bot` and `alert` bubbles when nobody replies.

```html
<div class="feature">
  <div>
    <span class="eyebrow">What the client sees</span>
    <h3>Short outcome headline</h3>
    <ul><li><span><b>Bold lead.</b> Plain explanation.</span></li></ul>
  </div>
  <div class="phone">
    <div class="top">Slack, #onboarding</div>
    <div class="b bot">New intake: Test Client</div>
    <div class="b them">clicked Build Development Brief</div>
    <div class="b alert"><b>QUEUED</b>Job 4821 started.</div>
  </div>
</div>
```

## See it work

**trysteps**: numbered steps anyone can follow with test data, each with what they should see.

```html
<div class="trysteps">
  <div class="trystep"><b>Open the test form and submit it</b><span class="see">a new card in #test within 10 seconds.</span></div>
</div>
```

**bigstat + bars**: real results only. Bar width `--w` is the real percentage. `data-count` makes the big number count up; keep the final number as the text too.

```html
<div class="statgrid">
  <div class="bigstat"><span class="big" data-count="12">12</span><p><b>of 12 tests pass</b></p><p class="note">Run with <code>npm test</code> on 17 Sept 2026.</p></div>
  <div class="bars">
    <div class="bar"><span>Buttons</span><span class="track2"><i style="--w:100%"></i></span><span class="v">5 / 5</span></div>
    <div class="bar"><span>Errors</span><span class="track2"><i style="--w:75%"></i></span><span class="v">3 / 4</span></div>
  </div>
</div>
```

**minibars**: a tiny column chart for 3 to 6 values (batch sizes, daily counts). Heights are real proportions.

```html
<div class="minibars"><span style="height:25%">500</span><span style="height:50%">1,000</span><span style="height:100%">2,000</span></div>
```

## Set it up

**setup**: numbered steps. Commands go in a `cmd` block with a copy button. Click paths in plain text with → between clicks.

```html
<div class="setup">
  <div class="su"><b>Make your settings file</b><p>Then fill in the table below.</p><div class="cmd"><code>cp .env.example .env</code><button class="cp" type="button">Copy</button></div></div>
</div>
```

**settings table**: every setting, what it is, where to get it, needed or not. Names only, never values.

```html
<div class="tablewrap"><table class="env">
  <thead><tr><th>Setting</th><th>What it is</th><th>Where to get it</th><th>Needed?</th></tr></thead>
  <tbody>
    <tr><td><code>BRIEF_PIPELINE_URL</code></td><td>Where the button sends the job</td><td>Ethan sends it privately</td><td><span class="req">Yes</span></td></tr>
    <tr><td><code>LOG_LEVEL</code></td><td>How much it writes to the logs</td><td>You choose</td><td><span class="req no">No, defaults to info</span></td></tr>
  </tbody>
</table></div>
```

**cards**: three small explainers, usually what you can change without code.

```html
<div class="cards"><div class="card"><span class="k">Change the wording</span><p>Edit <code>messages.json</code>, redeploy.</p></div></div>
```

## What breaks it

```html
<div class="breaks">
  <div class="brk"><div><span class="l">You notice</span><span class="sym">The button says access denied</span></div><div><span class="l">Why</span><span class="why">The secret in Vercel does not match the pipeline.</span></div><div><span class="l">Fix</span><span class="fix">Copy the secret again into Vercel settings and redeploy.</span></div></div>
</div>
```

## Status

```html
<div class="board">
  <div class="srow"><span class="what">Part name<small>How it was tested, or what is left</small></span><span class="pill ok">Working now</span></div>
</div>
```

Pills: `ok` Working now, `go` Needs your go, `you` Waiting on you, `off` Not built, `bad` Broken or Not fixed yet. Meanings in `writing.md`.

## What I need from you

```html
<div class="asks">
  <div class="ask"><b>Add me to the Vercel project</b><ol><li>vercel.com → the project → Settings → Members</li><li>Invite dev@example.com as Member</li></ol></div>
</div>
```

## Loom embed (optional)

The Loom button in the hero is required. If the video matters to a section, you may also embed it:

```html
<div style="position:relative;padding-bottom:56.25%;height:0;border-radius:18px;overflow:hidden;border:1px solid var(--line)"><iframe src="https://www.loom.com/embed/<id>" style="position:absolute;inset:0;width:100%;height:100%;border:0" allowfullscreen></iframe></div>
```
