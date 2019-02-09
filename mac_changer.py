#!/urs/bin/env python

"""

"""
# Import the necessary packages
import random
import subprocess
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser(description="Generate random MAC address")
    parser.add_argument('-i', '--interface', required=True,
                        help='Network interface to change its MAC Address.')
    parser.add_argument('-m', '--mac', required=False,
                        help="New Mac Address of your network interface.")

    interface, new_mac = vars(parser.parse_args()).values()

    if new_mac is None:
        new_mac = generate_random_mac()

    return interface, new_mac


def generate_random_mac():
    # You can only set unicast address address: the first octet needs to be even
    random_mac = ['{:02x}'.format(random.randrange(0, 254, 2))]

    # Generate a random value for the remaining five octets
    random_mac.extend(['{:02x}'.format(random.randint(0, 255)) for _ in range(5)])

    return ':'.join(random_mac)


def get_mac_address(interface):
    # Get informations from > ifconfig {interface}
    ifconfig_output = subprocess.check_output('ifconfig {}'.format(interface), shell=True).decode('ascii')

    # Get MAC Address g Regular expression perations
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)

    if not mac_search_result:
        print("[-] Could not read MAC address...\n")

        return 'xx:xx:xx:xx:xx:xx'

    else:
        mac_address = mac_search_result.group(0)

        return mac_address


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for {} to {}...\n".format(interface, new_mac))

    subprocess.call('ifconfig {} down'.format(interface), shell=True)
    subprocess.call('ifconfig {} hw ether {}'.format(interface, new_mac), shell=True)
    subprocess.call('ifconfig {} up'.format(interface), shell=True)


def main():
    # Get arguments (Interface/new MAC address) from cli
    interface, new_mac = get_arguments()

    old_mac_address = get_mac_address(interface)
    print("[+] Current MAC address: {}\n".format(old_mac_address))

    # Change MAC Address of selected interface
    change_mac(interface, new_mac)

    current_mac_address = get_mac_address(interface)

    # Check if MAC address was changed
    if current_mac_address ==  new_mac:
        print("[+] MAC address successfully changed to {}!\n".format(new_mac))
    else:
        print("[-] MAC address was not changed!\n")


if __name__ == '__main__':
    main()
