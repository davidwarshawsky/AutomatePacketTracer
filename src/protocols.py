from src.interface import Interface
#     def configure_rip(self):
#         for addr in self.get_net_addrs():
#             self.rip_commands.append("networks %s" % addr)
#         self.rip_commands.append("exit")
#         self.commands += self.rip_commands

class RIP2(object):
    """
    This class is meant to be initialized at the end of the program. It will take all networks that are
    desired and add rip commands to the Router.
    """
    commands = ["ip routing", "router rip", "version 2", "no auto-summary"]
    networks   = []
    def __init__(self,interfaces:[Interface]):
        self.networks = [interface.cidr[0] for interface in interfaces]
        network_commands = ["networks %s" % network for network in self.networks]
        self.commands.extend(network_commands)
        self.commands.append("exit")

# Pay attention to management side. Many tools free to simulate.
# NGSoft SMTP, Enterprise industry network management tool.
# TODO: Add




class OSPF(object):
    pass
