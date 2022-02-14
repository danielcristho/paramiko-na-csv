from netmiko import ConnectHandler
rtr_ios1  = {
    "device_type": 'cisco_ios',
    "host": '172.16.1.254',
    "username": 'admin',
    "password": 'cisco123'
}
try_conn = ConnectHandler(**rtr_ios1)
output = try_conn.send_command("show ip interface brief")
print(output)

config_commands = ['int loop 0', 'ip address 1.1.1.1 255.255.255.255']
output = try_conn.send_config_set(config_commands)
print(output)

# for x in range(2,6):
#     print ("Create interface loopback") + str(x)