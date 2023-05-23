import src as lib


class Connection:
    def __init__(self):
        self.env = None
        self.response = None

    def get_connection(self):
        credentials = self.get_credentials()
        base_url = credentials.get('base_url')
        # Login with the credentials in cred.json
        payload = {
            'grant_type': 'password',
            'client_id': credentials.get('clientId'),
            'client_secret': credentials.get('secret_key'),
            'username': credentials.get('username'),
            'password': credentials.get('password') + credentials.get('token')
        }
        try:
            response = lib.requests.post(base_url + '.my.salesforce.com/services/oauth2/token', data=payload)
            if response.status_code != 200:
                error_message = f"[{lib.datetime.now().replace(microsecond=0)}] - Error while connecting user '{credentials.get('username')}': {response.content}\n\n"
                lib.messagebox.showerror("Error", error_message)
            elif response.status_code == 200:
                print("Connection established")

            access_token = response.json()['access_token']
            instance_url = response.json()['instance_url']

            # Set the headers with the obtained access_token
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json'
            }

            response = {
                "instance_url": instance_url,
                "headers": headers,
                "access_token": access_token,
                "credentials": credentials,
            }

            self.response = response
            return response
        except Exception as e:
            error_message = f"[{lib.datetime.now().replace(microsecond=0)}] - Error while connecting to the org: {str(e)}\n\n"
            lib.messagebox.showerror("Error", error_message)
            return

    def get_credentials(self):
        with open('../cred.json') as config_file:
            config = lib.json.load(config_file)
        return config.get(self.env, {})

    def set_environment(self, environment):
        self.env = environment
