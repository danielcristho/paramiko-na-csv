import paramiko
import time
import csv
from datetime import datetime

conn_ssh = paramiko.SSHClient()
conn_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#Create script log
create_log = open("script-logs.txt", "a")

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
        conn = conn_ssh.invoke_shell()
        print("****************************************************")
        print(f"Success login to {device['username']}")

        if device['vendor'] == "cisco":
            conn.send("enable\n")
            conn.send("admin\n")
            conn.send("conf t\n")
            conn.send("int lo0\n")
            conn.send("ip add 1.1.1.1 255.255.255.255\n")
            conn.send("no sh\n")
            conn.send("do show ip int br | exc unass\n")
            time.sleep(10)
            output = conn.recv(65535).decode()

        elif device['vendor'] == "mikrotik":
            conn_ssh.exec_command("interface vlan add name=testing vlan-id=10 interface=ether4\n")
            conn_ssh.exec_command("interface vlan print\n")
            time.sleep(10)
            output = conn.recv(65535).decode()

        else:
            print("Unknown vendor")

        conn_ssh.close()
        file_backup = open(f"backup/{device['ip']}.cfg", "w")
        file_backup.write(output)
        file_backup.close()

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