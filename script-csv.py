import paramiko
import time
import csv
import os
import sys
from datetime import datetime

conn_ssh = paramiko.SSHClient()
conn_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#Create
create_log = open("logs.txt", "a")

#Read from CSV file
readcsv_file = open("list-devices.csv", "r")
listcsv_device = csv.DictReader(readcsv_file, delimiter=",")

for device in listcsv_device:
    try:
        conn_ssh.connect(
            hostname=device['ip'],
            username=device['username'],
            password=device['password'],
            port = device['port'] if device['port'] else 22,
            look_for_keys=False, allow_agent=False
        )
        print("****************************************************")
        print(f"Succes login to {device['username']}")
        conn = conn_ssh.invoke_shell()

        conn.send("show ip int br | exclude unass")
        time.sleep(10)

        output = conn.recv(65535).decode()
        file_backup = open(f"backup/{device['ip']}.cfg", "w")
        file_backup.write(output)
        file_backup.close()

        conn_ssh.close()

#Create error exception
    except paramiko.ssh_exception.AuthenticationException as message:
        print(f"{message} [{device['ip']}] ")
        create_log.write(f"{message} {datetime.now()}\n")
        pass

    except paramiko.ssh_exception.NoValidConnectionsError as message:
        print(f"{message}")
        create_log.write(f"{message} {datetime.now()}\n")

    #DEFAULT EXECEPTION!!!
    except Exception as message:
        print(f"error: {message} [{device['ip']}]")
        create_log.write(f"error, message: {message} {datetime.now()}\n")

create_log.close()


