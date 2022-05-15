import subprocess
import optparse
import re
from getmac import get_mac_address as gma

def getUserInput():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--interface",dest="interface",help="interface to change")
    parse_object.add_option("-m", "--mac",dest="mac",help="New MAC address")
    return parse_object.parse_args()

(user_input, arguments) = getUserInput()
default_mac = gma(interface=user_input.interface)

def macchanger(interface, mac):
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig",interface,"up"])

def controlNewMac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    if new_mac:
        return new_mac.group(0)
    else:
        return None

print("Macchanger started")
macchanger(user_input.interface, user_input.mac)
checker = controlNewMac(user_input.interface)

if checker == user_input.mac:
    print("MAC Address changed successfully!!")
else:
    print("Macchanger failed :(")

while True:
    try:
        print("Press Ctrl + C to exit")
        input()
    except KeyboardInterrupt:
        print('Setting default MAC address and exitting')
        subprocess.call(["ifconfig",user_input.interface,"down"])
        subprocess.call(["ifconfig", user_input.interface, "hw", "ether", default_mac])
        subprocess.call(["ifconfig",user_input.interface,"up"])
        break
    else:
        continue