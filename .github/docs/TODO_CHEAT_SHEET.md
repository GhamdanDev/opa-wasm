# 🚀 TODO Action - Cheat Sheet

## Quick Reference Guide

---

## 📝 TODO Syntax

### Basic Format
```python
# TYPE: Description
# TYPE: Description with more details
#       on multiple lines
```

### Valid Types
| Type | Priority | When to Use |
|------|----------|-------------|
| `TODO` | Medium | New features, enhancements |
| `FIXME` | High | Known bugs, urgent fixes |
| `HACK` | Medium | Temporary solutions, tech debt |
| `XXX` | High | Critical warnings, attention needed |
| `BUG` | Critical | Serious bugs, production issues |
| `NOTE` | Low | Documentation, information |

---

## ✅ Good Examples

```python
# TODO: Add input validation for email field using RFC 5322
def register(email):
    pass

# FIXME: Race condition in concurrent access - add mutex lock
# BUG: Memory leak in loop - objects not released
# HACK: Hardcoded credentials - move to environment variables
# XXX: Performance-critical code - do not modify without review
# NOTE: Algorithm optimized for Python 3.12+ (uses PEP 669)
```

---

## ❌ Bad Examples

```python
# todo: fix  # lowercase
# TODO fix  # missing colon
# TODO:  # empty description
#TODO: test  # missing space after #
```

---

## 🏷️ Labels Applied

### TODO → `type:enhancement`, `priority:medium`, `todo`
### FIXME → `type:bug`, `priority:high`, `needs-fix`, `todo`
### HACK → `type:technical-debt`, `priority:medium`, `refactor`, `todo`
### XXX → `type:attention-needed`, `priority:high`, `todo`
### BUG → `type:bug`, `priority:critical`, `todo`
### NOTE → `type:documentation`, `priority:low`, `todo`

---

## 🔍 Search Queries

### By Priority
```
is:issue is:open label:priority:critical
is:issue is:open label:priority:high
is:issue is:open label:priority:medium
is:issue is:open label:priority:low
```

### By Type
```
is:issue is:open label:type:bug
is:issue is:open label:type:enhancement
is:issue is:open label:type:technical-debt
```

### My TODOs
```
is:issue is:open label:todo assignee:@me
```

### All TODOs
```
is:issue is:open label:todo
```

---

## 🛠️ Commands

### Setup (One Time)
```bash
# Create labels
gh workflow run setup-labels.yml

# Enable permissions
# Settings → Actions → Workflow permissions
# → Enable "Read and write permissions"
```

### Daily Use
```bash
# Local scan before push
./scripts/scan_todos.sh

# Scan specific directory
./scripts/scan_todos.sh src/

# Scan specific file
./scripts/scan_todos.sh src/main.py
```

### Manual Trigger
```bash
# From GitHub UI
# Actions → Create Issues from TODOs → Run workflow

# Or CLI
gh workflow run create-todo-issues.yml
```

---

## 📊 Dashboard

```bash
# Generate stats
gh workflow run todo-dashboard.yml

# View results
cat .github/TODO_DASHBOARD.md
```

---

## 🎯 Best Practices

### DO ✅
- Be specific and detailed
- Add time estimates
- Link to documentation
- Mention responsible person
- Explain business impact

### DON'T ❌
- Be vague ("fix this")
- Skip the colon
- Use lowercase
- Leave empty
- Forget context

---

## 🔄 Lifecycle

1. **Write TODO** in code
2. **Push** to GitHub
3. **Action runs** automatically
4. **Issue created** with labels
5. **Fix** the problem
6. **Remove TODO** from code
7. **Push** again
8. **Issue closes** automatically

---

## 📈 Quick Stats

Run: `./scripts/scan_todos.sh`

Shows:
- Total TODOs by type
- Priority distribution
- Critical items needing attention
- Colored output
- Markdown report

---

## 🔧 Files Reference

| File | Purpose |
|------|---------|
| `.github/workflows/create-todo-issues.yml` | Main workflow |
| `.github/workflows/setup-labels.yml` | Label setup |
| `.github/workflows/todo-dashboard.yml` | Daily reports |
| `README_TODO_ACTION.md` | Complete guide |
| `.github/TODO_QUICK_START.md` | Quick start |
| `examples/todo_best_practices.py` | 50+ examples |
| `scripts/scan_todos.sh` | Local scanner |

---

## ⚙️ Configuration

Located in: `.github/workflows/create-todo-issues.yml`

```yaml
AUTO_ASSIGN: true       # Assign to TODO author
CLOSE_ISSUES: true      # Close when TODO removed
AUTO_P: true            # Format as paragraphs
ESCAPE: true            # Escape special chars
```

---

## 🎨 Issue Template

Each issue includes:
- 📋 Summary (your comment)
- 📍 Location (file and line)
- 💻 Code Context (snippet)
- ✅ Acceptance Criteria (checklist)

---

## 🚦 Triggers

| Event | When | Type |
|-------|------|------|
| Push | To main/master | Auto |
| Pull Request | Open/Update | Auto |
| Schedule | Mon 9AM UTC | Auto |
| Manual | From Actions | Manual |

---

## 💡 Pro Tips

### Add Estimates
```python
# TODO: [Est: 4h] Implement caching layer
```

### Link Issues
```python
# TODO: Refactor auth (related to #42)
```

### Assign Person
```python
# FIXME: @username review this logic
```

### Add Business Value
```python
# TODO: [REVENUE-IMPACT] Add premium features
```

---

## 🆘 Troubleshooting

### No Issues Created?
1. Check permissions (Settings → Actions)
2. Verify TODO format (colon after type)
3. Check Action logs
4. Ensure file not in IGNORE list

### Duplicate Issues?
1. Avoid multiple triggers for same code
2. Enable CLOSE_ISSUES
3. Use INSERT_ISSUE_URLS

### Wrong Labels?
1. Run setup-labels.yml
2. Check IDENTIFIERS config
3. Verify label names match

---

## 📚 Learn More

- **Complete Guide:** `README_TODO_ACTION.md`
- **Quick Start:** `.github/TODO_QUICK_START.md`
- **Full Docs:** `.github/TODO_WORKFLOW_GUIDE.md`
- **Examples:** `examples/todo_best_practices.py`
- **Official Action:** [GitHub](https://github.com/alstr/todo-to-issue-action)

---

<div align="center">

**Keep this cheat sheet handy!** 📌

Print or bookmark for quick reference 🚀

</div>
