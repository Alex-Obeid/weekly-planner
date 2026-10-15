# Weekly Planner: notes for Claude Code

Single-file web app: everything lives in `index.html` (HTML, CSS in `<style>`, vanilla JS in one IIFE). No build step, no framework, no package manager. Keep it that way unless asked.

The only files beside it are the PWA shell — `manifest.webmanifest`, `sw.js`, `icons/` — and `tools/build-icons.py`, which generates the icons. **Edit the generator, never the PNGs.** All three only come into play over http(s); opened as a file the page runs exactly as it always did, so guard anything new on `location.protocol` the same way. **Bump `VERSION` in `sw.js` whenever `index.html` changes**, or an installed copy can serve the old build while offline.

## Running and checking

- Open `index.html` directly in a browser, or serve the folder (`python3 -m http.server`).
- There are no automated tests. After changes, check by hand: add/edit/delete a block, drag to move and resize, create a repeat on several days and edit "All repeats" vs "Only this day", duplicate a block, copy a day (add and replace modes), export a week and import it back (both modes, and a deliberately broken file), confirm clash outlines and the free-time gaps, change the awake hours (including a bedtime of midnight, and narrowing them until a block falls outside), check the "NOW:" bar against a block that spans the current time and that it disappears when none does, and check light and dark themes plus a ~400px-wide phone viewport.

## Architecture

- **State:** `blocks` (array of `{id, day, start, end, title, label, note, series?}`), `labels` (array of `{id, name, color}`), and `mode` (`"db"`, `"local"` or `"loading"`).
- **Persistence:** all block writes go through `commit(saves, removes)`; labels through `saveLabels(next)`. In `"local"` mode these update the arrays, write `localStorage["rcvd-planner-v1"]` and re-render. In `"db"` mode they write to the claude.ai artifact database via `window.claude.use("db")`, and `onSnapshot` listeners re-render. Code must keep working when `window.claude` is absent (plain browser).
- **Rendering:** `render()` redraws the grid (it defers while a drag is active); `renderWeek()` does the work and also calls `renderTotals()` (share bars) and `renderClashes()`. `renderTotals()` builds one `periodGroup()` per entry in `PERIODS` (Mon–Fri, Sat–Sun); each is a share of **its own** span, not of the week, so the two are not comparable as percentages — compare the hours in the legend. Add a period by adding to `PERIODS`; nothing else needs to change. `renderLabels()` draws the labels panel.
- **Times:** stored as `"HH:MM"` 24-hour strings; `toMin`/`toHHMM` convert; display uses `fmt12`/`fmtRange` (AM/PM). **`DAY_START` and `DAY_END` are `let`, not constants** — the user sets them (*Awake ... to ...*), they persist under `rcvd-planner-v1-day`, and `setDay()` re-renders everything that derives from them, the form's time dropdowns included. Anything new that reads them must survive their changing. Bedtime may be `24 * 60`, so `"24:00"` is a legal end time and `HHMM` in `parseWeek()` accepts it.
- **Drag:** pointer events (`startPress`, `onMove`, `onUp`, `onCancel`). Mouse drags start after 6 px; touch needs a 360 ms hold so scrolling still works. A drag edits only the dragged block, even if it is part of a series.
- **Repeats:** blocks created together share a `series` id. The form's scope switch decides whether edits and deletes apply to the whole series or one day.
- **Backup:** the *Backup* dialog exports `{app, version, exported, labels, blocks}` and imports it back. `parseWeek()` validates and drops anything malformed; `applyImport()` writes through `commit`/`saveLabels` like everything else, so it works in both modes. Exports carry **no block ids** — `applyImport` mints fresh ones with `uid()`, and in add mode it also remaps label ids by name and re-keys `series`, so an import can never collide with existing data. Bump `EXPORT_VERSION` if the stored shape changes, and teach `parseWeek()` to read the old one.

## Conventions

- Colours come from CSS tokens in `:root` with matching dark-mode overrides; never hard-code a colour that only works in one theme (label colours are user data and use `textOn()` for readable text).
- Build DOM with `textContent` for any user text (titles, notes, label names); never inject user text as HTML.
- Use in-page confirmations (the two-step "Delete" → "Confirm delete" pattern); `alert`/`confirm`/`prompt` are not allowed in the artifact viewer.
