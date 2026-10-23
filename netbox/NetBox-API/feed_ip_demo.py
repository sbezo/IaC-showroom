from pathlib import Path
from dotenv import load_dotenv
import pynetbox
import datetime
import csv
import os

today = datetime.date.today()
description = f"Booked via API on {today}"


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
print(f"### Demo feeding IPs {prefix} on site {site_name}, VLAN {vlan_name} ({vlan_id}) ###\n")

# load files:
with open(Path(__file__).with_name('feed_ip_demo.csv'), 'r') as file:
    lines = file.readlines()
    csv_reader = csv.reader(lines)

for row in csv_reader:
    hostname = row[0]
    ip_to_book = row[1]
    ip_address = f"{ip_to_book}/24"
    # check if IP is already booked
    ip = nb.ipam.ip_addresses.get(address=ip_address)
    if ip:
        print(f'IP {ip_address} already booked, skipping...\n')
    else:
        # book IP
        ip = nb.ipam.ip_addresses.create(address=ip_address, status='active', description=description, site=site.id, vlan=vlan_obj.id, tenant=None, dns_name=hostname)
        print(f"IP address {ip_address} has been booked.")
