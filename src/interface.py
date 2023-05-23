import src as lib


def validate_entries(entries):
    for entry in entries:
        if not entry.get():
            return False
    return True


class SFDXLogInterface:
    def __init__(self):
        self.db_lvl_map = None
        self.hours_entry = None
        self.user_widget = None
        self.data_mng = None
        self.connect = None
        self.user_window = None
        self.entry = None
        self.debug_var = None
        self.main_window = None
        self.config_window = None
        self.environment_var = None
        self.debug_level_options = ['']

        # Create window
        self.window = lib.tk.Tk()
        self.window.title("SDFX Logs")
        self.window.geometry("300x200")
        self.window.iconbitmap("salesforce_icon.ico")

        # Apply a theme using ttkthemes
        style = lib.ThemedStyle(self.window)
        style.set_theme("radiance")

        self.create_widgets()

    def create_widgets(self):
        # First windows [SELECT ENVIRONMENT]
        welcome_label = lib.ttk.Label(self.window, text="Welcome to SFDX Logs!")
        welcome_label.pack(pady=10)
        label = lib.ttk.Label(self.window, text="Choose the environment:")
        label.pack(pady=5)

        env_frame = lib.ttk.Frame(self.window)
        env_frame.pack(pady=10)

        environment_options = self.update_env_options()
        environment_dropdown = lib.ttk.OptionMenu(env_frame, self.environment_var, *environment_options)
        environment_dropdown.pack(side=lib.tk.LEFT, padx=5)

        configure_button = lib.ttk.Button(env_frame, text="New Environment", command=self.open_configuration_window)
        configure_button.pack(side=lib.tk.LEFT, padx=5)

        submit_button = lib.ttk.Button(self.window, text="Submit", command=self.open_main_window)
        submit_button.pack(pady=10)

    def update_env_options(self):
        environment_options = ['']
        with open('../cred.json', 'r') as conf_file:
            if lib.os.path.getsize('../cred.json') > 0:
                config = lib.json.load(conf_file)

        if lib.os.path.getsize('../cred.json') > 0:
            for env in config:
                environment_options.append(env)

        if len(environment_options) > 1:
            self.environment_var = lib.tk.StringVar(self.window, environment_options[1])
        else:
            self.environment_var = lib.tk.StringVar(self.window, environment_options[0])

        return environment_options

    def open_configuration_window(self):
        if self.config_window is None:
            self.config_window = lib.tk.Toplevel(self.window)
            self.config_window.title("Configure new environment")
            self.config_window.iconbitmap("salesforce_icon.ico")
            self.config_window.geometry("400x600")

            label = lib.ttk.Label(self.config_window, text="(*) = Required field")
            label.pack(pady=5)

            # Create labels and entry fields for each information
            labels = ["Environment", "Username", "Password", "Token", "Client ID",
                      "Secret Key", "Base URL"]
            entries = []
            for label_text in labels:
                frame = lib.ttk.Frame(self.config_window)
                frame.pack(pady=5)
                label = lib.ttk.Label(frame, text="(*) " + label_text + ":")
                label.pack(pady=5)
                if label_text == "Password" or label_text == "Token" or label_text == "Secret Key":
                    entry = lib.ttk.Entry(frame, show="*", width=30)
                else:
                    entry = lib.ttk.Entry(frame, width=30)
                entry.pack(side=lib.tk.LEFT, pady=5)
                entries.append(entry)

            # Create a button to save the configuration
            save_button = lib.ttk.Button(self.config_window, text="Save", command=lambda: self.save_configuration(entries))
            save_button.pack(pady=10)
        else:
            self.config_window.lift()

    def save_configuration(self, entries):
        if not validate_entries(entries):
            lib.messagebox.showerror("Error", "Please fill in all fields")
            return

        old_config = {}

        try:
            with open('../cred.json', 'r') as config_file:
                if lib.os.path.getsize('../cred.json') > 0:
                    old_config = lib.json.load(config_file)
        except FileNotFoundError:
            pass

        env_name = entries[0].get()

        new_config = {
            "username": entries[1].get(),
            "password": entries[2].get(),
            "token": entries[3].get(),
            "clientId": entries[4].get(),
            "secret_key": entries[5].get(),
            "base_url": entries[6].get()
        }

        old_config[f"{env_name}"] = new_config

        with open('../cred.json', 'w') as config_file:
            lib.json.dump(old_config, config_file, indent=4)

        self.config_window.destroy()
        self.config_window = None

        lib.messagebox.showinfo("Completed", f"New environment {env_name} inserted successfully")

        environment_options = self.update_env_options()
        environment_dropdown = lib.ttk.OptionMenu(self.window, self.environment_var, *environment_options)
        environment_dropdown.pack(padx=5)
        self.window.destroy()
        self.window = None
        SFDXLogInterface()

    def open_main_window(self):
        if self.main_window is None:

            # Create connection
            self.connect = lib.conn()
            self.connect.set_environment(self.environment_var.get())
            self.connect.get_connection()
            if self.connect.response is not None:

                # Create main window
                self.main_window = lib.tk.Tk()
                self.main_window.title("SFDX Logs - Enable Logs")
                self.main_window.geometry("550x210")
                self.main_window.iconbitmap("salesforce_icon.ico")

                # Apply a theme using ttkthemes
                style = lib.ThemedStyle(self.main_window)
                style.set_theme("radiance")

                # Fist section [DEBUG]
                db_lvl_label = lib.ttk.Label(self.main_window, text="Select the debug level and the hours number to be enable:")
                db_lvl_label.pack(pady=5)

                debug_frame = lib.ttk.Frame(self.main_window)
                debug_frame.pack(pady=10)

                self.data_mng = lib.dr()
                self.data_mng.set_connection_response(self.connect.response)
                db_lvl_resp = self.data_mng.get_debug_levels()
                if db_lvl_resp is not None:
                    self.db_lvl_map = {}
                    for db_lvl in db_lvl_resp:
                        key = db_lvl.get("DeveloperName")
                        val = db_lvl.get("Id")
                        self.db_lvl_map[key] = val
                        self.debug_level_options.append(key)

                    db_label = lib.ttk.Label(debug_frame, text="Debug Level:")
                    db_label.pack(side=lib.tk.LEFT, padx=10)
                    self.debug_var = lib.tk.StringVar(self.main_window, self.debug_level_options[1])
                    debug_log_dropdown = lib.ttk.OptionMenu(debug_frame, self.debug_var, *self.debug_level_options)
                    debug_log_dropdown.pack(side=lib.tk.LEFT, padx=10)

                    h_label = lib.ttk.Label(debug_frame, text="Hour:")
                    h_label.pack(side=lib.tk.LEFT, padx=10)

                    self.hours_entry = lib.ttk.Entry(debug_frame, width=5)
                    self.hours_entry.pack(side=lib.tk.LEFT, padx=10)

                    label_ids = lib.ttk.Label(self.main_window, text="Enter user IDs separated by commas:")
                    label_ids.pack(pady=10)

                    self.entry = lib.ttk.Entry(self.main_window, width=50)
                    self.entry.pack(pady=5)

                    button_frame = lib.ttk.Frame(self.main_window)
                    button_frame.pack(pady=10)

                    enable_button = lib.ttk.Button(button_frame, text="Enable Logs", command=self.validate_hours)
                    enable_button.pack(side=lib.tk.LEFT, padx=5)

                    query_button = lib.ttk.Button(button_frame, text="Show Users", command=self.open_user_window)
                    query_button.pack(side=lib.tk.LEFT, padx=5)

                    refresh_button = lib.ttk.Button(button_frame, text="Change Environment", command=lambda: self.change_env())
                    refresh_button.pack(side=lib.tk.LEFT, padx=5)

                    self.window.destroy()

    def open_user_window(self):
        if self.user_window is None:
            records = self.data_mng.query_user_ids()
            user_ids = [(record['Name'], record['Id']) for record in records]
            # Create a window to display the results
            self.user_window = lib.tk.Toplevel(self.main_window)
            self.user_window.title(f"Users - [{self.environment_var.get()}]")
            self.user_window.iconbitmap("salesforce_icon.ico")

            self.user_widget = lib.tk.Text(self.user_window, width=50, height=30)
            self.user_widget.pack(side=lib.tk.LEFT, fill=lib.tk.BOTH)

            formatted_text = ""
            for name, user_id in user_ids:
                formatted_text += f"Username: {name}\nUser ID: {user_id}\n\n"
            self.user_widget.insert("1.0", formatted_text)
            self.user_widget.config(state=lib.tk.DISABLED)

        else:
            warning_message = f"{lib.datetime.now().replace(microsecond=0)}\n\nWarning, the user window is already opened"
            lib.messagebox.showwarning("Warning", warning_message)

    def validate_hours(self):
        hours = self.hours_entry.get()
        selected_ids = self.entry.get().split(',')
        selected_debug_lvl = self.debug_var.get()
        debug_lvl_id = self.db_lvl_map.get(selected_debug_lvl)
        if (hours != "" and str.isdigit(hours)) and (selected_ids[0] != "") and (debug_lvl_id != ""):
            enabled_users = self.data_mng.enable_salesforce_logs(hours, selected_ids, debug_lvl_id)
            if enabled_users is not None:
                success_message = f"{lib.datetime.now().replace(microsecond=0)}\n\n"
                success_message += "The currents users are enabled successfully:\n"
                for en_us in enabled_users:
                    success_message += "- " + en_us + "\n"
                lib.messagebox.showinfo("Completed", success_message)
        else:
            warning_message = f"{lib.datetime.now().replace(microsecond=0)}\n\n"
            if hours == "" or not str.isdigit(hours):
                warning_message += "Warning, only numbers are allowed in \'Hour\' field\n\n"
            if selected_ids[0] == "":
                warning_message += "Warning, insert at least a valid Id\n\n"
            if debug_lvl_id == "":
                warning_message += "Warning, something went wrong retrieving debug level"
            lib.messagebox.showwarning("Warning", warning_message)

    def change_env(self):
        self.main_window.destroy()
        SFDXLogInterface()

    def run(self):
        self.window.mainloop()
