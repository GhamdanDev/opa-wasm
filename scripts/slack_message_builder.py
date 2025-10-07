#!/usr/bin/env python3
"""
Slack Message Builder - Helper script for creating rich Slack messages

This script demonstrates how to build professional Slack messages with Block Kit
for your TODO notifications. Use this as a reference or integrate into your workflow.

Author: DevOps Team
Version: 1.0
"""

import json
from typing import List, Dict, Any
from datetime import datetime


class SlackMessageBuilder:
    """Build rich Slack messages using Block Kit"""
    
    # Color constants
    COLORS = {
        'critical': '#FF0000',
        'high': '#FF6B00',
        'medium': '#FFD700',
        'low': '#00AA00',
        'info': '#0099FF',
        'success': '#28A745'
    }
    
    # Emoji mapping
    EMOJIS = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢',
        'bug': '🐛',
        'fixme': '🔧',
        'hack': '⚠️',
        'todo': '📝',
        'note': '📌'
    }
    
    def __init__(self):
        self.blocks: List[Dict[str, Any]] = []
        
    def add_header(self, text: str) -> 'SlackMessageBuilder':
        """Add a header block"""
        self.blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": True
            }
        })
        return self
    
    def add_section(self, text: str, fields: List[str] = None) -> 'SlackMessageBuilder':
        """Add a section block with optional fields"""
        block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
        
        if fields:
            block["fields"] = [
                {"type": "mrkdwn", "text": field}
                for field in fields
            ]
        
        self.blocks.append(block)
        return self
    
    def add_divider(self) -> 'SlackMessageBuilder':
        """Add a divider line"""
        self.blocks.append({"type": "divider"})
        return self
    
    def add_button(self, text: str, url: str, style: str = None) -> 'SlackMessageBuilder':
        """Add an action button"""
        button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": True
            },
            "url": url
        }
        
        if style in ['primary', 'danger']:
            button["style"] = style
        
        # Check if we already have an actions block
        if self.blocks and self.blocks[-1].get("type") == "actions":
            self.blocks[-1]["elements"].append(button)
        else:
            self.blocks.append({
                "type": "actions",
                "elements": [button]
            })
        
        return self
    
    def add_context(self, text: str) -> 'SlackMessageBuilder':
        """Add a context block (small gray text at bottom)"""
        self.blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": text
                }
            ]
        })
        return self
    
    def build(self, fallback_text: str = None) -> Dict[str, Any]:
        """Build the final message payload"""
        payload = {
            "text": fallback_text or "New notification",
            "blocks": self.blocks
        }
        return payload
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.build(), indent=indent)


def create_critical_alert(repo: str, branch: str, critical_count: int, high_count: int, 
                         issue_url: str, repo_url: str, workflow_url: str) -> Dict[str, Any]:
    """
    Create a critical alert message
    
    Example:
        msg = create_critical_alert(
            repo="owner/repo",
            branch="main",
            critical_count=3,
            high_count=5,
            issue_url="https://github.com/owner/repo/issues",
            repo_url="https://github.com/owner/repo",
            workflow_url="https://github.com/owner/repo/actions/runs/123"
        )
    """
    builder = SlackMessageBuilder()
    
    builder.add_header("🚨 Critical TODOs Require Immediate Attention")
    
    builder.add_section(
        f"*Repository:* {repo}\n*Branch:* {branch}",
        fields=[
            f"*Critical Count:*\n{critical_count} 🔴",
            f"*High Priority:*\n{high_count} 🟠"
        ]
    )
    
    builder.add_section(
        "<!channel> *Action required:* Critical issues (FIXME/BUG) have been detected in the codebase. "
        "Please review and address these items as soon as possible."
    )
    
    builder.add_button("View Critical Issues", issue_url, style="danger")
    builder.add_button("View Repository", repo_url)
    builder.add_button("View Workflow Run", workflow_url)
    
    builder.add_context(
        f"Triggered by workflow run • {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
    
    return builder.build(fallback_text="🚨 CRITICAL TODOs DETECTED 🚨")


def create_daily_summary(repo: str, critical: int, high: int, medium: int, low: int,
                        all_issues_url: str, critical_url: str, dashboard_url: str) -> Dict[str, Any]:
    """
    Create a daily summary report
    
    Example:
        msg = create_daily_summary(
            repo="owner/repo",
            critical=2,
            high=5,
            medium=10,
            low=3,
            all_issues_url="https://github.com/owner/repo/issues",
            critical_url="https://github.com/owner/repo/issues?q=label:critical",
            dashboard_url="https://github.com/owner/repo/blob/main/.github/TODO_DASHBOARD.md"
        )
    """
    builder = SlackMessageBuilder()
    
    total = critical + high + medium + low
    
    builder.add_header("📊 Daily TODO Summary Report")
    
    builder.add_section(
        f"*Repository:* {repo}\n*Date:* {datetime.now().strftime('%Y-%m-%d')}"
    )
    
    builder.add_divider()
    
    builder.add_section("*TODO Breakdown by Priority:*")
    
    builder.add_section(
        "",
        fields=[
            f"🔴 *Critical:* {critical}",
            f"🟠 *High:* {high}",
            f"🟡 *Medium:* {medium}",
            f"🟢 *Low:* {low}"
        ]
    )
    
    builder.add_section(f"*Total TODOs:* `{total}`")
    
    builder.add_divider()
    
    builder.add_button("📋 View All Issues", all_issues_url)
    builder.add_button("🔴 Critical Only", critical_url, style="danger")
    builder.add_button("📊 Dashboard", dashboard_url)
    
    builder.add_context(
        f"🤖 Automated report • Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
    
    return builder.build(fallback_text=f"📊 Daily TODO Summary - {repo}")


def create_weekly_metrics(repo: str, created: int, closed: int, resolution_rate: int,
                         issues_url: str) -> Dict[str, Any]:
    """
    Create a weekly metrics report
    
    Example:
        msg = create_weekly_metrics(
            repo="owner/repo",
            created=15,
            closed=20,
            resolution_rate=133,
            issues_url="https://github.com/owner/repo/issues"
        )
    """
    builder = SlackMessageBuilder()
    
    net_change = created - closed
    trend_emoji = "📉" if net_change < 0 else "📈" if net_change > 0 else "➡️"
    
    builder.add_header("📈 Weekly TODO Performance Metrics")
    
    builder.add_section(
        f"*Repository:* {repo}\n*Period:* Last 7 days"
    )
    
    builder.add_divider()
    
    builder.add_section("*This Week's Activity:*")
    
    builder.add_section(
        "",
        fields=[
            f"📝 *Created:*\n{created} new TODOs",
            f"✅ *Resolved:*\n{closed} TODOs",
            f"📊 *Resolution Rate:*\n{resolution_rate}%",
            f"🎯 *Net Change:*\n{net_change} TODOs {trend_emoji}"
        ]
    )
    
    # Add interpretation
    if resolution_rate >= 100:
        message = "🎉 *Great job!* You're resolving more TODOs than you're creating!"
        color = "success"
    elif resolution_rate >= 80:
        message = "👍 *Good progress!* Keep up the momentum."
        color = "info"
    else:
        message = "⚠️ *Attention needed:* TODOs are accumulating faster than they're being resolved."
        color = "medium"
    
    builder.add_section(message)
    
    builder.add_context(
        "💡 *Tip:* Aim for a resolution rate > 100% to reduce technical debt over time"
    )
    
    builder.add_button("View All TODOs", issues_url)
    
    return builder.build(fallback_text=f"📈 Weekly TODO Metrics - {repo}")


def create_test_notification() -> Dict[str, Any]:
    """Create a simple test notification"""
    builder = SlackMessageBuilder()
    
    builder.add_section(
        "✅ *Slack Integration Test Successful!*\n\n"
        "Your Slack notifications are configured correctly and working as expected."
    )
    
    builder.add_context(
        f"Test notification • Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
    
    return builder.build(fallback_text="🧪 Test Notification")


# Example usage
if __name__ == "__main__":
    print("=== Slack Message Builder Examples ===\n")
    
    # Example 1: Critical Alert
    print("1. Critical Alert Message:")
    print("-" * 50)
    msg = create_critical_alert(
        repo="owner/awesome-project",
        branch="main",
        critical_count=3,
        high_count=5,
        issue_url="https://github.com/owner/repo/issues?q=label:critical",
        repo_url="https://github.com/owner/repo",
        workflow_url="https://github.com/owner/repo/actions/runs/123456"
    )
    print(json.dumps(msg, indent=2))
    print("\n")
    
    # Example 2: Daily Summary
    print("2. Daily Summary Message:")
    print("-" * 50)
    msg = create_daily_summary(
        repo="owner/awesome-project",
        critical=2,
        high=5,
        medium=10,
        low=3,
        all_issues_url="https://github.com/owner/repo/issues",
        critical_url="https://github.com/owner/repo/issues?q=label:critical",
        dashboard_url="https://github.com/owner/repo/blob/main/.github/TODO_DASHBOARD.md"
    )
    print(json.dumps(msg, indent=2))
    print("\n")
    
    # Example 3: Weekly Metrics
    print("3. Weekly Metrics Message:")
    print("-" * 50)
    msg = create_weekly_metrics(
        repo="owner/awesome-project",
        created=15,
        closed=20,
        resolution_rate=133,
        issues_url="https://github.com/owner/repo/issues"
    )
    print(json.dumps(msg, indent=2))
    print("\n")
    
    # Example 4: Test Notification
    print("4. Test Notification:")
    print("-" * 50)
    msg = create_test_notification()
    print(json.dumps(msg, indent=2))
    print("\n")
    
    # Example 5: Custom message using builder
    print("5. Custom Message Using Builder:")
    print("-" * 50)
    custom = (SlackMessageBuilder()
              .add_header("🎯 Custom TODO Alert")
              .add_section("This is a custom message with multiple features:")
              .add_section("", fields=[
                  "*Field 1:* Value 1",
                  "*Field 2:* Value 2",
                  "*Field 3:* Value 3",
                  "*Field 4:* Value 4"
              ])
              .add_divider()
              .add_button("Action 1", "https://example.com/1", style="primary")
              .add_button("Action 2", "https://example.com/2")
              .add_context("Created with SlackMessageBuilder")
              .build(fallback_text="Custom TODO Alert"))
    
    print(json.dumps(custom, indent=2))
