interface  = input("Ex: g2/2 fa2/5 | Please enter interface: ")
net_id = input("Ex: 192.168.0.0/25 | Please enter network id for %s with a subnet: " % interface)
address = input("Ex: 192.168.1.2 | Please enter IP Address for int %s: " % interface)
import re
class Interface(object):
    """
    Interface works with fast ethernet and gigabit ethernet ports.
    TO DO: Provide support for serial interfaces.
    """
    commands: [str] = []
    # Example: fa 0/1 | g 0/2
    port: [str]     = None
    # Example: 192.168.1.0/24
    cidr: str       = None
    # The actual ip address assigned to the interface.
    # Example: 192.168.1.1
    ip_address: str = None

    def __init__(self,port:str,cidr:str,ip_address):
        self.port = port
        self.cidr = cidr
        self.ip_address = ip_address
        self.initial_setup()
        self.configure_setup()
        self.exit_setup()

    @property
    def port(self):
        # A list of valid regex for the first part of the port.
        return self.port

    @port.setter
    def port(self,port):
        valid_port_types = ['^fastethernet$', '$f$', '^fa$', '^gigabitethernet$', '^g$', '^gb$']
        # Split the port by spaces.
        port_split = port.split()
        # If the first part of the port is not a valid port type, raise a ValueError.
        if sum([bool(re.match(port_name, port_split[0])) for port_name in valid_port_types]) != 1:
            raise ValueError(f'<{port_split[0]}> is not a valid port name')
        # If the second part of the port does not contain '/', raise a ValueError.
        if '/' not in port_split[1]:
            raise ValueError(f'<{port_split[1]}> does not contain "/"')
        return port_split

    @property
    def cidr(self):
        return self.cidr

    @cidr.setter
    def cidr(self,cidr):
        cidr_split = re.split("/",cidr)
        if len(cidr_split) != 2:
            raise ValueError(f'<{cidr}> does not contain "/"')
        valid_subnet_address = '\d{,3}.\d{,3}.\d{,3}.\d{,3}'
        if not bool(re.match(valid_subnet_address,cidr_split[0])):
            raise ValueError(f'<{cidr_split[0]}> is not a valid subnet address')
        valid_subnet_mask   = '^\d$|^[1-3][0-2]$'
        if
        return cidr_split;

    def initial_setup(self):
        # Enter the interface.
        self.commamnds += ["int %s" % self.port]
        # Make sure you can change the interface.
        self.commands  += ["no switchport"]

    def configure_setup(self):
        ["ip address %s %s" % (ip address, subnet_mask)]

    def exit_setup(self):
        # Stop the port interface from going down
        ["no shut"]
        # Get out of the interface
        ["exit"]
