import weakref
from ipaddress import IPv4Network, IPv4Address
from interfaces import Interface
import os
class Router:
    hostname = None
    commands = ["en","conf t","no ip domain-lookup"]

    def __init__(self,hostname):
        # If the hostname already exists, then raise a ValueError
        if sum([hostname == router.hostname for router in self.getinstances()]) != 0:
            raise ValueError(f"Router hostname <{hostname}> already exists")
        self.hostname = hostname
        self.commands += ["hostname %s" % self.hostname]

    def add_interface(self,interface:Interface):
        self.interfaces.append(interface)

    # Used to check that two routers with the same hostname do not exist.
    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def configure_interfaces(self):
        for interface,values in self.networks.items():


    def done(self):
        # ["end", "wr mem"]

        # Configure rip
        self.commands += ["end","wr mem"]
        self.generate_output()


    def generate_output(self):
        filename = "%s.txt" %self.hostname
        if (os.path.isfile(filename)):
            raise ValueError(f"There is already a file called {filename}")
        output_file = open(filename, "w")
        for command in self.commands:
            output_file.write(command + "\n ! \n")
        output_file.close()








