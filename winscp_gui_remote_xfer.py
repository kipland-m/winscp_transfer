import tkinter as tk
from tkinter import messagebox
import subprocess, json, os, schedule, time, threading
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

    pulling_data_from_label.config(text=f"source: {source_sftp['hostname']}")
    pushing_data_to_label.config(text=f"destination: {destination_sftp['hostname']}")

    download_from_sftp(**source_sftp)

    upload_to_sftp(**destination_sftp)



""" GUI CODE """

def run_script():
    try:
        sftp_xfer()
        update_last_run_time_label()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def update_last_run_time_label():
    last_run_time_label.config(text=f"Last run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def schedule_script_execution(interval_minutes):
    schedule.every(interval_minutes).minutes.do(run_script)

    def run_continuously():
        while True:
            schedule.run_pending()
            time.sleep(1)


    # Start a separate thread to run the schedule continuously
    thread = threading.Thread(target=run_continuously)
    thread.start()

# Create the main application window
root = tk.Tk()
root.title("SFTP Automation")
root.iconbitmap("bluegrass_arrows.ico")


# Set minimum window width and height
root.minsize(350, 200)

# Create a button to run the script
run_button = tk.Button(root, text="Transfer Files", command=run_script)
run_button.pack(pady=10)

pulling_data_from_label = tk.Label(root, text="")
pulling_data_from_label.pack()

pushing_data_to_label = tk.Label(root, text="")
pushing_data_to_label.pack()

# Create a label to display the last run time
last_run_time_label = tk.Label(root, text="")
last_run_time_label.pack()

schedule_script_execution(interval_minutes=3)

# Run the Tkinter event loop
root.mainloop()
