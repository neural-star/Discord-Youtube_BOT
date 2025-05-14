# Discord-Youtube_BOT
This bot can send new youtube video!

This project uses a Google Cloud service account key to access the API. Follow the steps below to obtain google_cloud.json.

# 1. Access the Google Cloud Console 
Log in to the Google Cloud Console.

Select an existing project or create a new project.

# 2. Create a Service Account 
From the left menu, select "IAM and Administration" → "Service Accounts".

Click on "Create Service Account.

Enter a name (e.g., my-service-account) and description.

Assign the required roles (e.g., Cloud Translation API User, Editor, etc.).

Complete the creation.

# 3. Generate Key File (JSON) 
Select the appropriate account from the list of service accounts created and go to the "Keys" tab.

Click "Add Key" → "Create New Key.

Select "JSON" as the key type and "Create".

A .json file will be automatically downloaded (e.g. google_cloud.json).
Overwrite google_cloud.json in this repository with the downloaded JSON file.This project uses a Google Cloud service account key to access the API. Follow the steps below to obtain google_cloud.json.

![image](https://github.com/user-attachments/assets/56a0d601-357d-4d87-a71b-aa4ce154fd3f)

Copy the channel id as shown in this image and paste it into YOUTUBE_CHANNEL_ID in main.py.
