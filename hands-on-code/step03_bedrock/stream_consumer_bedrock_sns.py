import boto3
import json
import requests
import os
import time

# Destination phone number for SNS notifications
phone_number = "+82010********"

# Create Bedrock Runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

# Create SNS client
sns_client = boto3.client('sns', region_name='us-west-2')

# GitHub API authentication header
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def generate_code_review(code_diff):
    """
    Generate a code review using Amazon Bedrock (Claude 3 Haiku).
    """
    prompt = (
        "Human: You are a senior software engineer performing a code review. "
        "Please analyze the following code changes and provide a detailed review. "
        "Please write the review in Korean.\n"
        "Focus on the following aspects:\n"
        "- Code readability (naming, structure, comments)\n"
        "- Performance (time and space complexity)\n"
        "- Security considerations\n"
        "- Best practices (Python PEP8, AWS best practices)\n"
        "- Improvement suggestions with example code if applicable.\n\n"
        f"Code changes:\n{code_diff}\n\nAssistant:"
    )

    request = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "temperature": 0.3,
        "top_k": 250,
        "top_p": 0.999,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
    })

    try:
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=request,
        )
        raw_body = response["body"].read().decode("utf-8")
        return json.loads(raw_body).get("content", [{}])[0].get(
            "text", "Code review generation failed."
        )
    except Exception as e:
        print("Error invoking Bedrock:", e)
        return "Code review generation failed."

def post_github_pr_comment(repo, pr_number, review_text):
    """
    Post a code review comment to a GitHub Pull Request.
    """
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = {"body": review_text}

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        print("Successfully posted code review comment to GitHub PR.")
    else:
        print(f"Failed to post PR comment: {response.status_code}")
        print(response.json())

def send_sns_notification(message):
    """
    Send an SMS notification via Amazon SNS.
    """
    try:
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        print("SNS notification sent successfully:", response)
    except Exception as e:
        print("Failed to send SNS notification:", e)

def process_pull_request(payload):
    """
    Process a Pull Request event and trigger code review if applicable.
    """
    repository = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]
    pr_title = payload["pull_request"]["title"]
    pr_url = payload["pull_request"]["html_url"]
    sender = payload["pull_request"]["user"]["login"]
    action = payload["action"]
    diff_url = payload["pull_request"]["diff_url"]

    if action != "opened":
        print(f"Skipping PR action '{action}'. Code review is only performed on PR creation.")
        return {
            "statusCode": 200,
            "body": f"Skipped code review for PR action: {action}"
        }

    diff_response = requests.get(diff_url)
    code_diff = diff_response.text

    review_text = generate_code_review(code_diff)
    post_github_pr_comment(repository, pr_number, review_text)

    message = (
        f"A new Pull Request has been opened by {sender} in {repository}.\n"
        f"Title: {pr_title}\n"
        f"URL: {pr_url}\n"
        "An automated code review has been completed using Amazon Bedrock."
    )
    send_sns_notification(message)

    return {
        "statusCode": 200,
        "body": f"SNS notification sent for PR: {pr_title}"
    }

def lambda_handler(event, context):
    """
    Lambda handler triggered by DynamoDB Streams.
    """
    print("Received DynamoDB Stream event.")

    for record in event["Records"]:
        event_name = record["eventName"]

        if event_name not in ("INSERT", "MODIFY"):
            print(f"Skipping unsupported event type: {event_name}")
            continue

        new_image = record["dynamodb"].get("NewImage", {})
        event_type = new_image.get("event_type", {}).get("S")
        item_id = new_image.get("id", {}).get("S")

        if not item_id:
            print("Item ID is missing. Skipping record.")
            continue

        if event_type == "pull_request":
            repository = new_image["repository"]["S"]
            pr_number = int(new_image["number"]["N"])
            pr_title = new_image["title"]["S"]
            pr_url = new_image["url"]["S"]
            sender = new_image["sender"]["S"]
            action = new_image["action"]["S"]
            diff_url = new_image["diff_url"]["S"]

            payload = {
                "repository": {"full_name": repository},
                "pull_request": {
                    "number": pr_number,
                    "title": pr_title,
                    "html_url": pr_url,
                    "user": {"login": sender},
                    "diff_url": diff_url
                },
                "action": action
            }

            process_pull_request(payload)

        else:
            print(f"Unsupported event_type: {event_type}")

    return {
        "statusCode": 200,
        "body": "DynamoDB Stream processing completed successfully."
    }
