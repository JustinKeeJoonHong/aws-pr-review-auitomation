# Step 3 – Use Bedrock to Automatically Write Code Reviews for PRs

![](./images/0301.png)

In this step, we use Amazon Bedrock to automatically generate code reviews
for GitHub Pull Requests and post them as PR comments.
We also send SMS notifications using Amazon SNS.

---

## Goal

- Request access to an Amazon Bedrock model
- Generate automated code reviews for Pull Requests
- Post code review comments to GitHub
- Send SMS notifications when a PR is reviewed

---

## Prerequisites

- Completed **Step 2 – DynamoDB Streams**
- AWS Region set to **us-west-2**
- A public GitHub repository

> ✅ Before practicing, make sure your AWS Console is set to the **us-west-2** region.

---

## Step 1. Request Access to a Bedrock Model

Search for **Amazon Bedrock** in the AWS Console and open it.

![](./images/0302.png)

Scroll down to the **Foundation models** section.
Under **Available to request**, hover over the model and click  
**Request model access**.

![](./images/0303.png)

---

### Select Claude 3 Haiku

Scroll down to the **Anthropic** section.
Under **Claude 3 Haiku**, click **Available to request** and then  
**Request model access**.

![](./images/0304.png)

You will be redirected to the **Edit model access** page.
Scroll down and click **Next**.

![](./images/0305.png)
![](./images/0306.png)

On the **Review and submit** page, confirm that **Claude 3 Haiku**
is selected and click **Submit**.

![](./images/0307.png)

After a short time, you should see **Access granted**.

![](./images/0308.png)
![](./images/0309.png)

---

## Step 2. Configure Amazon SNS for SMS Notifications

Search for **SNS** in the AWS Console.

Open the sidebar menu and select  
**Text messaging (SMS)**.

![](./images/0310.png)

Scroll down to **Sandbox destination phone numbers**
and click **Add phone number**.

![](./images/0311.png)

Enter your phone number in the format:

- `+1xxxxxxxxxx`

Select **English (United States)** as the verification language
and click **Add phone number**.

![](./images/0312.png)

Enter the verification code you received and click **Verify phone number**.

![](./images/0313.png)

Confirm that the **Verification status** is **Verified**.

![](./images/0314.png)

---

## Step 3. Update StreamConsumer Lambda Logic

Return to **AWS Lambda → StreamConsumer**.

Paste the provided code into the code editor  
and update the required values.

- [`stream_consumer_bedrock_sns.py`](../hands-on-code/step03_bedrock/stream_consumer_bedrock_sns.py)

Click **Deploy**.

![](./images/0315.png)

---

## Step 4. Add Requests Library Using Lambda Layers

The Lambda logic requires an external library.
To support this, we will add a **Lambda Layer**.

In the **StreamConsumer** Lambda page, click **Layers**.

![](./images/0316.png)

Scroll down and click **Add a layer**.

![](./images/0317.png)

On the next page, click **Create a new layer**.

![](./images/0318.png)

---

### Create the Layer

Download the required library archive using the link below.

- **Download layer.zip**

Enter the values as shown on the screen,
upload the downloaded zip file, and click **Create**.

![](./images/0319.png)

Open the sidebar and click **Functions**.

![](./images/0320.png)

Select **StreamConsumer**.

![](./images/0321.png)

Click **Layers** again and select **Add a layer**.

![](./images/0322.png)
![](./images/0323.png)

Choose **Custom layers**, select the layer you just created,
and click **Add**.

![](./images/0324.png)

---

## Step 5. Increase Lambda Memory and Timeout

To ensure stable execution, update the Lambda configuration.

Go to **Configuration → General configuration**
and click **Edit**.

![](./images/0325.png)

Set the following values:

- **Memory**: 512 MB
- **Timeout**: 1 minute

Click **Save**.

![](./images/0326.png)

---

## Step 6. Generate a GitHub Token

To post comments on Pull Requests, a GitHub token is required.

Visit the GitHub token creation page.

![](./images/0327.png)

Select only the **repo** permission
and click **Generate token**.

![](./images/0328.png)

Copy the generated token.

![](./images/0329.png)

---

## Step 7. Register the GitHub Token in Lambda

Return to **AWS Lambda → StreamConsumer**.

Go to **Configuration → Environment variables**
and click **Edit**.

![](./images/0330.png)

Add a new variable:

- **Key**: `GITHUB_TOKEN`
- **Value**: (your token)

Click **Save**.

![](./images/0331.png)

---

## Step 8. Create a Pull Request for Testing

Clone the repository and create a new branch.

```bash
git checkout -b feature
```

![](./images/0332.png)

Add a simple file, then commit the changes.

- [`word_count.py`](../hands-on-code/step03_bedrock/word_count.py)

![](./images/0333.png)

Push the branch to GitHub.

```bash
git add .
git commit -m "feat: add word_count.py"
```

![](./images/0334.png)

---

## Step 9. Create a Pull Request

Go back to GitHub.
Click **Compare & pull request**, then click **Create pull request**.

![](./images/0335.png)
![](./images/0336.png)

---

## Step 10. Verify Automated Code Review

After a short time, you should see a code review comment
automatically posted on the Pull Request.

![](./images/0337.png)

Verify that the review content was generated correctly.

![](./images/0338.jpeg)

---

## Result

- Bedrock automatically generates PR code reviews
- Reviews are posted directly to GitHub Pull Requests
- SMS notifications are sent using Amazon SNS
