from network_interfaces import InterfacesFile


if_ = InterfacesFile('/etc/network/interfaces')
eth0 = if_.get_iface('eth0')
eth0.address = '192.168.11.2'
if_.save('/etc/network/interfaces', validate=False)