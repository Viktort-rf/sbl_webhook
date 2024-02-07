# iface_set.py

import argparse
import ipaddress
from netmiko import ConnectHandler
from pynetbox import api

def main():
    parser = argparse.ArgumentParser(description='Process VLAN data')
    parser.add_argument("--state_if", required=True, help="State of interface")
    parser.add_argument('--device_name', required=True, help='Name of the device')
    parser.add_argument('--mode_value', required=True, help='value of the mode')
    parser.add_argument('--untagged_vlan_vid', required=True, help='ID of the untagged VLAN')
    parser.add_argument("--name_if", required=True, help="Name iface")

    args = parser.parse_args()

    # Main code this
    print(f"State_if: {args.state_if}, Device: {args.device_name}, Mode: {args.mode_value}, Untagged VLAN ID: {args.untagged_vlan_vid}, Name_if: {args.name_if}")

    # Set on real data
    netbox_url = "https://netbox.example.com"
    netbox_token = "12345678"
    nb = api(url=netbox_url, token=netbox_token)

    username = "username"
    password = "pass"
    cisco_device = []

    devices = nb.dcim.devices.filter(name=args.device_name, status="active", has_primary_ip=True)

    for device in devices:
        primary_ip = device.primary_ip
        manufacturer = device.device_type.manufacturer.slug
        if manufacturer == "cisco":
            cisco_device.append(primary_ip)
        else:
            print("Manufacturer not found")

    with open("ip_list.log", "a", encoding="utf-8") as file:
        file.write('\n'.join(map(str, cisco_device)))
    print(cisco_device)
    print("Hello web!")

    if cisco_device:
        for ip_address_with_mask in cisco_device:
            ip_address = ipaddress.IPv4Interface(ip_address_with_mask).ip  # Get ip addr without mask
            device_info = {
                    "device_type": "cisco_xe",
                    "ip": str(ip_address),
                    "username": username,
                    "password": password,
                    "read_timeout_override": 30,
                    "session_log": "session_log.txt"
            }
            net_connect = ConnectHandler(**device_info)
            if args.state_if == "false":
                net_connect.send_config_set([f"interface {args.name_if}",
                                            "shutdown",
                                            "end"])
            else:
                net_connect.send_config_set([f"interface {args.name_if}",
                                            "no shutdown",
                                            "end"])
              

if __name__ == "__main__":
    main()
