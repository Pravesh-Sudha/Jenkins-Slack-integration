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
