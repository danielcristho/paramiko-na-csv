import paramiko
import time
import csv
from datetime import date, datetime

conn_ssh = paramiko.SSHClient()
conn_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#CREATE LOG FILE
create_log = open("Logs.txt", "a")

#READ CSV FILE
readcsv_file = open("LIST.csv", "r")
listcsv_device = csv.DictReader(readcsv_file, delimiter=",")

for device in listcsv_device:
    try:
        conn_ssh.connect(
            hostname=device['ip'],
            username=device['username'],
            password=device['password'],
            port = device['port'] if device['port'] else 22
        )
        print("****************************************************")
        print(f"Succes login to {device['usernam']}")
        conn = conn_ssh.invoke_shell()

        conn.send("ip int print")
        time.sleep(5)

        output = conn.recv(65535).decode()
        file_backup = open(f"backup-config/{device['ip']}.cfg", "w")
        file_backup.write(output)
        file_backup.close()

        conn_ssh.close()

#CREATE ERR EXECPTION
    except paramiko.ssh_exception.AuthenticationException as message:
        print(f"{message} [{device['ip']}] ")
        create_log.write(f"{message} {datetime.now()}\n")

    except paramiko.ssh_exception.NoValidConnectionsErrot as message:
        print(f"{message}")
        create_log.write(f"{message} {datetime.now()}\n")

    #DEFAULT EXECEPTION!!!
    except Exception as message:    
        print(f"error: {message} [{device['ip']}]")
        create_log.write(f"error, message: {message} {datetime.now()}\n")

create_log.close()


