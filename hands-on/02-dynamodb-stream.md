# Step 2 – Storing GitHub Events Using DynamoDB Streams

![](./images/0201.png)

In this step, we store GitHub webhook events in DynamoDB and enable DynamoDB
Streams to detect data changes in real time.

---

## Goal

- Store GitHub Issue and Pull Request events in DynamoDB
- Verify event persistence
- Enable DynamoDB Streams
- Trigger a Lambda function on data changes

---

## Prerequisites

- Completed **Step 1 – Webhook Ingestion**
- AWS Region set to **us-west-2**

> ✅ Before practicing, make sure your AWS Console is set to the **us-west-2** region.

---

## Step 1. Create a DynamoDB Table

Search for **DynamoDB** in the AWS Console and click **Create table**.

![](./images/0202.png)

Set the following values:

- **Table name**: `GitHubEvent`
- **Partition key**: `id` (String)

Click **Create table**.

![](./images/0203.png)

> ⚠️ The table name must be exactly `GitHubEvent`.

![](./images/0204.png)

---

## Step 2. Grant Lambda Permission to Write to DynamoDB

Go to **AWS Lambda → WebhookToDB**.

Navigate to **Configuration → Permissions**  
Click the **Role name**.

![](./images/0205.png)

---

### Create an Inline Policy

Click **Add permissions → Create inline policy**.

![](./images/0206.png)

Select the **JSON** tab.

![](./images/0207.png)

Paste the policy and click **Next**.

![](./images/0208.png)

Set the policy name to:

- **DB_Write_Only**

Click **Create policy**.

![](./images/0209.png)

---

## Step 3. Deploy Lambda with DynamoDB Integration

Return to the **WebhookToDB** Lambda function.

Paste the provided code into the editor  
and click **Deploy**.

![](./images/0210.png)

---

## Step 4. Verify Data Is Stored in DynamoDB

Go to **GitHub** and create a new **Issue**.

![](./images/0211.png)

Return to **DynamoDB**.

Click **Explore items** and select the `GitHubEvent` table.

![](./images/0212.png)

You should see the issue saved as an item.

![](./images/0213.png)

---

## Step 5. Create a Stream Consumer Lambda Function

Go to **AWS Lambda → Create function**.

![](./images/0214.png)

Set the following values:

- **Function name**: `StreamConsumer`
- **Runtime**: Python 3.13

Click **Create function**.

![](./images/0215.png)

---

## Step 6. Grant Permissions for DynamoDB Streams

In the `StreamConsumer` Lambda function:

Go to **Configuration → Permissions**  
Click the **Role name**.

![](./images/0216.png)

Click **Add permissions → Create inline policy**.

![](./images/0217.png)

Select **JSON** and paste the policy for:

- DynamoDB Streams
- SNS
- Bedrock

![](./images/0218.png)

Click **Next**.

![](./images/0219.png)

Set the policy name to:

- **getStream**

Click **Create policy**.

![](./images/0220.png)

---

## Step 7. Enable DynamoDB Streams

Go to **DynamoDB → Tables → GitHubEvent → Exports and streams**.

![](./images/0221.png)

Click **Turn on** under DynamoDB Streams.

![](./images/0222.png)

Select **New image** and click **Turn on stream**.

![](./images/0223.png)

---

## Step 8. Connect DynamoDB Stream to Lambda

Scroll down and click **Create trigger**.

![](./images/0224.png)

Select **StreamConsumer** as the target Lambda.

![](./images/0225.png)

Verify the trigger is created.

![](./images/0226.png)

---

## Step 9. Verify Stream Processing

Create another **GitHub Issue**.

![](./images/0227.png)

Go to **CloudWatch → Log groups → StreamConsumer**  
and verify that the event payload appears in the logs.

---

## Result

- GitHub events are stored in DynamoDB
- DynamoDB Streams detect changes in real time
- StreamConsumer Lambda is triggered successfully
