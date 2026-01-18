# Automated Pull Request Review & Reminder System

## Overview
Automated GitHub pull request review system that analyzes code changes,
posts LLM-generated summaries and comments, and detects long-unattended
pull requests to send automated reminders.

## Problem
- Code review turnaround time was inconsistent and heavily dependent on reviewer availability
- Some pull requests remained unattended for days, delaying releases
- Manual reminders were noisy and easy to forget

## Architecture
(Architecture diagram will be added here)

## Workflow
1. A pull request is created or updated
2. GitHub Webhook triggers the backend
3. Code diffs are analyzed and summarized
4. Amazon Bedrock generates review comments
5. PR activity timestamps are stored in DynamoDB (TTL enabled)
6. EventBridge detects inactive pull requests
7. SNS sends automated reminders

## Impact
- Accelerated pull request review cycles
- Reduced long-unattended pull requests
- Improved reviewer awareness with minimal noise

## References
- AWS Cloud Deep Dive Hands-on Guide: (link will be added)
- Demo Page: (link will be added)

> Note: Source code is not publicly available as this project was developed
> as part of an internal AWS hands-on session. This repository focuses on
> architecture, system design, and execution details.
