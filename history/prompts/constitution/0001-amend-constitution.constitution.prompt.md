---
id: 0001
title: Amend Constitution
stage: constitution
date: 2025-12-31
surface: command
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: pc
command: sp.constitution
labels: [constitution, update, todo-app]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - path: .specify/memory/constitution.md
    action: update
    summary: Updated constitution to add intermediate and advanced features
tests:
  - path:
    action:
    summary:
---

## Prompt

 # Todo App – Extended Constitution (Concise)

## Already Implemented (Basic)
- Add / Delete / Update / View tasks
- Mark as complete

---

## INTERMEDIATE FEATURES (Usability)

1. **Priorities & Tags**
   - Task fields: `priority` (high/med/low), `tags[]` (e.g., work, home)
   - UI: dropdown for priority, multi‑select chips for tags
   - ✅ Users can set/change priority & tags; list can be filtered by them.

2. **Search & Filter**
   - Search bar (title/description, case‑insensitive)
   - Filter panel: status, priority, tags, date range
   - ✅ Real‑time results; combined filters work; "no match" message shown.

3. **Sort**
   - Options: due date, priority, alphabetical, creation date (asc/desc)
   - Persist choice in local storage
   - ✅ Selecting a sort instantly reorders the list.

---

## ADVANCED FEATURES (Intelligence)

4. **Recurring Tasks**
   - Field `recurrence` (none, daily, weekly, monthly, custom)
   - On completion, auto‑create next instance with updated due date
   - ✅ Users set recurrence; completing generates next task preserving other data.

5. **Due Dates & Reminders**
   - Fields `dueDate` (+ optional `dueTime`)
   - Date‑time picker UI
   - Browser notifications: 10 min before & at due time, with snooze option
   - ✅ Notifications fire (with permission); overdue tasks highlighted.

---

## COMMON RULES
- Follow existing UI style & accessibility (ARIA, keyboard).
- Lazy‑load heavy components; debounce search.
- Add unit & integration tests for new fields/behaviours.
- Update README & code comments.

---

*Add these sections to your current constitution and commit.*   i want u to update my constitution and add these

## Response snapshot

Constitution file updated successfully with the new intermediate and advanced features. The version was updated from 1.1.0 to 1.2.0, and the file now includes sections for:

1. Priorities & Tags
2. Search & Filter
3. Sort
4. Recurring Tasks
5. Due Dates & Reminders

The sync impact report was updated to reflect these changes, and the core principles section was maintained.

## Outcome

- ✅ Impact: Constitution updated with new features, version bumped to 1.2.0
- 🧪 Tests: N/A for this constitution update
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: N/A
- 🧠 Reflection: Successfully integrated new feature requirements into existing constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
