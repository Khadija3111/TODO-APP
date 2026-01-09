# Implementation Plan: Intermediate-Level Features for Console-Based Todo App

## 1. Architecture Sketch (Textual)

### Data Flow:
```
CLI → Command parser (argparse) → Service layer (TaskStore) → Model (Task with priority, tags[]) → Renderer (plain text with ANSI colors)
Config file (~/.todo/config.json) stores user preferences (last sort field & order)
```

### Component Structure:
```
src/
├── models/
│   └── task.py          # Extended Task model (priority, tags)
├── services/
│   ├── task_store.py    # Extended storage with search/filter/sort
│   └── config_service.py # Config file handling
├── cli/
│   ├── cli_interface.py # Command parser and dispatch
│   └── renderers.py     # Output formatting with ANSI colors
└── utils/
    ├── filters.py       # Filter utility functions
    ├── search.py        # Search utility functions
    └── sorters.py       # Sort utility functions
```

## 2. Feature Breakdown

### A. Extended Task Model (src/models/task.py)
- Add `priority` field (enum: high/medium/low)
- Add `tags` field (list of strings)
- Add validation for new fields
- Update `to_dict()` method

### B. Extended Task Store (src/services/task_store.py)
- Update `add_task()` to accept priority and tags
- Update `update_task()` to handle priority and tags
- Add `search_tasks()` method
- Add `filter_tasks()` method
- Add `sort_tasks()` method
- Add `get_task_statistics()` method

### C. Config Service (src/services/config_service.py)
- Load/save config from `~/.todo/config.json`
- Store default sort preferences
- Handle config initialization

### D. CLI Commands
- `todo add --priority high|medium|low --tags tag1,tag2 "title"`
- `todo list --status all|pending|completed --priority high|medium|low|any --tags tag1,tag2 --sort created|priority|alpha --order asc|desc`
- `todo search <keyword>`
- Update help text and error handling

### E. Utility Modules
- Filter functions (status, priority, tags)
- Search functions (case-insensitive partial matching)
- Sort functions (by various fields, ascending/descending)
- ANSI color rendering

## 3. Implementation Roadmap (5 Business Days)

### Day 1: Foundation
- [ ] Extend Task model with priority and tags fields
- [ ] Create config service for persistent preferences
- [ ] Update TaskStore to handle new fields
- [ ] Document decisions in DECISIONS.md

### Day 2: Core Functionality
- [ ] Implement search functionality (case-insensitive partial matching)
- [ ] Implement filter functionality (status, priority, tags)
- [ ] Implement sort functionality (all fields, asc/desc)
- [ ] Write unit tests for new utility functions

### Day 3: CLI Integration
- [ ] Update CLI interface with new commands and flags
- [ ] Implement `todo add` with priority/tags options
- [ ] Implement `todo list` with filter/sort options
- [ ] Implement `todo search` command
- [ ] Add ANSI color support for output

### Day 4: Testing & QA
- [ ] Write integration tests for CLI commands
- [ ] Performance test with 500 tasks
- [ ] Accessibility testing (help text, error messages)
- [ ] Cross-platform testing (Windows, macOS, Linux)

### Day 5: Documentation & Polish
- [ ] Update README with new usage examples
- [ ] Verify all acceptance criteria
- [ ] Final testing and bug fixes
- [ ] Commit and prepare release

## 4. Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| State storage | In-memory only (as per constitution) | Maintains existing architecture, simpler implementation |
| CLI framework | Python argparse | Built-in, no additional dependencies, familiar to Python developers |
| Tag input format | Comma-separated string (e.g., "work,home") | Simpler parsing, consistent with specification |
| Config persistence | JSON file in `~/.todo/config.json` | Human-readable, easy to modify, standard approach |
| Search implementation | In-memory filtering | Fast for reasonable task counts, no external dependencies |
| Color output | ANSI colors with `--no-color` flag | Improves UX while maintaining compatibility |

## 5. Testing Strategy

### Unit Tests
- Model validation for `priority` enum and `tags[]`
- Filter, search, and sort utility functions (edge cases, empty inputs)
- Config service (load/save, defaults)

### Integration Tests
- `todo add -p high -t work,home "Write report"` → verify stored correctly
- `todo list --priority high --tags work` → only matching tasks displayed
- `todo search meet` → case-insensitive partial matches returned
- `todo list --sort priority --order desc` → order verified; config persistence

### Performance Tests
- Populate 500 tasks
- Measure `list`, `search`, `filter`, `sort` operations
- Assert ≤ 100ms completion time

### Accessibility Tests
- Verify `--help` output contains all flags and examples
- Test with `--no-color` flag
- Verify error messages and exit codes

## 6. Quality Validation Checklist

- [ ] Priority and tags can be set via CLI flags and stored correctly
- [ ] `list` filters by status, priority, tags; works in any combination
- [ ] `search` returns correct case-insensitive partial matches
- [ ] Sorting works for all fields and persists via config file
- [ ] Help text is complete and examples are provided
- [ ] ANSI color output degrades when disabled
- [ ] All operations on 500 tasks complete ≤ 100ms
- [ ] Unit + integration test coverage ≥ 80%
- [ ] All decisions recorded in DECISIONS.md

## 7. Deliverables

- [ ] `architecture.txt` - Updated architecture diagram
- [ ] Updated source code (CLI commands, model, config handling)
- [ ] `DECISIONS.md` - Documented trade-offs and choices
- [ ] Test suite with coverage report
- [ ] Updated `README.md` with usage examples and installation steps
- [ ] Working console app with all intermediate features implemented