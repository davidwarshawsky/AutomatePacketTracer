#     def configure_rip(self):
#         for addr in self.get_net_addrs():
#             self.rip_commands.append("network %s" % addr)
#         self.rip_commands.append("exit")
#         self.commands += self.rip_commands

class RIP(object):
    rip_commands = ["ip routing", "router rip", "version 2", "no auto-summary"]



class OSPF(object):

