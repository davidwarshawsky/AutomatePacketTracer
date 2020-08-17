from router import Router
from interface import *
from protocols import *
commands = ["en", "conf t", "no ip domain-lookup"]


def main():
    prompt = ["N for new router","A for a new interface","D for done with current router","Q to finish","R for a reminder"]
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
    main()

