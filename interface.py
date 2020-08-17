# interface  = input("Ex: g2/2 fa2/5 | Please enter interface: ")
# net_id = input("Ex: 192.168.0.0/25 | Please enter networks id for %s with a subnet: " % interface)
# address = input("Ex: 192.168.1.2 | Please enter IP Address for int %s: " % interface)
import re
import socket
import struct
class Interface(object):
    """
    Interface works with fast ethernet and gigabit ethernet ports.
    TO DO: Provide support for serial interfaces.
    """
    def __init__(self,port:str,cidr:str,ip_address:str):
        # Make sure you can change the interface.
        self.init_commands: [str] = [None, "no switchport"]
        self.config_commands: [str] = [None]
        # Stop the port interface from going down
        # Get out of the interface
        self.exit_commands = ["no shut", "exit"]
        self._port: [str] = None
        self._cidr: [str] = None
        self._ip_address: [str] = None
        # Example 255.255.255.0
        self.netmask: str = None
        self.port = port
        self.cidr = cidr
        self.ip_address = ip_address
        self.init_setup()
        self.config_setup()

    @property
    def commands(self) -> [str]:
        commands = self.init_commands + self.config_commands + self.exit_commands
        return commands

    @property
    def port(self) -> str:
        # A list of valid regex for the first part of the port.
        return ' '.join(self._port)

    @property
    def cidr(self) -> str:
        return '/'.join(self._cidr)

    @property
    def ip_address(self) -> str:
        return '.'.join(self._ip_address)

    @port.setter
    def port(self,port:str):
        # todo: Add support for VLAN(You'll support Switches Later).
        valid_port_types = ['^fastethernet$', '$f$', '^fa$', '^gigabitethernet$', '^g$', '^gb$']
        # Split the port by spaces.
        port_split = port.split()
        # If the port is not split by spaces, then split it by letters and numbers separated by "/".
        if len(port_split) != 2:
            port_split = re.match("([a-zA-Z]+)([0-9]+/[0-9]+)",port_split[0])
            if port_split == None:
                raise ValueError(f"<{port}> is not a valid port name")
            port_split = list(port_split.groups())
        # If the first part of the port is not a valid port type, raise a ValueError.
        if sum([bool(re.match(port_name, port_split[0])) for port_name in valid_port_types]) != 1:
            raise ValueError(f'<{port_split[0]}> is not a valid port name')
        # If the second part of the port does not contain '/', raise a ValueError.
        if '/' not in port_split[1]:
            raise ValueError(f'port number <{port_split[0]}> <{port_split[1]}> does not contain "/"')
        self._port = port_split
        self.init_setup()

    @cidr.setter
    def cidr(self,cidr):
        cidr_split = re.split("/",cidr)
        if len(cidr_split) != 2:
            raise ValueError(f'cidr <{cidr}> does not contain "/" or is invalid')
        cidr_split = [value.strip() for value in cidr_split]
        valid_subnet_address = '\d{,3}.\d{,3}.\d{,3}.\d{,3}'
        if not bool(re.match(valid_subnet_address,cidr_split[0])):
            raise ValueError(f'<{cidr_split[0]}> is not a valid subnet address')
        if '/' in cidr_split[1]:
            cidr_split[1] = cidr_split[1].replace("/","")
        prefix = int(cidr_split[1])
        if prefix < 0 or prefix > 32:
            raise ValueError(f"<{cidr_split[1]}> is not a valid subnet mask")
        network,netmask = self.cidr_to_netmask('/'.join(cidr_split))
        self.netmask = netmask
        self._cidr = [network,str(prefix)]
        if self._ip_address != None:
            self.config_setup()

    @ip_address.setter
    def ip_address(self,ip_address):
        # Remove spaces and split ip address by "."
        split_ip_address = ip_address.replace(" ","").split(".")
        valid_ip_address = '\d{,3}.\d{,3}.\d{,3}.\d{,3}'
        # If the IP address does not match X.X.X.X, raise a ValueError.
        if not bool(re.match(valid_ip_address, ip_address)):
            raise ValueError(f'<{ip_address}> is not a valid IP address')
        self._ip_address = split_ip_address
        self.config_setup()

    @staticmethod
    # https://stackoverflow.com/questions/33750233/convert-cidr-to-subnet-mask-in-python
    # "<<" and ">>" are bitwise operators that move the binary value over by the number of digits.
    def cidr_to_netmask(cidr):
        network, net_bits = cidr.split('/')
        host_bits = 32 - int(net_bits)
        # ntoa only supports 32 bit IPV4, use ntop to support ipv6
        # todo support IPV6
        netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
        return network, netmask

    def init_setup(self):
        # Enter the interface.
        self.init_commands[0] = "int %s" % self.port


    def config_setup(self):
        self.config_commands = ["ip address %s %s" % (self.ip_address, self.netmask)]

    def __str__(self):
        return ','.join([self.port,self.cidr,self.ip_address])

