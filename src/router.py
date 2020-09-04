import os
from src.interface import Interface


class IterRouter(type):
    def __iter__(cls):
        return iter(cls._all_routers)

class Router(metaclass=IterRouter):
    _all_routers = []
    available_protocols = ['RIP1','RIP2','OSPF1','OSPF2']

    def __init__(self,hostname):
        # If the hostname already exists, then raise a ValueError
        double_list = [hostname == router.hostname for router in self._all_routers]
        if sum(double_list) != 0:
            raise ValueError(f"Router hostname <{hostname}> already exists")
        # Add new router to list of instances.
        Router._all_routers.append(self)
        # Set class instance attributes.
        self.hostname = hostname
        self.commands = ["en", "conf t", "no ip domain-lookup"]
        self.interfaces: [Interface] = []
        self.activated_protocols: {str: bool} = {'RIP1': False, 'RIP2': False, 'OSPF1': False, 'OSPF2': False}

    def __eq__(self, other):
        if not isinstance(other, Router):
            # don't attempt to compare against unrelated types
            return NotImplementedError
        return self.__dict__ == other.__dict__

    def add_interface(self,interface:Interface):
        # If the interface already exists, raise a ValueError.
        if len(self.interfaces) != 0:
            print("More than interface existed before you added this new interface")
            double_list = [interface == current_interface for current_interface in self.interfaces]
            print("Does your new interface match any existing ones?: ", double_list)
            if sum(double_list) != 0:
                print("You did an oopsie")
                raise ValueError
        self.interfaces = self.interfaces + [interface]

    def activate_protocol(self,protocol):
        "ONLY ADD PROTOCOLS AT THE END of the program!"
        if protocol not in self.available_protocols:
            raise ValueError(f"This is not a valid protocol: {protocol}")
        else:
            self.activated_protocols[protocol] = True

    def add_protocol_config(self,protocol):
        if protocol == 'RIP1':
            pass
        elif protocol == 'RIP2':
            # Configure and add networks and then exit.
            commands = ['ip routing','router rip','version 2','no auto-summary']
            for interface in self.interfaces:
                commands.append("network %s" % interface._cidr[0])
            self.commands.extend(commands)
            self.commands.append('exit')
        elif protocol == 'OSPF1':
            pass
        elif protocol == 'OSPF2':
            pass
        else:
            raise ValueError(f"<{protocol}> is Not a Valid Protocol")

    def exit(self):
        # Add the hostname to the commands
        self.commands += ["hostname %s" % self.hostname]
        # Add interface configurations to commands.
        for interface in self.interfaces:
            self.commands.extend(interface.commands)
        # Add each protocol if activated.
        for protocol,activated in self.protocols:
            if activated:
                self.add_protocol_config(protocol)
        self.commands += ["end","wr mem"]
        self.generate_output()


    def generate_output(self,folder):
        filename = os.path.join(folder,"%s.txt" %self.hostname)
        if (os.path.isfile(filename)):
            raise ValueError(f"There is already a file called {filename}")
        output_file = open(filename, "w")
        for command in self.commands:
            output_file.write(command + "\n ! \n")
        output_file.close()

    # Used to check that two routers with the same hostname do not exist.




