import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    try:
        # Initialize DynamoDB resource and target table
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('GitHubEvent')

        # Parse GitHub webhook payload
        body = json.loads(event['body'])
        event_type = event['headers'].get('x-github-event')

        # Generate a Unix timestamp for sorting and tracking
        created_timestamp = int(
            datetime.fromisoformat(
                datetime.utcnow().isoformat().replace("Z", "+00:00")
            ).timestamp()
        )

        # Generate a unique item ID based on event type
        if event_type == 'pull_request':
            item_id = f"pr_{body['pull_request']['id']}"
        elif event_type == 'issues':
            item_id = f"issue_{body['issue']['id']}"
        else:
            raise ValueError(f"Unsupported event type: {event_type}")

        # Check if an item with the same ID already exists
        try:
            existing_item = table.get_item(Key={'id': item_id})
        except Exception:
            existing_item = {'Item': None}

        print("Parsed webhook body:", body)

        # Common attributes shared by all event types
        base_item = {
            'id': item_id,
            'event_type': event_type,
            'action': body['action'],
            'last_updated_at': datetime.utcnow().isoformat(),
            'repository': body['repository']['full_name'],
            'sender': body['sender']['login'],
            'created_timestamp': created_timestamp
        }

        # Preserve the original creation time if the item already exists
        if 'Item' in existing_item and existing_item['Item']:
            base_item['created_at'] = existing_item['Item']['created_at']
        else:
            base_item['created_at'] = datetime.utcnow().isoformat()

        # Handle Pull Request events
        if event_type == 'pull_request':
            pr = body['pull_request']
            item = {
                **base_item,
                'number': pr['number'],
                'title': pr['title'],
                'url': pr['html_url'],
                'assignee': pr['user']['login'],
                'organization': body.get('organization', {}).get('login'),
                'diff_url': pr['diff_url']
            }

        # Handle Issue events
        elif event_type == 'issues':
            issue = body['issue']
            item = {
                **base_item,
                'number': issue['number'],
                'title': issue['title'],
                'url': issue['html_url'],
                'assignee': issue['assignee']['login'] if issue['assignee'] else None
            }

        # Store the event in DynamoDB
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully processed GitHub webhook',
                'event_type': event_type,
                'id': item['id']
            })
        }

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing webhook',
                'error': str(e)
            })
        }
