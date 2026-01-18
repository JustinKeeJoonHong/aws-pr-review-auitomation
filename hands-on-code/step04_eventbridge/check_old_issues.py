import json
import boto3
from datetime import datetime, timezone

# Initialize DynamoDB and SNS clients
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns', region_name='us-west-2')

# Destination phone number for SNS notifications
phone_number = "+82010xxxxxxxx"

# Target DynamoDB table
table = dynamodb.Table('GitHubEvent')

def lambda_handler(event, context):
    """
    Lambda function triggered by EventBridge on a fixed schedule.
    Scans DynamoDB for GitHub Issues that have been open longer than
    a configured threshold and sends an SNS notification if found.
    """
    try:
        # Current time (UTC, Unix timestamp)
        now = int(datetime.now(timezone.utc).timestamp())

        # Threshold: 10 minutes ago (can be adjusted)
        ten_minutes_ago = now - 600

        # Scan DynamoDB for old open issues
        response = table.scan(
            FilterExpression="created_timestamp <= :timestamp AND #act = :open AND #evt = :issues",
            ExpressionAttributeValues={
                ":timestamp": ten_minutes_ago,
                ":open": "opened",
                ":issues": "issues"
            },
            ExpressionAttributeNames={
                "#act": "action",
                "#evt": "event_type"
            },
        )

        print("Current timestamp (UTC):", now)
        print("Threshold timestamp (10 minutes ago):", ten_minutes_ago)

        old_issues = response.get("Items", [])
        issue_count = len(old_issues)

        print(f"Found {issue_count} old issues (10 minutes or older).")

        # Send SMS notification if at least one old issue exists
        if issue_count >= 1:
            message = f"⚠️ {issue_count} old issues found! Check them here:\n"

            # Include up to 3 issue links in the message
            for issue in old_issues[:3]:
                message += f"- {issue['title']}: {issue['url']}\n"

            sns_client.publish(
                PhoneNumber=phone_number,
                Message=message,
            )

            print("SNS notification sent successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps(f"{issue_count} old issues checked.")
        }

    except Exception as e:
        print("Error checking old issues:", e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error checking issues")
        }
