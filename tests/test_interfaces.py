import pytest
from interfaces import Interface

@pytest.fixture(scope='module')
def default_interface():
    port = 'fa0/1'
    cidr = '192.168.0.0/24'
    ip_address = '192.168.1.1'
    fa01 = Interface(port=port, cidr=cidr, ip_address=ip_address)
    return fa01

class TestInit(object):
    def test_valid_args(self,default_interface):
        fa01 = default_interface

        port_message = f'<{fa01.port}> is not a valid port name.'
        expected_port = ['fa','0/1']
        assert fa01._port == expected_port,port_message

        cidr_message = f'<{fa01.cidr}> is not a valid cidr'
        expected_cidr = ['192.168.0.0','24']
        assert fa01._cidr == expected_cidr,cidr_message

        ip_message = f'<{fa01.ip_address}> is not a valid ip address'
        expected_ip_address = ['192','168','1','1']
        assert fa01._ip_address == expected_ip_address,ip_message

        command_message = f'<{fa01.commands}>\n are not as expected'
        expected_commands = ['int fa 0/1','no switchport','ip address 192.168.1.1 255.255.255.0','no shut','exit']
        assert fa01.commands == expected_commands,command_message

    def test_spaced_port(self,default_interface):
        # |= 3 spaces, { = start, } = finish, < = spaces from left, > = spaces from right
        #  {|<>|} , {|<},{>|},{a|b},{a|b|>}
        ports = ['   fa0/1   ','   fa0/1','fa0/1   ','fa   0/1','fa   0/1   ']
        fa01 = default_interface

        for port in ports:
            fa01.port = port
            port_message = f'<{port}> is not a valid port name.'
            expected_port = ['fa', '0/1']
            assert fa01._port == expected_port, port_message

    def test_spaced_cidr(self,default_interface):
        # |= 3 spaces, { = start, } = finish, < = spaces from left, > = spaces from right
        #  {|<>|} , {|<},{>|},{a|b},{a|b|>}
        c = '192.168.0.0/24'
        cidrs = [f'   {c}   ',f'{c}   ',f'   {c}','192.168.0.0   /24','192.168.0.0   /24   ']
        fa01 = default_interface
        for cidr in cidrs:
            fa01.cidr = cidr
            cidr_message = f'<{cidr}> is not a valid cidr'
            expected_cidr = ['192.168.0.0', '24']
            assert fa01._cidr == expected_cidr, cidr_message

    def test_spaced_ip_address(self,default_interface):
        ip = '192.168.1.1'
        fa01 = default_interface
        # |= 3 spaces, { = start, } = finish, < = spaces from left, > = spaces from right
        #  {|<>|} , {|<},{>|},{a|b},{a|b|>}
        ips = [f'   {ip}   ',f'{ip}   ',f'   {ip}',f'192.168.   1.1',f'192.168.   1.1   ']
        for ip_address in ips:
            fa01.ip_address = ip_address
            ip_address_message = f'IP address <{ip_address}> is invalid'
            assert ip == fa01.ip_address,ip_address_message


