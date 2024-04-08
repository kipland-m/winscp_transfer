import tkinter as tk
from tkinter import messagebox
import subprocess, json, os
from datetime import datetime


def download_from_sftp(hostname, port, username, password, remote_path, local_path):
    command = f'"C:\\Program Files (x86)\\WinSCP\\WinSCP.com" /command "open sftp://{username}:{password}@{hostname}:{port}" "get {remote_path} {local_path}" "exit"'
    subprocess.run(command, shell=True)

def upload_to_sftp(hostname, port, username, password, local_path, remote_path):
    command = f'"C:\\Program Files (x86)\\WinSCP\\WinSCP.com" /command "open sftp://{username}:{password}@{hostname}:{port}" "put {local_path} {remote_path}" "exit"'
    subprocess.run(command, shell=True)

def sftp_xfer():

    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_directory, "config.json")

    with open(config_file_path, "r") as file:
        config = json.load(file)

    source_sftp = config["source_sftp"]
    destination_sftp = config["destination_sftp"]

    download_from_sftp(**source_sftp)

    upload_to_sftp(**destination_sftp)



""" GUI CODE """

def run_script():
    try:
        sftp_xfer()
        messagebox.showinfo("Success", "Script executed successfully!")
        update_last_run_time_label()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def update_last_run_time_label():
    last_run_time_label.config(text=f"Last run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Create the main application window
root = tk.Tk()
root.title("SFTP Automation")

# Set minimum window width and height
root.minsize(350, 200)

# Create a button to run the script
run_button = tk.Button(root, text="Transfer Files", command=run_script)
run_button.pack(pady=10)

# Create a label to display the last run time
last_run_time_label = tk.Label(root, text="")
last_run_time_label.pack()

# Run the Tkinter event loop
root.mainloop()
