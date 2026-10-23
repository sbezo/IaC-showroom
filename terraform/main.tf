provider "vsphere" {
  user                 = var.vc_user
  password             = var.vc_password
  vsphere_server       = var.vc_server
  allow_unverified_ssl = false
}

data "vsphere_datacenter" "dc" {
  name = var.vc_dc
}

data "vsphere_distributed_virtual_switch" "dvs" {
  name          = var.vc_dvs
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_resource_pool" "pool" {
  name          = var.vc_pool
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_datastore" "datastore" {
  name          = var.vc_datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "MNG" {
  name          = var.vc_mng
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_virtual_machine" "ubuntu-template" {
  name          = "ubuntu-template"
  datacenter_id = data.vsphere_datacenter.dc.id
}

#####################################################################################


# create node app-host
resource "vsphere_virtual_machine" "app-host" {
  name                       = "app-host"
  resource_pool_id           = data.vsphere_resource_pool.pool.id
  datastore_id               = data.vsphere_datastore.datastore.id
  num_cpus                   = 8
  memory                     = 16384
  guest_id                   = data.vsphere_virtual_machine.ubuntu-template.guest_id
  folder                     = "Examples"
  wait_for_guest_net_timeout = 0
  network_interface {
    network_id   = data.vsphere_network.MNG.id
    adapter_type = "vmxnet3"
  }
  disk {
    label            = "Hard disk 1"
    size             = 128
    thin_provisioned = true
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.ubuntu-template.id
    customize {
      linux_options {
        host_name = "apps"
        domain    = "example.test"
      }
      network_interface {
        ipv4_address = "192.0.2.21"
        ipv4_netmask = 24
      }

      ipv4_gateway    = "192.0.2.1"
      dns_server_list = ["192.0.2.10", "8.8.8.8"]
    }
  }
}


# create node gitlab.example.test
resource "vsphere_virtual_machine" "gitlab-host" {
  name                       = "gitlab-host"
  resource_pool_id           = data.vsphere_resource_pool.pool.id
  datastore_id               = data.vsphere_datastore.datastore.id
  num_cpus                   = 4
  memory                     = 16384
  guest_id                   = data.vsphere_virtual_machine.ubuntu-template.guest_id
  folder                     = "Examples"
  wait_for_guest_net_timeout = 0
  network_interface {
    network_id   = data.vsphere_network.MNG.id
    adapter_type = "vmxnet3"
  }
  disk {
    label            = "Hard disk 1"
    size             = 128
    thin_provisioned = true
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.ubuntu-template.id
    customize {
      linux_options {
        host_name = "gitlab"
        domain    = "example.test"
      }
      network_interface {
        ipv4_address = "192.0.2.20"
        ipv4_netmask = 24
      }

      ipv4_gateway    = "192.0.2.1"
      dns_server_list = ["192.0.2.10", "8.8.8.8"]
    }
  }
}

# create node gitlab-runner.example.test
resource "vsphere_virtual_machine" "runner-host" {
  name                       = "runner-host"
  resource_pool_id           = data.vsphere_resource_pool.pool.id
  datastore_id               = data.vsphere_datastore.datastore.id
  num_cpus                   = 2
  memory                     = 8192
  guest_id                   = data.vsphere_virtual_machine.ubuntu-template.guest_id
  folder                     = "Examples"
  wait_for_guest_net_timeout = 0
  network_interface {
    network_id   = data.vsphere_network.MNG.id
    adapter_type = "vmxnet3"
  }
  disk {
    label            = "Hard disk 1"
    size             = 64
    thin_provisioned = true
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.ubuntu-template.id
    customize {
      linux_options {
        host_name = "gitlab-runner"
        domain    = "example.test"
      }
      network_interface {
        ipv4_address = "192.0.2.19"
        ipv4_netmask = 24
      }

      ipv4_gateway    = "192.0.2.1"
      dns_server_list = ["192.0.2.10", "8.8.8.8"]
    }
  }
}

# create node infra-host node
resource "vsphere_virtual_machine" "infra-host" {
  name                       = "infra-host"
  resource_pool_id           = data.vsphere_resource_pool.pool.id
  datastore_id               = data.vsphere_datastore.datastore.id
  num_cpus                   = 1
  memory                     = 4096
  guest_id                   = data.vsphere_virtual_machine.ubuntu-template.guest_id
  folder                     = "Examples"
  wait_for_guest_net_timeout = 0
  network_interface {
    network_id   = data.vsphere_network.MNG.id
    adapter_type = "vmxnet3"
  }
  disk {
    label            = "Hard disk 1"
    size             = 32
    thin_provisioned = true
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.ubuntu-template.id
    customize {
      linux_options {
        host_name = "infra-services"
        domain    = "example.test"
      }
      network_interface {
        ipv4_address = "192.0.2.10"
        ipv4_netmask = 24
      }

      ipv4_gateway    = "192.0.2.1"
      dns_server_list = ["8.8.8.8"]
    }
  }
}
