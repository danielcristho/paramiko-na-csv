from netmiko import ConnectHandler
router1 = {
    "device_type": 'mikrotik_routeros',
    "host": '172.16.1.1',
    "username": 'rtr1',
    "password": 'router1',
}

conn = ConnectHandler(**router1)
output = conn.send_command("ip address print")
#print(f"Interface on {router1['host']}")
print(output)
