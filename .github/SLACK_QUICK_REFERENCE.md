# 🔔 Slack Integration - Quick Reference

> **One-page cheat sheet for Slack + GitHub Actions TODO integration**

---

## ⚡ 3-Minute Setup

```bash
# 1. Create Slack App
→ api.slack.com/apps → "Create New App" → "From scratch"

# 2. Add Bot Token Scopes
OAuth & Permissions → Bot Token Scopes:
  ✅ chat:write
  ✅ chat:write.public  
  ✅ channels:read

# 3. Install to Workspace
"Install to Workspace" → Copy Bot Token (xoxb-...)

# 4. Add to GitHub
Settings → Secrets → Actions → New:
  Name: SLACK_BOT_TOKEN
  Value: xoxb-...

# 5. Invite Bot to Channels
In Slack: /invite @BotName

# 6. Test
Actions → "Advanced Slack Notifications" → "Run workflow" → test_notification
```

---

## 📋 Required GitHub Secrets

| Secret | Value | How to Get |
|--------|-------|------------|
| `SLACK_BOT_TOKEN` | `xoxb-xxx-xxx-xxx` | Slack App → OAuth & Permissions → Bot User OAuth Token |

**Optional (for custom channels):**
- `SLACK_CRITICAL_CHANNEL` (default: `#critical-todos`)
- `SLACK_GENERAL_CHANNEL` (default: `#dev-todos`)
- `SLACK_REPORTS_CHANNEL` (default: `#dev-reports`)

---

## 🎯 Notification Types

| Type | When | Channel | Alert Level |
|------|------|---------|-------------|
| 🚨 **Critical Alert** | FIXME/BUG found | `#critical-todos` | @channel mention |
| 📊 **Daily Summary** | 9 AM (Mon-Fri) | `#dev-reports` | No mention |
| 📈 **Weekly Metrics** | Manual | `#dev-reports` | No mention |
| 🧪 **Test** | Manual | `#dev-todos` | No mention |

---

## 🛠️ Common Issues & Fixes

### ❌ "channel_not_found"
```bash
# Fix: Invite bot to channel
/invite @BotName
```

### ❌ "not_authed"
```bash
# Fix: Check SLACK_BOT_TOKEN secret exists and is correct
Settings → Secrets → Actions → SLACK_BOT_TOKEN
```

### ❌ "missing_scope"
```bash
# Fix: Add required scope
Slack App → OAuth & Permissions → Bot Token Scopes → Add: chat:write
Then: Reinstall app
Then: Update SLACK_BOT_TOKEN in GitHub
```

### ❌ "rate_limited"
```bash
# Fix: Workflow already implements batching
# If still an issue, reduce notification frequency
```

---

## 🎨 Color Scheme

```yaml
🔴 Critical (#FF0000)  →  FIXME, BUG
🟠 High     (#FF6B00)  →  HACK, XXX
🟡 Medium   (#FFD700)  →  TODO
🟢 Low      (#00AA00)  →  NOTE
```

---

## 📱 Example Slack Message

```
╔═══════════════════════════════════════╗
║ 🚨 Critical TODOs Require Attention   ║
╠═══════════════════════════════════════╣
║ Repository: owner/repo                ║
║ Branch: main                          ║
║                                       ║
║ Critical: 3 🔴                        ║
║ High: 5 🟠                            ║
║                                       ║
║ @channel Action required: Critical    ║
║ issues detected in codebase.          ║
║                                       ║
║ [View Issues] [View Repo] [Workflow]  ║
╚═══════════════════════════════════════╝
```

---

## 🚀 Manual Triggers

```bash
# Test notification
Actions → "Advanced Slack Notifications" → "Run workflow"
→ Select: test_notification

# Daily summary (on-demand)
→ Select: daily_summary

# Weekly report
→ Select: weekly_report

# Critical alert (on-demand)
→ Select: critical_alert
```

---

## ⚙️ Customization

### Change notification schedule:
```yaml
# In .github/workflows/slack-notifications-advanced.yml
on:
  schedule:
    - cron: '0 9 * * 1-5'  # 9 AM Mon-Fri
    # Change to your timezone and preference
```

### Change channels:
```yaml
# Option 1: GitHub Secrets (recommended)
Settings → Secrets → Actions → New:
  SLACK_CRITICAL_CHANNEL: #my-channel

# Option 2: In workflow file
env:
  SLACK_CRITICAL_CHANNEL: '#my-custom-channel'
```

### Disable critical alerts:
```yaml
# In workflow file, comment out or delete:
# critical-alert:
#   needs: analyze-todos
#   if: needs.analyze-todos.outputs.has_critical == 'true'
#   ...
```

---

## 📚 Best Practices Summary

| Practice | Why |
|----------|-----|
| ✅ Use separate channels | Reduces noise, allows prioritization |
| ✅ Only @channel for critical | Prevents alert fatigue |
| ✅ Use Block Kit formatting | Better readability, actionable buttons |
| ✅ Batch notifications | Respects rate limits, reduces spam |
| ✅ Schedule wisely | Respects work hours, increases engagement |
| ✅ Include action buttons | Enables quick response |
| ✅ Implement error handling | Ensures delivery |
| ✅ Rotate tokens regularly | Security best practice |

---

## 🔒 Security Checklist

- [ ] Token stored in GitHub Secrets (not in code)
- [ ] Use bot tokens (not user tokens)
- [ ] Only grant required OAuth scopes
- [ ] Rotate tokens every 90 days
- [ ] Monitor token usage for anomalies
- [ ] Enable Slack audit logging

---

## 📞 Quick Links

- [Slack API Documentation](https://api.slack.com)
- [Block Kit Builder](https://app.slack.com/block-kit-builder)
- [GitHub Slack Action](https://github.com/slackapi/slack-github-action)
- [Full Integration Guide](./SLACK_INTEGRATION_GUIDE.md)

---

## 🆘 Emergency Troubleshooting

```bash
# 1. Check workflow logs
GitHub → Actions → Click failed workflow → View logs

# 2. Verify bot token
GitHub → Settings → Secrets → SLACK_BOT_TOKEN exists?

# 3. Test Slack API manually
curl -X POST https://slack.com/api/auth.test \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Verify bot in channel
Slack → Channel → View members → Bot listed?

# 5. Check scopes
api.slack.com/apps → Your App → OAuth & Permissions → Scopes
```

---

**Version:** 2.0 | **Last Updated:** 2025-01-17
