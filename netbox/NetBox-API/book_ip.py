import os
from pathlib import Path
from dotenv import load_dotenv
import pynetbox
import datetime

def valid_ip(ip_to_book):
    if ip_to_book.isdigit() and 1 < int(ip_to_book) <= 254:
        return True
    return False

today = datetime.date.today()

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
print(f"### Booking IP from {prefix} on site {site_name}, VLAN {vlan_name} ({vlan_id}) ###\n")

ip_to_book = ""
still_finding = True

while still_finding:
    while not valid_ip(ip_to_book):
        ip_to_book = input("Enter last octet of 192.0.2.x/24: ")
    ip_address = f"192.0.2.{ip_to_book}/24"
    # check if IP is already booked
    ip = nb.ipam.ip_addresses.get(address=ip_address)
    if ip:
        still_finding = True
        ip_to_book = ""
        print('Already booked, try again...\n')
    else:
        still_finding = False
        print(' OK, it is free...')
# book IP
hostname = input("Enter hostname for " + ip_address + ": ")
description = input("Enter description for " + ip_address + " (or leave empty): ")
if description == "": description = f"Booked via API on {today}"
ip = nb.ipam.ip_addresses.create(address=ip_address, status='active', description=description, site=site.id, vlan=vlan_obj.id, tenant=None, dns_name=hostname)
print(f"IP address {ip_address} has been booked.")
