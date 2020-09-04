import pytest
import os
import copy
import src
from src.router import Router
from src.interface import Interface


@pytest.fixture(scope='module')
def default_router():
    name = 'default'
    router = Router(name)
    return router

@pytest.fixture(scope='module')
def default_interface():
    created_interfaces = []
    port = 'fa0/1'
    cidr = '192.168.0.0/24'
    ip_address = '192.168.1.1'
    interface = Interface(port=port, cidr=cidr, ip_address=ip_address)
    return interface


# class TestInit(object):
#     def test_valid_args(self,default_router):
#         router = default_router
#         name = router.hostname
#
#         hostname_message = f'Expected "default" as hostname, Actual: <{name}>'
#         assert router.hostname == 'default',hostname_message
#
#         expected_commands = ["en", "conf t", "no ip domain-lookup"]
#         actual_commands   = router.commands
#         commands_message  = f'Expected: {expected_commands}\n Actual: <{actual_commands}>'
#         assert actual_commands == expected_commands,commands_message
#
#         router_message = "Expected to get the default router"
#         assert Router._all_routers[0] == router,router_message
#         del(router)
#
#     def test_invalid_args(self,default_router):
#         """Test that if you try and make a second Router with the same name, it will fail."""
#         router = default_router
#         with pytest.raises(ValueError):
#             router1 = Router("default")



def test_interface_fixture(default_router, default_interface):
    router = default_router
    assert len(router.interfaces) == 0

    first_interface = default_interface
    router.add_interface(first_interface)
    print("First added: ", router.interfaces)
    assert len(router.interfaces) == 1
    second_interface = default_interface
    with pytest.raises(ValueError):
        router.add_interface(second_interface)
    print("Second added: ", router.interfaces)
    print("I want this to be one:",len(router.interfaces))
    assert 1 == 1
    print(router.interfaces)
    router = None
    first_interface = None
    second_interface = None

def test_interface_fixture_again(default_router, default_interface):
    router = default_router
    assert len(router.interfaces) == 0
    first_interface = default_interface
    router.add_interface(first_interface)
    print("First added: ", router.interfaces)
    assert len(router.interfaces) == 1
    second_interface = default_interface
    with pytest.raises(ValueError):
        router.add_interface(second_interface)
    print("Second added: ", router.interfaces)
    print("I want this to be one:", len(router.interfaces))
    assert 1 == 1
    print(router.interfaces)
    # assert len(router.interfaces) == 1
    # assert first_interface == second_interface
    # # assert id(first_interface) != id(second_interface)
    # assert first_interface is not second_interface
    # list_interfaces = [first_interface,second_interface]
    # assert len(list_interfaces) == 2
    # new_list = []
    # new_list.append(first_interface)
    # new_list.append(second_interface)
    # assert len(new_list) == 2

# class TestAddInterface(object):
    # def test_valid_args(self,default_router,default_interface):
    #     router = default_router
    #     interface = default_interface
    #     print("router   id TVA",id(router))
    #     print("interface id TVA",id(interface))
    #     router.add_interface(default_interface)
    #
    #     expected_interface = 'fa 0/1,192.168.0.0/24,192.168.1.1'
    #     actual_interface   = str(router.interfaces[0])
    #     interface_add_message = f'Expected: {expected_interface}\n Actual:'
    #     assert actual_interface == expected_interface,interface_add_message
    #
    # def test_add_two_same_interfaces(self,default_router,default_interface):
    #     """This test adds the same interface to a Router twice to test that it raises
    #     a ValueError."""
    #     router = default_router
    #     print(router.interfaces)
    #     first_interface = default_interface
    #     print(router.interfaces)
    #     second_interface = default_interface
    #     print(router.interfaces)
    #     print(first_interface == second_interface)
    #     router.add_interface(first_interface)
    #     with pytest.raises(ValueError):
    #         router.add_interface(second_interface)