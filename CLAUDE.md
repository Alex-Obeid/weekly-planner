# Weekly Planner: notes for Claude Code

Single-file web app: everything lives in `index.html` (HTML, CSS in `<style>`, vanilla JS in one IIFE). No build step, no framework, no package manager. Keep it that way unless asked.

## Running and checking

- Open `index.html` directly in a browser, or serve the folder (`python3 -m http.server`).
- There are no automated tests. After changes, check by hand: add/edit/delete a block, drag to move and resize, create a repeat on several days and edit "All repeats" vs "Only this day", duplicate a block, copy a day (add and replace modes), confirm clash outlines and the free-time gaps, and check light and dark themes plus a ~400px-wide phone viewport.

## Architecture

- **State:** `blocks` (array of `{id, day, start, end, title, label, note, series?}`), `labels` (array of `{id, name, color}`), and `mode` (`"db"`, `"local"` or `"loading"`).
- **Persistence:** all block writes go through `commit(saves, removes)`; labels through `saveLabels(next)`. In `"local"` mode these update the arrays, write `localStorage["rcvd-planner-v1"]` and re-render. In `"db"` mode they write to the claude.ai artifact database via `window.claude.use("db")`, and `onSnapshot` listeners re-render. Code must keep working when `window.claude` is absent (plain browser).
- **Rendering:** `render()` redraws the grid (it defers while a drag is active); `renderWeek()` does the work and also calls `renderTotals()` (share bar) and `renderClashes()`. `renderLabels()` draws the labels panel.
- **Times:** stored as `"HH:MM"` 24-hour strings; `toMin`/`toHHMM` convert; display uses `fmt12`/`fmtRange` (AM/PM). Visible range is `DAY_START`–`DAY_END` (7 AM–11 PM).
- **Drag:** pointer events (`startPress`, `onMove`, `onUp`, `onCancel`). Mouse drags start after 6 px; touch needs a 360 ms hold so scrolling still works. A drag edits only the dragged block, even if it is part of a series.
- **Repeats:** blocks created together share a `series` id. The form's scope switch decides whether edits and deletes apply to the whole series or one day.

## Conventions

- Colours come from CSS tokens in `:root` with matching dark-mode overrides; never hard-code a colour that only works in one theme (label colours are user data and use `textOn()` for readable text).
- Build DOM with `textContent` for any user text (titles, notes, label names); never inject user text as HTML.
- Use in-page confirmations (the two-step "Delete" → "Confirm delete" pattern); `alert`/`confirm`/`prompt` are not allowed in the artifact viewer.
