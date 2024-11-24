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
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time

# In my case, I am running Jenkins on my host machine on port 8080. That's why its URL is localhost 

JENKINS_USER = "<your-jenkins-user>"  # Mostly its admin
JENKINS_URL = "http://localhost:8080/job/<job-name>/build"
JENKINS_API_TOKEN = "<your-jenkins-token>"
BUILD_STATUS_URL = "http://localhost:8080/job/<Job-name>/lastBuild/api/json"

SLACK_CHANNEL = "#devops-updates"
SLACK_BOT_TOKEN = "<your-slack-bot-token>"

def trigger_pipeline():
    print("Triggering the Pipeline....")
    response = requests.post(
        url=JENKINS_URL,auth=(JENKINS_USER, JENKINS_API_TOKEN),
    )
    if response.status_code == 201:
        print("Triggered Pipeline Successfully!!")
    else:
        print(f"Failed to trigger Pipeline, response's status code: {response.status_code}")
        response.raise_for_status()


def get_build_status():
    print("Checking Build info....")
    while True:
        response = requests.get(BUILD_STATUS_URL, auth= (JENKINS_USER, JENKINS_API_TOKEN),
                                )
        if response.status_code == 200:
            build = response.json()
            status = build.get('result')
            if status:
                return status
            else:
                print("Build in progress....")
                time.sleep(10)
        else:
            print(f"Failed to fetch build details! Response's status Code: {response.status_code}")
            response.raise_for_status()


def send_slack_notification(status):
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        message = f"Pipeline Completed with status: *{status}* 🚀"
        response = client.chat_postMessage(channel= SLACK_CHANNEL, text= message)
        print(f"Slack notification sent: {response['message']['text']}")
    except Exception as e:
        print(f"Slack notification failed, error: {e}")


if __name__ == "__main__":
    try:
        trigger_pipeline()
        status = get_build_status()
        send_slack_notification(status)
    except Exception as e:
        print(f"Error: {e}") 
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
