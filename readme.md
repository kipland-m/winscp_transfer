Program Setup

Download WinSCP - https://winscp.net/eng/download.php

When installing, please choose to install for all users as the default path in the code is at "C:\Program Files (x86)\WinSCP\WinSCP.com", otherwise this file path for the CLI tool in the python script will have to change.

In config_template.json, please configure the SFTP server credentials for both the source server (server you are pulling files from) and the destination server (server you are pushing files to)

Change the remote and local paths as necessary.
 
Rename 'config_template.json' to 'config.json'

Launch the .py script.
