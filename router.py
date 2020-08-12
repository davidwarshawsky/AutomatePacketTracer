from ipaddress import IPv4Network, IPv4Address

class Router:
    hostname = None

    networks = dict()
    network_addresses = []

    rip_commands = ["ip routing","router rip","version 2","no auto-summary"]
    commands = ["en","conf t","no ip domain-lookup"]

    def __init__(self):
        self.hostname = input("Please enter hostname: ")
        self.commands += ["hostname %s" % self.hostname]

    def add_interface(self):

        interface  = input("Ex: g2/2 fa2/5 | Please enter interface: ")
        net_id = input("Ex: 192.168.0.0/25 | Please enter network id for %s with a subnet: " % interface)
        self.network_addresses.append(net_id.split("/")[0])
        network  = IPv4Network(net_id)

        address = input("Ex: 192.168.1.2 | Please enter IP Address for int %s: " % interface)
        mask = str(network.netmask)
        self.networks[interface] = [address,mask]

    def get_net_addrs(self):
        return self.network_addresses

    def get_ip_addresses(self):
        ip_addresses = []
        for value in self.networks:
            ip_addresses.append(value[0])
        return ip_addresses

    def configure_rip(self):
        for addr in self.get_net_addrs():
            self.rip_commands.append("network %s" % addr)
        self.rip_commands.append("exit")
        self.commands += self.rip_commands


    def done(self):
        # ["end", "wr mem"]
        for _int,values in self.networks.items():
            # Enter interface
            self.commands += ["int %s" % _int]
            # Make sure you can change it
            self.commands += ["no switchport"]
            # Set the ip address of the interface
            self.commands += ["ip address %s %s" % (values[0],values[1])]
            # Stop the port interface from going down
            self.commands += ["no shut"]
            # Get out of the interface
            self.commands  += ["exit"]
        # Configure rip
        self.configure_rip()
        self.commands += ["end","wr mem"]
        self.generate_output()




    def generate_output(self):
        output_file = open("%s.txt" %self.hostname, "w")
        for command in self.commands:
            output_file.write(command + "\n ! \n")
        output_file.close()



def main1():
    prompt = " N for new router \n A for a new interface \n D for done with current router \n Q to finish\n R for reminder\n:"
    inp = input(prompt)
    while inp != "Q":
        if (inp == "N"):
            router = Router()
            print("You created a router called %s" % router.hostname)
        if (inp == "A"):
            router.add_interface()
            print("You created an interface")
        if (inp == "D"):
            print("Check this directory for a text file with this hostname you provided")
            router.done()
        if (inp == "R"):
            print(prompt)
        inp = input("R for a reminder of commands | Enter command: ")

if __name__ == '__main__':
    main1()






