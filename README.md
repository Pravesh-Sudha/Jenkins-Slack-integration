# **Jenkins and Slack Integration with Python**

A Python project demonstrating how to integrate Jenkins with Slack. This program triggers a Jenkins pipeline, fetches the build status, and sends a notification to a Slack channel.

---

## **Features**
- Automates triggering a Jenkins pipeline.
- Fetches build status using the Jenkins API.
- Sends build notifications to Slack channels via a Slack bot.

---

## **Prerequisites**
- Python 3.x installed
- Jenkins installed and running
- Slack workspace access

---

## **Installation Steps**

### **1. Install Jenkins**
1. Download and install Jenkins from the [official site](https://www.jenkins.io/download/).
2. Start Jenkins:
   ```bash
   java -jar jenkins.war
   ```
3. Access Jenkins at [http://localhost:8080](http://localhost:8080).
4. Complete the setup by entering the initial admin password found in `~/.jenkins/secrets/initialAdminPassword`.

### **2. Install Required Plugins**
- Go to **Manage Jenkins** → **Plugins** → Install the following plugins:
  - **Pipeline**
  - **Blue Ocean**

### **3. Create a Hello World Pipeline**
1. Click on **New Item** → Enter a name → Choose **Pipeline**.
2. In the pipeline configuration, use the following script:
   ```groovy
   pipeline {
       agent any
       stages {
           stage('Hello') {
               steps {
                   echo 'Hello, World!'
               }
           }
       }
   }
   ```
3. Save the pipeline.

### **4. Create Jenkins API Token**
1. Go to your profile in Jenkins (click on your username in the top-right).
2. Click on **Configure** → **API Token** → Generate a new token.
3. Copy the token and store it securely.

---

## **Slack Setup**

### **1. Create a Slack Bot**
1. Go to [Slack API](https://api.slack.com/apps) and click **Create New App**.
2. Choose **From Scratch** and give your app a name.
3. Under **OAuth & Permissions**, add the following bot token scopes:
   - `chat:write`
   - `chat:write.public`

### **2. Install the Bot in Your Workspace**
1. Go to the **Install App** section in your Slack app dashboard.
2. Install the app to your workspace.
3. Copy the **Bot User OAuth Token**.

### **3. Create a Slack Channel**
1. Create a channel in Slack (e.g., `#jenkins-notifications`).
2. Invite the bot to the channel:
   ```plaintext
   /invite @<your_bot_name>
   ```

---

## **Python Program Setup**

### **1. Install Required Python Packages**
Install the dependencies:
```bash
pip3 install requests
pip3 install slack_sdk
```

### **2. Create the Python Script**
Save the following Python script as `jenkins_slack_integration.py`:
```python
import requests

# Jenkins setup
jenkins_url = "http://localhost:8080"
job_name = "Jenkins-Python-pipeline"  # Replace with your job name
jenkins_user = "admin"  # Replace with your Jenkins username
jenkins_token = "<your_jenkins_token>"  # Replace with your Jenkins API token

# Slack setup
slack_webhook_url = "https://slack.com/api/chat.postMessage"
slack_bot_token = "<your_slack_bot_token>"  # Replace with your Slack bot token
channel_id = "<your_channel_id>"  # Replace with your channel ID

# Trigger Jenkins Pipeline
print("Triggering the Pipeline....")
trigger_url = f"{jenkins_url}/job/{job_name}/build"
response = requests.post(trigger_url, auth=(jenkins_user, jenkins_token))

if response.status_code == 201:
    print("Triggered Pipeline Successfully!!")
    # Retrieve Build Info
    print("Checking Build info....")
    build_info_url = f"{jenkins_url}/job/{job_name}/lastBuild/api/json"
    build_response = requests.get(build_info_url, auth=(jenkins_user, jenkins_token))
    if build_response.status_code == 200:
        build_info = build_response.json()
        build_status = build_info.get("result", "IN PROGRESS")

        # Send Slack Notification
        payload = {
            "channel": channel_id,
            "text": f"Jenkins Build Status: {build_status}"
        }
        headers = {
            "Authorization": f"Bearer {slack_bot_token}",
            "Content-Type": "application/json"
        }
        slack_response = requests.post(slack_webhook_url, headers=headers, json=payload)
        if slack_response.status_code == 200 and slack_response.json().get("ok"):
            print("Slack Notification Sent Successfully!")
        else:
            print("Slack notification failed, error:", slack_response.json())
    else:
        print("Failed to fetch build info from Jenkins:", build_response.status_code)
else:
    print("Failed to trigger Pipeline, response's status code:", response.status_code)
```

---

## **Running the Program**
Run the Python script:
```bash
python3 jenkins_slack_integration.py
```

---

## **Troubleshooting**

1. **Error: `401 Unauthorized`**
   - Verify the Jenkins username and API token.
   - Ensure the Jenkins user has permissions to trigger the pipeline.

2. **Error: `not_in_channel`**
   - Ensure the bot is invited to the Slack channel using `/invite`.

3. **Error: `CERTIFICATE_VERIFY_FAILED`**
   - Update Python certificates:
     ```bash
     /Applications/Python\ 3.x/Install\ Certificates.command
     ```
   - Or disable SSL verification (not recommended for production).

---

## **Future Improvements**
- Add error handling for Jenkins API failures.
- Support multiple Slack channels and Jenkins jobs.
- Use environment variables to store sensitive information.

---

Feel free to contribute to this project or share your feedback! 😊

---

### **License**
This project is licensed under the MIT License.
