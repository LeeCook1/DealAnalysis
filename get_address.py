import sys
import argparse

from geopy.geocoders import AzureMaps

geolocator = AzureMaps('eF-Nq5c-cCDqpjIVFyfK1CgZwHNcnkG5iA9uTBl9ADw')


def get_args():
    description = ''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--address','-a', help='Property Address')
    parser.add_argument('--file', '-f', help="File with addresses to get")
    return parser.parse_args()
    
def get_address_from_file(file_name):
    with open(file_name,'r') as f:
        for line in f:
            address = line.strip()
            if not address: continue
            print(get_address(address))

def get_address(address):
    return geolocator.geocode(address)

def main():
    args = get_args()
    if args.address:
        print(get_address(args.address))

    elif args.file:
        get_address_from_file(args.file)

if __name__ == '__main__':
    main()
