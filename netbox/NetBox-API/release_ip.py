import os
from pathlib import Path
from dotenv import load_dotenv
import pynetbox
import datetime

# NetBox API URL and token
load_dotenv(Path(__file__).resolve().parent / ".env", interpolate=False)
NETBOX_API_URL = os.environ["NETBOX_API_URL"]
NETBOX_API_TOKEN = os.environ["NETBOX_API_TOKEN"]

# Initialize NetBox API
nb = pynetbox.api(NETBOX_API_URL, token=NETBOX_API_TOKEN)

# Define device parameters
site_name = 'Example Site'
site_group = 'LAB'
vlan_name = 'Example'
vlan_id = 100
prefix = '192.0.2.0/24'

# Load objects of example prefix
site = nb.dcim.sites.get(name=site_name)
vlan_obj = nb.ipam.vlans.get(vid=vlan_id)
prefix_obj = nb.ipam.prefixes.get(prefix=prefix)

# try to book an IP
print(f"### Releasing IP from {prefix} on site {site_name}, VLAN {vlan_name} ({vlan_id}) ###\n")

# print all booked IPs in this prefix
all_ips = nb.ipam.ip_addresses.filter(prefix_id=prefix_obj.id)
for ip in all_ips:
    print(f" - {ip.address:<20} - {ip.dns_name:<25} - {ip.description}")


ip_to_release = input("\nEnter last octet of 192.0.2.x/24 to release: ")
if not ip_to_release.isdigit() or not 1 < int(ip_to_release) <= 254:
    print("Invalid input, exiting...")
    exit()
ip_address = f"192.0.2.{ip_to_release}/24"
# check if IP is booked
ip = nb.ipam.ip_addresses.get(address=ip_address)
if not ip:
    print('This IP is not booked, exiting...\n')
else:
    print(f' OK, releasing...')
    ip.delete()
    print(f"IP address {ip_address} has been released.\n")
