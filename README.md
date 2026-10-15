# Weekly Planner

A weekly timetable for planning study time around a fixed class schedule. Each block takes up space in proportion to the time it reserves, so you can see at a glance where the week goes.

It is a single HTML file with no build step and no dependencies apart from Google Fonts.

![Weekly Planner screenshot](docs/screenshot.png)

## Features

- **Week grid, 7 AM to 11 PM**, Monday to Sunday, in 12-hour (AM/PM) time. Today's column is tinted and a line marks the current time.
- **Add, edit and delete blocks.** Click any empty slot or free gap to add a block there; click a block to edit it. Each block has a title, label, day(s), start and end time (15-minute steps) and notes.
- **Drag to move and resize.** Drag a block up/down to change its time or sideways to change its day; drag its bottom edge to change its length. Snaps to 15 minutes. On touch screens, press and hold a block briefly before dragging, so normal swipes still scroll.
- **Repeating blocks.** Pick several days in the form to create a repeating block (shown with a ↻ icon). When editing one, choose *All repeats* or *Only this day*. Adding or removing days under *All repeats* adds or removes the copies.
- **Duplicate.** Duplicate a single block to other days, or copy a whole day (click the day name or *Copy day*) to other days, either alongside their existing blocks or replacing them.
- **Clash warnings.** Overlapping blocks get a red outline and a "!" badge. A pill above the grid counts clashes and expands into a clickable list. The edit form also warns if the time you are setting overlaps something (it still lets you save).
- **Free time.** Gaps of 30 minutes or more show as hatched "free · 1h 30m" areas; click one to fill it. A switch turns this off.
- **Labels.** Colour-coded categories (class, study, gym…) that you can add, rename, recolour and delete.
- **Share-of-hours bar.** One pill-shaped bar splits all scheduled hours by label, with a legend and an "All RCVD work" total for labels whose name contains "RCVD".
- **Light and dark themes**, following the system setting.

## Running it

Open `index.html` in any modern browser. That's it.

To host it, enable **GitHub Pages** for this repository (Settings → Pages → Deploy from branch → `main` / root), and it will be served at `https://<user>.github.io/weekly-planner/`.

## Where data is saved

The page picks its storage when it loads:

| Where it runs | Storage | Notes |
|---|---|---|
| Opened as a file or hosted anywhere (GitHub Pages, etc.) | Browser `localStorage`, key `rcvd-planner-v1` | Private to that browser on that device. Clearing site data erases it. A new browser starts with an empty week. |
| Published as a claude.ai artifact with the `db` capability | The artifact's database (`blocks` collection, `settings/labels` document) | Synced across devices; the status pill shows "Synced". |

The status text next to the buttons tells you which one is active ("Saved in this browser only" or "Synced").

### Data model

```js
// a block
{ id, day, start, end, title, label, note, series? }
// day: 0 = Monday … 6 = Sunday
// start/end: "HH:MM" 24-hour strings (display is AM/PM)
// label: id of a label, or "" for none
// series: shared id for blocks created together as repeats

// a label
{ id, name, color }   // color: "#RRGGBB"
```

In local mode everything is stored as `{ blocks: [...], labels: [...] }` under the `rcvd-planner-v1` key. The free-time switch is stored separately under `rcvd-planner-v1-free`.

## Project structure

```
index.html        the whole app: markup, styles and script
docs/screenshot.png
README.md
CLAUDE.md         notes for working on this repo with Claude Code
```

Inside `index.html` the script is organised into sections marked with `// ---` comments: state, persistence, analysis (clashes and free gaps), week grid, drag to move/resize, labels panel, block form, copy-day form, and boot.

## Customising

- **Visible hours:** change `DAY_START` and `DAY_END` (minutes from midnight) at the top of the script.
- **Snap size:** `SNAP` (drag) and the `15` step in the time dropdowns.
- **Minimum free gap shown:** `MIN_GAP` (minutes).
- **Row height:** the `--ppm` CSS variable (pixels per minute).
- **Colours and fonts:** the tokens in the `:root` block at the top of the stylesheet, with dark-mode values in the two blocks below it.

## Ideas for later

Real dates and week-to-week navigation, exam/deadline markers, marking blocks done or skipped with planned-vs-done hours, a phone day view with swipe, a "now and next" card, a focus timer, weekly targets per label, JSON/.ics export, and links to a reading roadmap.
