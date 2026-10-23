import os
from pathlib import Path
from dotenv import load_dotenv
import pynetbox


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

# Create or get site
site = nb.dcim.sites.get(name=site_name)

if not site:
    site = nb.dcim.sites.create(name=site_name, slug=site_name.lower().replace(' ', '-'))


# Create or get VLAN
vlan_obj = nb.ipam.vlans.get(vid=vlan_id)
if not vlan_obj:
    vlan_obj = nb.ipam.vlans.create(vid=vlan_id, name=vlan_name, site=site.id, description="LAB VLAN for Example")

# Create or get Prefix
prefix_obj = nb.ipam.prefixes.get(prefix=prefix)
if not prefix_obj:
    prefix_obj = nb.ipam.prefixes.create(prefix=prefix, site=site.id, vlan=vlan_obj.id, description="LAB Prefix for Example")
