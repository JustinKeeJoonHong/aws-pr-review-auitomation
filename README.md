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

![Architecture Diagram](./architecture/pr-review-auto-architecture.png)

### Key Components

- **GitHub Webhooks**  
  Captures pull request and issue events and triggers the backend workflow.

- **Amazon API Gateway**  
  Serves as the entry point for incoming webhook events.

- **AWS Lambda (Python — Ingestion)**  
  Normalizes incoming webhook payloads and persists pull request and issue events into DynamoDB.

- **Amazon DynamoDB**  
  Acts as the central event store (source of truth) for pull request and issue states and metadata.

- **DynamoDB Streams (CDC)**  
  Emits change events from DynamoDB and enables asynchronous fan-out processing.

- **AWS Lambda (Python — Stream Consumer)**  
  Consumes DynamoDB Stream events to invoke Amazon Bedrock and publish notifications via SNS.

- **Amazon Bedrock**  
  Generates LLM-based pull request summaries and review comments.

- **Amazon EventBridge**  
  Periodically evaluates stale pull requests or issues and triggers reminder workflows.

- **Amazon SNS**  
  Sends automated review comments and reminder notifications to reviewers.

## Hands-on Walkthrough

The following hands-on sessions document how each part of the system
was implemented step by step, from webhook ingestion to scheduled
reminder workflows.

1. **Webhook Ingestion**  
   GitHub → API Gateway → Lambda  
   👉 [01 – Webhook Ingestion](./hands-on/01-webhook-ingestion.md)

2. **Event Storage & Stream Processing**  
   DynamoDB persistence and CDC via DynamoDB Streams  
   👉 [02 – DynamoDB Streams](./hands-on/02-dynamodb-stream.md)

3. **Automated Code Review with Bedrock**  
   LLM-based PR analysis, GitHub comments, and notifications  
   👉 [03 – Bedrock Code Review](./hands-on/03-bedrock-review.md)

4. **Scheduled Issue Monitoring**  
   EventBridge-based scanning and reminder notifications  
   👉 [04 – EventBridge Issue Scanner](./hands-on/04-eventbridge-reminder.md)

## Workflow

1. A pull request or issue event is received via GitHub Webhooks.
2. API Gateway forwards the event to an ingestion Lambda (Python).
3. The ingestion Lambda normalizes the payload and stores it in DynamoDB (event store).
4. DynamoDB Streams (CDC) emits change records for downstream processing.
5. Stream consumer Lambda(s) call Amazon Bedrock to generate summaries/comments when needed.
6. Stream consumer Lambda(s) publish notifications via SNS.
7. EventBridge runs scheduled checks for stale items.
8. Reminder workflows are triggered and notifications are sent via SNS.

## My Role

- Designed the event-driven serverless architecture
- Implemented webhook ingestion and event persistence logic
- Designed CDC-based fan-out processing using DynamoDB Streams
- Integrated Amazon Bedrock for LLM-based summaries and review comments
- Built scheduled reminder workflows using EventBridge and SNS
- Documented system architecture and operational workflows

## Impact

- Accelerated pull request review cycles by automating LLM-based summaries and review comments
- Reduced long-unattended pull requests through scheduled detection and reminder workflows
- Improved reviewer awareness while minimizing notification noise via event-driven design

## Hands-on Practice & Validation

This system was designed and validated through an official AWS hands-on practice
focused on DynamoDB-based event modeling and stream processing.

### AWS Hands-on Session

- Practice: AWS Cloud Deep Dive
- Link: https://acc.awskorea.kr/

> Note: The hands-on practice documentation is written in Korean.
> For English readers, please use your browser’s built-in
> "Translate to English" feature after opening each session page.

### What Was Practiced

- Modeling event data in DynamoDB as a source of truth
- Using DynamoDB Streams (CDC) to trigger downstream processing
- Designing asynchronous fan-out workflows
- Evaluating time-based conditions for follow-up actions

### How It Maps to This Project

- Pull request and issue events are stored as immutable records in DynamoDB
- DynamoDB Streams are used to decouple ingestion from processing
- Stream consumers trigger LLM-based analysis and notifications
- Scheduled evaluations for stale items are handled via EventBridge

> Note: Source code is not publicly available as this project was developed
> as part of an internal AWS hands-on session. This repository focuses on
> architecture, system design, and execution details.
