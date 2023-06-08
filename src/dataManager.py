import src as lib


class DataFromSFDC:
    def __init__(self):
        self.response = None

    def set_connection_response(self, response):
        self.response = response

    def get_debug_levels(self):
        if self.response is not None:
            instance_url = self.response.get("instance_url")
            headers = self.response.get("headers")
            try:
                response = lib.requests.get(instance_url + '/services/data/v52.0/tooling/query/?q=SELECT+Id,DeveloperName+FROM+DebugLevel', headers=headers)
                if response.status_code == 200:
                    return response.json().get('records')
            except Exception as e:
                error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError while searching for Debug Levels: {str(e)}"
                lib.messagebox.showerror("Error", error_message)
                return
        else:
            error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during the request, no response returned!"
            lib.messagebox.showerror("Error", error_message)

    def query_user_ids(self):
        if self.response is not None:
            instance_url = self.response.get("instance_url")
            headers = self.response.get("headers")
            try:
                response = lib.requests.get(instance_url + '/services/data/v52.0/query/?q=SELECT+Id,Name+FROM+User+WHERE+isActive=true+ORDER+BY+Name',
                                            headers=headers)
                if response.status_code == 200:
                    return response.json().get('records')
            except Exception as e:
                error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError while searching for Users in orgs: {str(e)}"
                lib.messagebox.showerror("Error", error_message)
                return
        else:
            error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during the request, no response returned!"
            lib.messagebox.showerror("Error", error_message)

    def enable_salesforce_logs(self, add_hours, user_ids, debug_level_id):
        if self.response is not None:
            instance_url = self.response.get("instance_url")
            headers = self.response.get("headers")
            try:
                expiration_date = lib.datetime.utcnow() + lib.timedelta(hours=int(add_hours))
                expiration_date_str = expiration_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                success_users = []
                # Enable logs for the specified users
                for user_id in user_ids:
                    payload = {
                        'TracedEntityId': user_id,
                        'LogType': 'USER_DEBUG',
                        'ExpirationDate': expiration_date_str,
                        'DebugLevelId': debug_level_id
                    }
                    response = lib.requests.post(instance_url + '/services/data/v52.0/tooling/sobjects/TraceFlag/', json=payload, headers=headers)
                    if response.status_code == 201:
                        success_users.append(user_id)
                    else:
                        content = response.content.decode('utf-8')
                        data = lib.json.loads(content)
                        message = None
                        if isinstance(data, list) and len(data) > 0:
                            message = data[0].get("message", "")
                        if message is None:
                            message = response.content
                        error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during enabling logs: {message} ID: [{user_id}]"
                        lib.messagebox.showerror("Error", error_message)
                return success_users
            except Exception as e:
                error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during enabling logs: {str(e)}"
                lib.messagebox.showerror("Error", error_message)
                return
        else:
            error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during the request, no response returned!"
            lib.messagebox.showerror("Error", error_message)

    def create_delete_debug_level(self, payload, delete_dbg):
        if self.response is not None:
            instance_url = self.response.get("instance_url")
            headers = self.response.get("headers")
            try:
                if delete_dbg is True:
                    response = lib.requests.delete(instance_url + f"/services/data/v52.0/tooling/sobjects/DebugLevel/{payload['Id']}", headers=headers)
                else:
                    response = lib.requests.post(instance_url + '/services/data/v52.0/tooling/sobjects/DebugLevel', json=payload, headers=headers)
                if response.status_code == 201:
                    info_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nNew debug level {payload['DeveloperName']} inserted successfully"
                    lib.messagebox.showinfo("Completed", info_message)
                    return True
                elif response.status_code == 204:
                    info_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nDebug level {payload['DeveloperName']} was deleted successfully"
                    lib.messagebox.showinfo("Completed", info_message)
                    return True
                else:
                    error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during the request: {response.content}"
                    lib.messagebox.showerror("Error", error_message)
                    return False
            except Exception as e:
                error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError while searching for Debug Levels: {str(e)}"
                lib.messagebox.showerror("Error", error_message)
                return
        else:
            error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during the request, no response returned!"
            lib.messagebox.showerror("Error", error_message)
            return False

    def delete_all_logs(self):
        if self.response is not None:
            instance_url = self.response.get("instance_url")
            headers = self.response.get("headers")
            try:
                response = lib.requests.get(instance_url + "/services/data/v52.0/tooling/query/?q=SELECT+Id+FROM+ApexLog", headers=headers)
                if response.status_code == 200:
                    records = response.json().get('records')
                    if len(records) > 0:
                        if len(records) > 200:
                            info = f"The number of logs to delete is: {len(records)} and because of it's over 200, the process will take a while!\nPress \"OK\" to continue."
                            lib.messagebox.showinfo("Completed", info)
                            chunks = []
                            del_true = 0
                            del_false = 0
                            for i in range(0, len(records), 200):
                                chunk = records[i:i+200]
                                chunks.append(chunk)
                                log_ids = [item['Id'] for item in chunk]
                                formatted_list = ','.join(log_ids)
                                del_resp = lib.requests.delete(instance_url + f"/services/data/v52.0/composite/sobjects?ids={formatted_list}&allOrNone=false", headers=headers)
                                if del_resp.status_code == 200:
                                    result = del_resp.json()
                                    for item in result:
                                        if item["success"] is True:
                                            del_true += 1
                                        else:
                                            del_false += 1
                                else:
                                    error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during deleting logs: {del_resp.content}"
                                    lib.messagebox.showerror("Error", error_message)
                            success_message = None
                            if del_true > 0:
                                success_message = f"{lib.datetime.now().replace(microsecond=0)}\n\n[{del_true}] - Logs deleted successfully"
                            if del_false > 0:
                                success_message += f"\n[{del_false}] - Logs not deleted\n\n"
                            lib.messagebox.showinfo("Completed", success_message)
                        else:
                            info_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nNo logs to delete in the environment"
                            lib.messagebox.showinfo("Completed", info_message)
                    else:
                        info_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during retrieve logs: {response.content}"
                        lib.messagebox.showinfo("Completed", info_message)
            except Exception as e:
                error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during deleting logs: {str(e)}"
                lib.messagebox.showerror("Error", error_message)
                return
        else:
            error_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nError during the request, no response returned!"
            lib.messagebox.showerror("Error", error_message)
