# <img src="https://github.com/kinnik7/SFDX-Logs/blob/master/static/salesforce_icon.ico" title="" alt="" data-align="center"> SFDX Logs

SFDX-Logs is a Python-based tool for managing logs in Salesforce DX (SFDX) projects.

## Features

- Fetch logs from Salesforce DX projects. 
- Enable/disable debug logs for specific user IDs.

## Requirements

- Python 3.x

- Salesforce org

- Salesforce user enable to connect via API

- Salesforce connected app

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kinnik7/SFDX-Logs.git
```

2. Navigate to the project directory:

```bash
cd SFDX-Logs
```

3. Install the requirements:

```bash
pip install -r requirements.txt
```

## Usage

### Configuration

Before performing any action you need to setup `\static\cred.json` file:

1. You can find it in this directory: 

```bash
cd SFDX-Logs/cred.json
```

2. Open end edit the `\static\cred.json` file:

```json
{
    "ENV NAME1": {
        "username": "username@salesforce.dev",
        "password": "user_password",
        "token": "user_token",
        "clientId": "connected_app_client_id",
        "secret_key": "connected_app_secret_key",
        "base_url": "https://yourbaseurl--dev"
    },
    "ENV NAME2": {
        "username": "username@salesforce.dev",
        "password": "user_password",
        "token": "user_token",
        "clientId": "connected_app_client_id",
        "secret_key": "connected_app_secret_key",
        "base_url": "https://yourbaseurl--dev"
    }
}
```

## How to use it?

You can find the **SFDX Logs.exe** file in the current path: `\dist\`

In the main window, you can select an environment or create a new one:

<img src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/main.JPG" title="" alt="" data-align="center">

Clicking the "New Environment" button allows you to configure a new environment in the `\static\cred.json` file:

<img src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/newEnvironment.JPG" title="" alt="" data-align="center">

After saving, the new environment will be available in the dropdown menu.

Once the configuration is completed and the correct environment is selected by clicking the **"Submit"** button, a new window will appear:

<img src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/enableLogs.JPG" title="" alt="" data-align="center">

In this window, you can enter the information to enable the log, including:

- Debug level

- Hour/s to add at the current time

- User ids

If you don't have the list of IDs that you want to enable, you can click the **"Show Users"** button to open a new window:

<img title="" src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/showUsersJPG.JPG" alt="" data-align="center">

In this window, you can select and copy the IDs you prefer, and paste them into the textbox separated by commas (", ").

Once all these steps are completed correctly, a new window will appear:

<img src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshot/success.JPG" title="" alt="" data-align="center">


