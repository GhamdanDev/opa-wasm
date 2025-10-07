# 🔔 Slack Integration Expert Guide

> **Expert-Level Best Practices for Slack + GitHub Actions Integration**

This guide provides professional-grade Slack integration for your TODO/FIXME workflow, following industry best practices used by top DevOps teams.

---

## 📚 Table of Contents

1. [Quick Setup](#-quick-setup)
2. [Architecture Overview](#-architecture-overview)
3. [Best Practices](#-best-practices)
4. [Configuration Options](#-configuration-options)
5. [Security](#-security)
6. [Troubleshooting](#-troubleshooting)
7. [Advanced Features](#-advanced-features)

---

## 🚀 Quick Setup

### Step 1: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Name it: `TODO Bot` or `GitHub Assistant`
4. Select your workspace

### Step 2: Configure Bot Permissions

Navigate to **OAuth & Permissions** and add these scopes:

**Required Bot Token Scopes:**
- `chat:write` - Post messages
- `chat:write.public` - Post to public channels
- `channels:read` - List public channels
- `groups:read` - List private channels

**Optional (for advanced features):**
- `users:read` - Mention users by name
- `reactions:write` - Add emoji reactions
- `files:write` - Upload reports as files

### Step 3: Install App to Workspace

1. Click **"Install to Workspace"**
2. Authorize the app
3. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### Step 4: Add GitHub Secrets

Add these secrets to your GitHub repository:

```
Settings → Secrets and variables → Actions → New repository secret
```

**Required Secrets:**

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token | `xoxb-xxx-xxx-xxxxx` |

**Optional Secrets (for tiered notifications):**

| Secret Name | Description | Default Value |
|-------------|-------------|---------------|
| `SLACK_CRITICAL_CHANNEL` | Channel for critical alerts | `#critical-todos` |
| `SLACK_GENERAL_CHANNEL` | General TODO updates | `#dev-todos` |
| `SLACK_REPORTS_CHANNEL` | Daily/weekly reports | `#dev-reports` |

### Step 5: Invite Bot to Channels

In Slack, invite your bot to the channels:

```
/invite @TODO Bot
```

### Step 6: Test the Integration

Trigger a test notification:

```bash
# Go to Actions tab → "Advanced Slack Notifications" → "Run workflow"
# Select: "test_notification"
```

---

## 🏗️ Architecture Overview

### Tiered Notification Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions Workflow                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├─── Analyze TODOs (scan codebase)
                     │
        ─────────────┴─────────────
        │                         │
   [Critical?]              [Scheduled?]
        │                         │
        ├─────────┐               ├──────────┐
        │         │               │          │
   ✅ YES     ❌ NO          Daily      Weekly
        │                         │          │
        ▼                         ▼          ▼
┌───────────────┐     ┌─────────────────┐  ┌────────────────┐
│ 🚨 Critical   │     │ 📊 Daily        │  │ 📈 Weekly      │
│    Alert      │     │   Summary       │  │   Metrics      │
│               │     │                 │  │                │
│ #critical-    │     │ #dev-reports    │  │ #dev-reports   │
│  todos        │     │                 │  │                │
│               │     │                 │  │                │
│ @channel      │     │ (no mentions)   │  │ (no mentions)  │
└───────────────┘     └─────────────────┘  └────────────────┘
```

### Notification Types

| Type | Trigger | Channel | Mentions | Frequency |
|------|---------|---------|----------|-----------|
| **Critical Alert** | FIXME/BUG detected | `#critical-todos` | `@channel` | Immediate |
| **Daily Summary** | Scheduled (9 AM) | `#dev-reports` | None | Daily (Mon-Fri) |
| **Weekly Metrics** | Manual/Scheduled | `#dev-reports` | None | Weekly |
| **Test** | Manual trigger | `#dev-todos` | None | On-demand |

---

## ⭐ Best Practices

### 1. **Use Tiered Channels**

❌ **Don't:** Send all notifications to one channel
```yaml
# Bad: Everything in #general
SLACK_CHANNEL: '#general'
```

✅ **Do:** Use dedicated channels for different priorities
```yaml
# Good: Separate channels
SLACK_CRITICAL_CHANNEL: '#critical-todos'
SLACK_GENERAL_CHANNEL: '#dev-todos'
SLACK_REPORTS_CHANNEL: '#dev-reports'
```

**Why:** Prevents notification fatigue and allows team members to prioritize.

---

### 2. **Minimize @channel Mentions**

❌ **Don't:** Use `@channel` for every notification
```yaml
# Bad: Too noisy
message: "<!channel> Found a TODO"
```

✅ **Do:** Reserve `@channel` for critical items only
```yaml
# Good: Only for critical
if: priority == 'critical'
  message: "<!channel> Critical issue detected"
else:
  message: "New TODO found"
```

**Why:** Reduces interruptions and maintains team focus.

---

### 3. **Use Rich Formatting (Block Kit)**

❌ **Don't:** Send plain text messages
```json
{
  "text": "Found 5 TODOs in the codebase"
}
```

✅ **Do:** Use Slack Block Kit for rich, actionable messages
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "📊 TODO Summary"}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Critical:* 2 🔴"},
        {"type": "mrkdwn", "text": "*High:* 3 🟠"}
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "View Issues"},
          "url": "https://github.com/..."
        }
      ]
    }
  ]
}
```

**Why:** Better visibility, easier scanning, and actionable buttons.

---

### 4. **Implement Rate Limiting**

❌ **Don't:** Send individual messages for each TODO
```yaml
# Bad: Sends 100 messages for 100 TODOs
for todo in todos:
  send_slack_message(todo)
```

✅ **Do:** Batch notifications and summarize
```yaml
# Good: One message with summary
summary = analyze_all_todos()
send_slack_message(summary)
```

**Why:** Prevents Slack channel spam and respects rate limits.

---

### 5. **Add Actionable Buttons**

❌ **Don't:** Just inform without actions
```json
{
  "text": "5 critical TODOs found. Please check GitHub."
}
```

✅ **Do:** Include direct action buttons
```json
{
  "blocks": [
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": "View Critical Issues",
          "url": "...",
          "style": "danger"
        },
        {
          "type": "button",
          "text": "Assign to Me",
          "url": "..."
        }
      ]
    }
  ]
}
```

**Why:** Reduces friction and enables quick responses.

---

### 6. **Schedule Reports Wisely**

❌ **Don't:** Send reports on weekends or during off-hours
```yaml
# Bad: Runs at 3 AM on Saturday
- cron: '0 3 * * 6'
```

✅ **Do:** Schedule during working hours
```yaml
# Good: 9 AM Monday-Friday
- cron: '0 9 * * 1-5'
```

**Why:** Respects work-life balance and increases engagement.

---

### 7. **Use Color Coding**

✅ **Apply consistent color scheme:**

```yaml
COLOR_CRITICAL: '#FF0000'  # Red
COLOR_HIGH:     '#FF6B00'  # Orange  
COLOR_MEDIUM:   '#FFD700'  # Yellow
COLOR_LOW:      '#00AA00'  # Green
COLOR_INFO:     '#0099FF'  # Blue
```

**Visual Impact:**
```
🔴 Critical (Red)    → Immediate action required
🟠 High (Orange)     → Review this week
🟡 Medium (Yellow)   → Review this sprint
🟢 Low (Green)       → Low priority
```

---

### 8. **Implement Error Handling**

✅ **Always include fallback behavior:**

```yaml
- name: Send Slack Notification
  uses: slackapi/slack-github-action@v1.27.0
  continue-on-error: true  # Don't fail workflow if Slack is down
  with:
    # ... configuration
```

```yaml
- name: Fallback Email Notification
  if: failure()  # Only if Slack fails
  run: |
    echo "Slack notification failed. Sending email..."
    # Send email backup notification
```

**Why:** Ensures notifications are delivered even if Slack is unavailable.

---

### 9. **Security Best Practices**

✅ **Token Management:**

```yaml
# ✅ Good: Use GitHub Secrets
env:
  SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}

# ❌ Bad: Hardcoded token (NEVER do this!)
env:
  SLACK_BOT_TOKEN: xoxb-EXAMPLE-NOT-REAL
```

✅ **Token Rotation:**
- Rotate tokens every 90 days
- Use different tokens for dev/staging/prod
- Audit token usage regularly

✅ **Least Privilege:**
- Grant only required OAuth scopes
- Use bot tokens, not user tokens
- Review permissions quarterly

---

### 10. **Monitor and Measure**

✅ **Track these metrics:**

```yaml
📊 Notification Metrics:
  - Delivery rate (should be >99%)
  - Response time (click-through rate)
  - Resolution rate (TODOs closed vs created)
  - False positive rate (ignored notifications)
```

✅ **Set up alerts:**
```yaml
# Alert if notification delivery fails
- name: Monitor Delivery
  if: failure()
  run: |
    # Send alert to ops team
    curl -X POST ${{ secrets.PAGERDUTY_WEBHOOK }}
```

---

## ⚙️ Configuration Options

### Environment Variables

```yaml
env:
  # Channel Configuration (tiered approach)
  SLACK_CRITICAL_CHANNEL: '#critical-todos'
  SLACK_GENERAL_CHANNEL: '#dev-todos'
  SLACK_REPORTS_CHANNEL: '#dev-reports'
  
  # Color Scheme
  COLOR_CRITICAL: '#FF0000'
  COLOR_HIGH: '#FF6B00'
  COLOR_MEDIUM: '#FFD700'
  COLOR_LOW: '#00AA00'
  
  # Mention Configuration
  MENTION_ON_CRITICAL: true
  MENTION_CODEOWNERS: true
  
  # Rate Limiting
  MAX_NOTIFICATIONS_PER_RUN: 10
  BATCH_DELAY_SECONDS: 5
```

### Customizing Channels

**Option 1: Use repository secrets (recommended)**
```yaml
SLACK_CRITICAL_CHANNEL: ${{ secrets.SLACK_CRITICAL_CHANNEL }}
```

**Option 2: Hardcode in workflow (for single repo)**
```yaml
SLACK_CRITICAL_CHANNEL: '#my-team-critical'
```

**Option 3: Use repository variables (for easier updates)**
```yaml
SLACK_CRITICAL_CHANNEL: ${{ vars.SLACK_CRITICAL_CHANNEL }}
```

---

## 🔒 Security

### Token Security Checklist

- [ ] Store tokens in GitHub Secrets (never in code)
- [ ] Use bot tokens, not user tokens
- [ ] Implement token rotation (every 90 days)
- [ ] Audit token permissions quarterly
- [ ] Use environment-specific tokens (dev/prod)
- [ ] Enable audit logging in Slack
- [ ] Monitor token usage for anomalies
- [ ] Revoke tokens immediately if compromised

### OAuth Scopes Explained

| Scope | Purpose | Required? |
|-------|---------|-----------|
| `chat:write` | Post messages to channels | ✅ Yes |
| `chat:write.public` | Post to channels without joining | ✅ Yes |
| `channels:read` | List public channels | ✅ Yes |
| `users:read` | Get user info for mentions | ⚠️ Optional |
| `reactions:write` | Add emoji reactions | ⚠️ Optional |
| `files:write` | Upload files/reports | ⚠️ Optional |

**Principle:** Only request scopes you actually need.

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **"channel_not_found" Error**

**Symptom:**
```
Error: channel_not_found
```

**Causes:**
- Bot not invited to channel
- Channel name typo
- Private channel without bot access

**Fix:**
```bash
# In Slack:
/invite @TODO Bot

# Or use channel ID instead of name:
channel-id: 'C01234567'  # Instead of '#channel-name'
```

---

#### 2. **"not_authed" or "invalid_auth" Error**

**Symptom:**
```
Error: not_authed
```

**Causes:**
- Missing `SLACK_BOT_TOKEN` secret
- Token expired or revoked
- Wrong token format

**Fix:**
1. Verify secret exists:
   ```bash
   # GitHub: Settings → Secrets → Actions → SLACK_BOT_TOKEN
   ```

2. Regenerate token:
   ```
   Slack API → Your App → OAuth & Permissions → Reinstall
   ```

3. Update GitHub secret with new token

---

#### 3. **"missing_scope" Error**

**Symptom:**
```
Error: missing_scope
Needed: chat:write
```

**Fix:**
1. Go to Slack API → Your App → OAuth & Permissions
2. Add the required scope under "Bot Token Scopes"
3. Reinstall app to workspace
4. Update `SLACK_BOT_TOKEN` in GitHub

---

#### 4. **Rate Limiting (429 Error)**

**Symptom:**
```
Error: rate_limited
Retry after: 60 seconds
```

**Causes:**
- Too many messages sent too quickly
- Hitting Slack's rate limit (1 message/second for apps)

**Fix:**

Implement batching and delays:
```yaml
- name: Send Notifications with Rate Limiting
  run: |
    for i in {1..10}; do
      # Send message
      curl -X POST ...
      # Wait 2 seconds between messages
      sleep 2
    done
```

---

#### 5. **Notifications Not Appearing**

**Checklist:**
- [ ] Bot invited to channel? (`/invite @BotName`)
- [ ] Correct channel name/ID in workflow?
- [ ] Token has `chat:write` permission?
- [ ] Workflow actually running? (Check Actions tab)
- [ ] No errors in workflow logs?

**Debug:**
```yaml
- name: Debug Slack Configuration
  run: |
    echo "Channel: ${{ env.SLACK_CRITICAL_CHANNEL }}"
    echo "Token exists: ${{ secrets.SLACK_BOT_TOKEN != '' }}"
```

---

## 🚀 Advanced Features

### 1. **Threading (Keep Conversations Organized)**

Send updates as replies to original message:

```yaml
- name: Send Initial Message
  id: initial_msg
  uses: slackapi/slack-github-action@v1.27.0
  with:
    channel-id: '#dev-todos'
    payload: |
      {"text": "Starting TODO scan..."}

- name: Send Update as Thread
  uses: slackapi/slack-github-action@v1.27.0
  with:
    channel-id: '#dev-todos'
    payload: |
      {
        "thread_ts": "${{ steps.initial_msg.outputs.ts }}",
        "text": "Scan complete! Found 5 TODOs"
      }
```

---

### 2. **User Mentions Based on CODEOWNERS**

Mention the right people automatically:

```yaml
- name: Get Code Owner
  id: codeowner
  run: |
    # Parse CODEOWNERS file
    owner=$(grep "^${{ github.event.head_commit.modified[0] }}" .github/CODEOWNERS | awk '{print $2}')
    echo "owner=$owner" >> $GITHUB_OUTPUT

- name: Notify Code Owner
  uses: slackapi/slack-github-action@v1.27.0
  with:
    payload: |
      {
        "text": "Hey <@${{ steps.codeowner.outputs.owner }}>, you have a new TODO in your area!"
      }
```

---

### 3. **Emoji Reactions for Status**

Add reactions to show processing status:

```yaml
- name: Add Processing Reaction
  run: |
    curl -X POST https://slack.com/api/reactions.add \
      -H "Authorization: Bearer ${{ secrets.SLACK_BOT_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d '{
        "channel": "C01234567",
        "timestamp": "'$MESSAGE_TS'",
        "name": "hourglass"
      }'

- name: Add Done Reaction
  run: |
    # Remove hourglass, add checkmark
    curl -X POST https://slack.com/api/reactions.add \
      -d '{"name": "white_check_mark", ...}'
```

---

### 4. **Interactive Buttons with Workflows**

Create buttons that trigger GitHub Actions:

```json
{
  "type": "button",
  "text": {"type": "plain_text", "text": "Assign to Me"},
  "url": "https://github.com/owner/repo/actions/workflows/assign.yml?ref=main&inputs.issue_number=42"
}
```

---

### 5. **File Uploads (For Large Reports)**

Upload reports as files instead of messages:

```yaml
- name: Upload TODO Report
  run: |
    curl -F file=@todo-report.json \
         -F channels=C01234567 \
         -F "initial_comment=Here's the full TODO report" \
         -H "Authorization: Bearer ${{ secrets.SLACK_BOT_TOKEN }}" \
         https://slack.com/api/files.upload
```

---

### 6. **Scheduled Digests (Summary Reports)**

Instead of individual notifications, send a digest:

```yaml
on:
  schedule:
    # Monday at 9 AM: Weekly kickoff
    - cron: '0 9 * * 1'
    # Friday at 4 PM: Weekly wrap-up
    - cron: '0 16 * * 5'
```

---

### 7. **Custom Slack Commands**

Set up slash commands to trigger workflows:

1. **In Slack App:**
   - Features → Slash Commands → Create New Command
   - Command: `/todos-summary`
   - Request URL: `https://your-webhook-url.com/slack-command`

2. **In GitHub:**
   - Use `repository_dispatch` event
   - Trigger workflow from webhook

---

## 📊 Metrics and Analytics

### Track These KPIs

```yaml
📈 Key Performance Indicators:

1. TODO Velocity
   - TODOs created per week
   - TODOs resolved per week
   - Net change (goal: negative or zero)

2. Resolution Time
   - Average time to close TODO
   - By priority (critical should be < 24h)

3. Technical Debt Ratio
   - TODOs per 1000 lines of code
   - Trend over time (goal: decreasing)

4. Notification Effectiveness
   - Click-through rate on Slack messages
   - Action rate (TODOs addressed after notification)
   - False positive rate (ignored notifications)
```

### Generate Reports

```yaml
- name: Generate Analytics
  run: |
    # Calculate metrics
    python scripts/calculate_todo_metrics.py > metrics.json
    
    # Send to Slack
    cat metrics.json | jq -r '.summary' | \
      slack-cli chat send \
        --channel "#dev-reports" \
        --text "$(cat -)"
```

---

## 🎯 Example Configurations

### For Small Teams (5-10 people)

```yaml
env:
  # Single channel for everything
  SLACK_CHANNEL: '#dev-team'
  
  # Only mention on critical
  MENTION_ON_CRITICAL: true
  MENTION_ON_HIGH: false
  
  # Daily summaries
on:
  schedule:
    - cron: '0 9 * * 1-5'
```

### For Medium Teams (10-50 people)

```yaml
env:
  # Tiered channels
  SLACK_CRITICAL_CHANNEL: '#critical-alerts'
  SLACK_GENERAL_CHANNEL: '#dev-todos'
  SLACK_REPORTS_CHANNEL: '#dev-metrics'
  
  # Mentions for critical and high
  MENTION_ON_CRITICAL: true
  MENTION_ON_HIGH: true
  
  # Daily + weekly reports
on:
  schedule:
    - cron: '0 9 * * 1-5'  # Daily
    - cron: '0 10 * * 1'   # Weekly Monday
```

### For Large Organizations (50+ people)

```yaml
env:
  # Dedicated channels per team
  SLACK_TEAM_A_CHANNEL: '#team-a-todos'
  SLACK_TEAM_B_CHANNEL: '#team-b-todos'
  SLACK_CRITICAL_CHANNEL: '#engineering-critical'
  SLACK_METRICS_CHANNEL: '#engineering-metrics'
  
  # Smart mentions based on CODEOWNERS
  USE_CODEOWNERS_MENTIONS: true
  MENTION_ON_CRITICAL: true
  
  # Multiple report types
on:
  schedule:
    - cron: '0 9 * * 1-5'   # Daily summaries
    - cron: '0 10 * * 1'    # Weekly team reports
    - cron: '0 14 * * 1'    # Weekly executive report
```

---

## 📚 Additional Resources

- [Slack API Documentation](https://api.slack.com)
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
- [GitHub Actions - Slack Action](https://github.com/slackapi/slack-github-action)
- [Best Practices for Slack Bots](https://api.slack.com/best-practices)

---

## 🆘 Support

If you encounter issues not covered here:

1. **Check workflow logs** in GitHub Actions tab
2. **Verify Slack App configuration** at api.slack.com/apps
3. **Test with manual trigger** (workflow_dispatch)
4. **Create a test notification** to isolate the issue

---

## ✅ Quick Checklist

Before deploying to production:

- [ ] Slack App created and configured
- [ ] Required OAuth scopes granted
- [ ] Bot token stored in GitHub Secrets
- [ ] Bot invited to all required channels
- [ ] Test notification sent successfully
- [ ] Channel names/IDs verified
- [ ] Notification schedule configured
- [ ] Team informed about new notifications
- [ ] Monitoring/alerting set up
- [ ] Documentation shared with team

---

**Last Updated:** 2025-01-17  
**Version:** 2.0 (Expert Edition)
