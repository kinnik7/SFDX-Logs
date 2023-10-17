# <img src="https://github.com/kinnik7/SFDX-Logs/blob/master/static/salesforce_icon.ico" title="" alt="" data-align="center" width="100" height="100"> SFDX Logs

SFDX-Logs is a Python-based tool for managing logs in Salesforce (SFDX) projects.

## Features

- Connect to different environments.

- Enable debug logs for specific user IDs.

## Requirements

- Python 3.x

- Salesforce org

- Salesforce user enable to connect via API

- Salesforce connected app

### Download

Click this link to download the source code: [Download SFDX Logs.zip](https://github.com/kinnik7/SFDX-Logs/archive/refs/heads/master.zip)

## Installation

### Windows

1. Download the `SFDX Logs.zip` file
2. Extract `SFDX-Logs-master` folder and save it in local.
3. Move to `\dist\` folder
4. Right click on `SFDX Logs.exe` file and click on "**Sent to Desktop (create shortcut)**"
5. Move to `\Desktop`
6. Run the application

### MacOs, Linux and other systems
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

4. Run this command from terminal:

```bash
pyinstaller --noconsole --onefile --icon='.\static\salesforce_icon.ico' '.\SFDX Logs.py'
```

5. A new file will appear in `\dist\` folder, open it and enjoy


6. You can also run the main with this comand:

```bash
python 'SFDX Logs.py'
```


## Configuration

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

- Select, create or delete a Debug level

- Hour/s to add at the current time

- User ids

- Change the selected environment

- Delete all the log files in the environment

By clicking on the **"Change Environment"** button the current window will be closed and the main window will appear.

By clicking on the **"New Debug Level"** button, a new window will appear:

<img src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/newDebugLevel.JPG" title="" alt="" data-align="center">

Otherwise, to delete a debug level, just select a debug level from dropdown list and then click on **"Delete Debug Level"** and a new window will appear:

<img src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/deleteDebuglevel.JPG" title="" alt="" data-align="center">

If you don't have the list of IDs that you want to enable, you can click the **"Show Users"** button to open a new window:

<img title="" src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/showUsersJPG.JPG" alt="" data-align="center">

In this window, you can select and copy the IDs you prefer, and paste them into the textbox separated by commas (", ").

Once all these steps are completed correctly, a new window will appear:

<img src="https://github.com/kinnik7/SFDX-Logs/blob/master/screenshots/success.JPG" title="" alt="" data-align="center">
